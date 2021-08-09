# Importar librerías
import dash
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from requests import get
from datetime import timedelta
import plotly.io as pio
import json
import dash_bootstrap_components as dbc
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Configurar vistas y colores:
pio.templates.default = "plotly_white"
colores_discretos = px.colors.qualitative.Prism

# URL de la base de datos de COVID-19:
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'

# Descargar última versión de la base de datos:
descargar = False

# Rutina de descarga:
if descargar:
    archivo_remoto = get(url, allow_redirects = True)
    archivo_local = open(os.path.join(THIS_FOLDER, 'covid_data.csv'), 'wb')
    archivo_local.write(archivo_remoto.content)
    archivo_local.close()

# Importar datos de COVID-19:
data = pd.read_csv(os.path.join(THIS_FOLDER, 'covid_data.csv'))

# Importar información geoespacial:
paises_archivo = open(os.path.join(THIS_FOLDER, 'custom.geo.json'))
paises = json.load(paises_archivo)
paises_archivo.close()

# Preprocesamiento de la base de datos:
data['date'] = pd.to_datetime(data['date'])
fecha_max = pd.to_datetime(max(data['date'].unique()))
fecha_min = pd.to_datetime(min(data['date'].unique()))
periodos = [(y, m) for y in range(fecha_min.year, fecha_max.year + 1) for m in range(fecha_min.month, fecha_max.month + 1)]
fechas = {x: {'periodo': periodos[x], 'periodo_str': str(periodos[x][0]) + '-' + str(periodos[x][1])} for x in range(0, len(periodos))}
data['total_vaccinations_per_hundred'] = data.groupby('location')['total_vaccinations_per_hundred'].fillna(0, limit = 1)
data['total_vaccinations_per_hundred'] = data.groupby('location')['total_vaccinations_per_hundred'].fillna(method = 'ffill')

periodos_dict = {
    0: pd.to_datetime(fecha_min).strftime('%Y-%m-%d'),
    1: (pd.to_datetime(fecha_max) - timedelta(days = 365)).strftime('%Y-%m-%d'),
    2: (pd.to_datetime(fecha_max) - timedelta(days = 30 * 6)).strftime('%Y-%m-%d'),
    3: (pd.to_datetime(fecha_max) - timedelta(days = 30)).strftime('%Y-%m-%d'),
    4: (pd.to_datetime(fecha_max) - timedelta(days = 7)).strftime('%Y-%m-%d')
}

variables_dict = {
    'pob_vac': 'total_vaccinations_per_hundred',
    'muertes_pm': 'total_deaths_per_million',
    'casos_pm': 'total_cases_per_million'
}

tamano_dict = {
    'pob': 'population',
    'pib': 'gdp_per_capita',
    'non': None
}

# Instancia principal de la app:
app_datos = dash.Dash(
    __name__,
    requests_pathname_prefix = '/datos/',
    external_stylesheets = [dbc.themes.FLATLY]
)

# Importar layout y cargarla en la instancia de la app:
from datos_layout import layout
app_datos.layout = layout(fecha_min, fecha_max)

@app_datos.callback(
    Output("modal", "is_open"),
    [Input("abrir", "n_clicks"), Input("cerrar", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# RESUMEN MUNDIAL

@app_datos.callback(
    Output(component_id = 'casos_mundiales_totales', component_property = 'figure'),
    Output(component_id = 'casos_mundiales_nuevos', component_property = 'figure'),
    Output(component_id = 'poblacion_mundial_vacunada', component_property = 'figure'),
    Output(component_id = 'eficacia_vacunacion_mundial', component_property = 'figure'),
    Input(component_id = 'periodo', component_property = 'value')
)
def resumen_mundial(valor):
    fecha_limite = periodos_dict[valor]
    datos = data.query(f"location in ('Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America') & date >= '{fecha_limite}'")

    casos_mundiales_totales = px.area(
        datos,
        x = 'date',
        y = 'total_cases',
        color = 'location',
        labels = {'date': 'Fecha', 'total_cases': 'Casos acumulados','location': 'Continente'},
        title = 'Casos acumulados (mundiales)',
        color_discrete_sequence = colores_discretos
    )

    casos_mundiales_nuevos = px.area(
        datos,
        x = 'date',
        y = 'new_cases_smoothed',
        color = 'location',
        labels = {'date': 'Fecha', 'new_cases_smoothed': 'Nuevos casos semanales','location': 'Continente'},
        title = 'Nuevos casos diarios (mundiales)',
        color_discrete_sequence = colores_discretos
    )

    poblacion_mundial_vacunada = px.line(
        datos,
        x = 'date',
        y = 'total_vaccinations_per_hundred',
        color = 'location',
        labels = {'date': 'Fecha', 'total_vaccinations_per_hundred': 'Dosis por cada 100 habitantes','location': 'Continente'},
        title = 'Dosis admistradas por cada 100 habitantes',
        color_discrete_sequence = colores_discretos
    )

    eficacia_vacunacion_mundial = px.density_contour(
        data.query(f"location in ('World') & date >= '{fecha_limite}'"),
        x = 'date',
        y = 'total_vaccinations_per_hundred',
        z = 'new_deaths_smoothed',
        histfunc = 'sum',
        labels = {'date': 'Fecha', 'total_vaccinations_per_hundred': 'Población vacunada (%)','new_deaths_smoothed': 'Nuevas muertes semanales'},
        title = 'Eficacia de la vacunación para prevenir muertes (agregado mundial)'
    )
    eficacia_vacunacion_mundial.update_traces(contours_coloring="fill", colorscale='Reds')
    eficacia_vacunacion_mundial.add_scatter(
        x = data.query(f"location in ('World') & date >= '{fecha_limite}'")['date'],
        y = data.query(f"location in ('World') & date >= '{fecha_limite}'")['total_vaccinations_per_hundred'],
        mode = 'lines',
        name = 'Población mundial vacunada (%)'
    )

    casos_mundiales_totales.update_layout(transition_duration=500)
    casos_mundiales_nuevos.update_layout(transition_duration=500)
    poblacion_mundial_vacunada.update_layout(transition_duration=500)
    eficacia_vacunacion_mundial.update_layout(transition_duration=500)

    return (
        casos_mundiales_totales,
        casos_mundiales_nuevos,
        poblacion_mundial_vacunada,
        eficacia_vacunacion_mundial
    )


# MAPA DEL MUNDO

@app_datos.callback(
    Output(component_id = 'casos_mundo', component_property = 'figure'),
    Input(component_id = 'variable', component_property = 'value'),
    Input(component_id = 'fecha', component_property = 'date')
)
def mapa_mundo(variable, fecha):
    datos = data.query(f"date == '{pd.to_datetime(fecha).strftime('%Y-%m-%d')}'")
    casos_mundo = px.choropleth_mapbox(
        datos,
        geojson = paises,
        featureidkey = 'properties.iso_a3',
        locations = 'iso_code',
        color = variables_dict[variable],
        mapbox_style = 'carto-positron',
        hover_name = 'location',
        hover_data = {'iso_code': False},
        zoom = 1,
        center = {"lat": 26, "lon": -42},
        opacity = 0.5,
        labels = {
            'total_vaccinations_per_hundred': 'Dosis (por 100 personas)',
            'total_deaths_per_million': 'Muertes (por 1M de personas)',
            'total_cases_per_million': 'Casos (por 1M de personas)'
        }
    )

    casos_mundo.update_layout(transition_duration=500, margin={"r":0,"t":0,"l":0,"b":0})

    return casos_mundo


# FACTORES DE RIESGO

@app_datos.callback(
    Output(component_id = 'diabetes', component_property = 'figure'),
    Output(component_id = 'cardio', component_property = 'figure'),
    Output(component_id = 'higiene', component_property = 'figure'),
    Output(component_id = 'camas', component_property = 'figure'),
    Output(component_id = 'esperanza', component_property = 'figure'),
    Output(component_id = 'desarrollo', component_property = 'figure'),
    Input(component_id = 'regiones', component_property = 'value'),
    Input(component_id = 'tamano', component_property = 'value')
)
def factores_riesgo(regiones, tamano):
    datos = data.query(f"date == '{fecha_max.strftime('%Y-%m-%d')}' & population == population & gdp_per_capita == gdp_per_capita & location not in ('World', 'Asia', 'North America', 'South America', 'Europe', 'Oceania') & continent == {str(regiones)}")
    size = tamano_dict[tamano]

    diabetes = px.scatter(
        datos,
        x = 'diabetes_prevalence',
        y = 'total_deaths_per_million',
        size = size,
        hover_name = 'location',
        hover_data = {'location': False, 'population': False},
        title = 'Prevalencia de diabetes',
        labels = {
            'diabetes_prevalence': 'Prevalencia de diabetes (%)',
            'total_deaths_per_million': 'Muertes (por millón)'
        }
    )

    cardio = px.scatter(
        datos,
        x = 'cardiovasc_death_rate',
        y = 'total_deaths_per_million',
        size = size,
        hover_name = 'location',
        hover_data = {'location': False, 'population': False},
        title = 'Riesgo cardiovascular',
        labels = {
            'cardiovasc_death_rate': 'Mortalidad cardiovascular (por miles)',
            'total_deaths_per_million': 'Muertes (por millón)'
        }
    )

    higiene = px.scatter(
        datos,
        x = 'handwashing_facilities',
        y = 'total_deaths_per_million',
        size = size,
        hover_name = 'location',
        hover_data = {'location': False, 'population': False},
        title = 'Acceso a instalaciones sanitarias',
        labels = {
            'handwashing_facilities': 'Acceso a instalaciones sanitarias (%)',
            'total_deaths_per_million': 'Muertes (por millón)'
        }
    )

    camas = px.scatter(
        datos,
        x = 'hospital_beds_per_thousand',
        y = 'total_deaths_per_million',
        size = size,
        hover_name = 'location',
        hover_data = {'location': False, 'population': False},
        title = 'Capacidad hospitalaria',
        labels = {
            'hospital_beds_per_thousand': 'Camas de hospital (por miles)',
            'total_deaths_per_million': 'Muertes (por millón)'
        }
    )

    esperanza = px.scatter(
        datos,
        x = 'life_expectancy',
        y = 'total_deaths_per_million',
        size = size,
        hover_name = 'location',
        hover_data = {'location': False, 'population': False},
        title = 'Esperanza de vida',
        labels = {
            'life_expectancy': 'Esperanza de vida al nacer',
            'total_deaths_per_million': 'Muertes (por millón)'
        }
    )

    desarrollo = px.scatter(
        datos,
        x = 'human_development_index',
        y = 'total_deaths_per_million',
        size = size,
        hover_name = 'location',
        hover_data = {'location': False, 'population': False},
        title = 'Índice de desarrolo humano',
        labels = {
            'human_development_index': 'Índice de desarrollo humano',
            'total_deaths_per_million': 'Muertes (por millón)'
        }
    )

    diabetes.update_layout(transition_duration=500, showlegend=False)
    cardio.update_layout(transition_duration=500, showlegend=False)
    higiene.update_layout(transition_duration=500, showlegend=False)
    camas.update_layout(transition_duration=500, showlegend=False)
    esperanza.update_layout(transition_duration=500, showlegend=False)
    desarrollo.update_layout(transition_duration=500, showlegend=False)

    return (
        diabetes,
        cardio,
        higiene,
        camas,
        esperanza,
        desarrollo
    )
