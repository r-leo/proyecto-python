from flask import Blueprint, Flask, render_template, url_for, request
import os

from digitos import app_digitos
from datos import app_datos

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

app.register_blueprint(app_digitos)

@app.route("/")
def principal():
    return """
    <p>Aplicación:</p>
    <ul>
        <li><a href='/digitos'>Reconocimiento de dígitos manuscritos usando aprendizaje automático</a></li>
        <li><a href='/datos'>Visualización interactiva de datos sobre COVID-19</a></li>
    </ul>
    """
