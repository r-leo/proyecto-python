from werkzeug.middleware import dispatcher
from werkzeug.serving import run_simple

from app_principal import app

from datos import app_datos

aplicacion = dispatcher.DispatcherMiddleware(app, {
    '/datos': app_datos.server,
})
