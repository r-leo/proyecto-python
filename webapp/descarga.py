import requests
import os

# Importar token para la API de PythonAnywhere:
import pa_token

# Credenciales para la API:
username = pa_token.username
token = pa_token.token
domain_name = 'rleo.pythonanywhere.com'

# Variable de ruta:
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# URL de la base de datos de COVID-19:
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'

# Rutina de descarga:
archivo_remoto = requests.get(url, allow_redirects = True)
archivo_local = open(os.path.join(THIS_FOLDER, 'covid_data.csv'), 'wb')
archivo_local.write(archivo_remoto.content)
archivo_local.close()

# Reiniciar app:
response = requests.post(
    'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
        username = username,
        domain_name = domain_name
    ),
    headers={'Authorization': 'Token {token}'.format(token=token)}
)

# Salida:
if response.status_code == 200:
    print('Success!')
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
