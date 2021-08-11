import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from pandas import to_datetime

def layout(fecha_min, fecha_max, filas, columnas):

    texto_markdown = """
    **Visualización de datos globales sobre COVID-19**

    Este proyecto está escrito por completo usando Python, y el objetivo es mostrar las posibilidades que tiene la implementación conjunta de las siguientes tecnologías en este lenguaje:
    * `pandas` para el análisis y manipulación de grandes bases de datos.
    * `dash` y `plotly` para generar gráficos dinámicos.
    * `flask` para escribir aplicaciones web usando Python.

    **Fuente de datos**

    Los datos se descargan autmáticamente de [github.com/owid/covid-19-data](https://github.com/owid/covid-19-data), que es el repositorio de información sobre COVID-19 que actualiza diariamente el equipo de [Our World in Data](https://ourworldindata.org). La base de datos descargada se preprocesa usando `pandas` y con ella se generan las visualizaciones mostradas aquí.

    ---
    **Rodrigo Leo (2021)** - Consulta el código fuente de este proyecto en mi GitHub: [github.com/r-leo/proyecto-python](https://github.com/r-leo/proyecto-python).
    """

    return dbc.Container(fluid = True, children = [

        dbc.Modal([
            dbc.ModalHeader("Acerca de"),
            dbc.ModalBody(dcc.Markdown(texto_markdown)),
            dbc.ModalFooter(dbc.Button("Cerrar", id = "cerrar", className = "ml-auto", n_clicks = 0, color = 'info')),
        ],
        id = 'modal',
        size = 'lg',
        is_open = False
        ),

        dbc.Row(
            dbc.Col([
                html.H1('Visualizador interactivo COVID-19'),
                html.H4('Rodrigo Leo, 2021'),
                html.P([
                    'Fuente de datos: ',
                    html.A('github.com/owid/covid-19-data', href = 'https://github.com/owid/covid-19-data', target = '_blank'),
                    html.Br(),
                    'Fecha más reciente en la base de datos: ',
                    dbc.Badge(f'{to_datetime(fecha_max).date()}', color = 'info'),
                    html.Br(),
                    'Tamaño de la base de datos: ',
                    dbc.Badge(f'{"{:,}".format(filas)} filas', color = 'light'),
                    ' x ',
                    dbc.Badge(f'{"{:,}".format(columnas)} columnas', color = 'light'),
                    ' = ',
                    dbc.Badge(f'{"{:,}".format(filas * columnas)} datos', color = 'light'),
                ]),
                dbc.Button("Acerca de este proyecto", id="abrir", n_clicks = 0, outline = True, color = 'info')
            ])
        ),

        dbc.Row(
            dbc.Col([
                html.Hr(),
                html.H2('Resumen mundial')
            ])
        ),

        dbc.Row([
            dbc.Col(width = 3, children = [
                dbc.Label("Horizonte de tiempo a mostrar"),
                dcc.Dropdown(
                    id = 'periodo',
                    options = [
                        {'label': 'Todos los datos', 'value': 0},
                        {'label': 'Último año', 'value': 1},
                        {'label': 'Últimos seis meses', 'value': 2},
                        {'label': 'Últimos 30 días', 'value': 3},
                        {'label': 'Últimos 7 días', 'value': 4}
                    ],
                    value = 0,
                    searchable = False,
                    clearable = False
                )
            ])
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id = 'casos_mundiales_totales')),
            dbc.Col(dcc.Graph(id = 'casos_mundiales_nuevos'))
        ]),

        dbc.Row([
            dbc.Col(children = dcc.Graph(id = 'poblacion_mundial_vacunada')),
            dbc.Col(dcc.Graph(id = 'eficacia_vacunacion_mundial'))
        ]),

        dbc.Row(
            dbc.Col([
                html.Hr(),
                html.H2('Mapa mundial de monitoreo')
            ])
        ),

        dbc.Row([
            dbc.Col(width = 4, children = [
                dbc.Label("Variable de interés"),
                dcc.Dropdown(
                    id = 'variable',
                    options = [
                        {'label': 'Dosis administradas (por cada 100 habitantes)', 'value': 'pob_vac'},
                        {'label': 'Casos totales (por millón de habitantes)', 'value': 'casos_pm'},
                        {'label': 'Muertes totales (por millón de habitantes)', 'value': 'muertes_pm'}
                    ],
                    value = 'pob_vac',
                    searchable = False,
                    clearable = False
                )
            ]),
            dbc.Col(width = 8, children = [
                dbc.Label("Fecha"),
                html.P(
                    dcc.DatePickerSingle(
                        id = 'fecha',
                        min_date_allowed = fecha_min,
                        max_date_allowed = fecha_max,
                        initial_visible_month = fecha_max,
                        date = fecha_max
                    )
                )
            ])
        ]),

        dbc.Row([
            dbc.Col(children = dcc.Graph(id = 'casos_mundo'))
        ]),

        dbc.Row(
            dbc.Col([
                html.Hr(),
                html.H2('Factores de riesgo')
            ])
        ),

        dbc.Row([
            dbc.Col(width = 4, children = [
                dbc.Label("Ajustar tamaño por variable"),
                dcc.Dropdown(
                    id = 'tamano',
                    options = [
                        {'label': 'Ninguno', 'value': 'non'},
                        {'label': 'Población', 'value': 'pob'},
                        {'label': 'PIB per cápita', 'value': 'pib'}

                    ],
                    value = 'non',
                    searchable = False,
                    clearable = False
                )
            ]),
            dbc.Col(width = 8, children = [
                dbc.Label("Regiones"),
                dcc.Checklist(
                    id = 'regiones',
                    options = [
                        {'label': 'África', 'value': 'Asia'},
                        {'label': 'Asia', 'value': 'Africa'},
                        {'label': 'Europa', 'value': 'Europe'},
                        {'label': 'Norteamérica', 'value': 'North America'},
                        {'label': 'Sudamérica', 'value': 'South America'},
                        {'label': 'Oceanía', 'value': 'Oceania'}

                    ],
                    value = ['Asia', 'Africa', 'Europe', 'North America', 'South America', 'Oceania'],
                    labelStyle = {'display': 'inline-block', 'margin-left': '10px', 'margin-right': '5px'}
                )
            ])
        ]),

        dbc.Row([
            dbc.Col(width = 4, children = dcc.Graph(id = 'diabetes')),
            dbc.Col(width = 4, children = dcc.Graph(id = 'cardio')),
            dbc.Col(width = 4, children = dcc.Graph(id = 'higiene'))
        ]),

        dbc.Row([
            dbc.Col(width = 4, children = dcc.Graph(id = 'camas')),
            dbc.Col(width = 4, children = dcc.Graph(id = 'esperanza')),
            dbc.Col(width = 4, children = dcc.Graph(id = 'desarrollo'))
        ]),

    ])
