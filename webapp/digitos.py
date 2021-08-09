# Importar librerías de Flask:
from flask import Blueprint, render_template, url_for, request

# Importar otras librerías:
from re import sub
from PIL import Image
from io import BytesIO
import base64
from random import randrange
import os
from joblib import load
from numpy import array

# Variable de entorno (pathname):
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

# Instancia principal de la app:
app_digitos = Blueprint('digitos' ,__name__)


@app_digitos.route("/digitos")
def digitos():
    return render_template(
    'principal.html',
    estilo = url_for('static', filename='estilo.css'),
    codigo = url_for('static', filename='canvas.js'),
    jquery = url_for('static', filename='jquery.js'),
    redirect = url_for('static', filename='redirect.js')
    )


@app_digitos.route("/procesar", methods = ['POST'])
def procesar():
    # Extraer string de la imagen (base 64):
    imagen_str = sub('^data:image/.+;base64,', '', request.form['img'])

    # Construir medidas de recorte:
    crop_d = {
        'l': abs(int(request.form['l'])),
        't': abs(int(request.form['t'])),
        'r': abs(int(request.form['r'])),
        'b': abs(int(request.form['b'])),
        'w': abs(int(request.form['w'])),
        'h': abs(int(request.form['h']))
    }

    # Crear objeto Image
    im = Image.open(BytesIO(base64.b64decode(imagen_str)))

    # Obtener ancho (w) y alto (h):
    w = im.width
    h = im.height

    # Recortar imagen:
    im = im.crop((0, crop_d['t'], w, crop_d['b']))

    # Calcular longitud de los cuadrantes:
    len_x = int(im.width / 8)
    len_y = int(im.height / 8)

    # Rutina para extraer y contar píxeles cuadrante a cuadrante:
    bitmap = []
    for y in range(0, 8):
        row = []
        for x in range(0, 8):
            xlim = (x * len_x, (x + 1) * len_x)
            ylim = (y * len_y, (y + 1) * len_y)
            pixels = 0
            for yy in range(ylim[0], ylim[1]):
                for xx in range(xlim[0], xlim[1]):
                    if im.getpixel((xx, yy))[3] > 0:
                        pixels = pixels + 1
            row.append(pixels)
        bitmap.append(row)

    # Normalizar mapa de bits en el rango 0-16:
    bitmap_max = max([max(x) for x in bitmap])
    bitmap_norm = []
    for row in bitmap:
        bitmap_norm.append([int(16.0 * x / bitmap_max) for x in row])

    # Volver a recortar imagen
    h = im.height
    im = im.crop((crop_d['l'], 0, crop_d['r'], h))

    # Poner sobre fondo blanco y eliminar transparencia:
    imw = Image.new("RGBA", im.size, "WHITE")
    imw.paste(im, (0, 0), im)
    imw = imw.convert('RGB')

    # Generar id:
    id = randrange(1000, 9999)

    # Guardar:
    imw_url = url_for('static', filename=f'generated/out{id}.jpg')
    imw.save(os.path.join(THIS_FOLDER, f'static/generated/out{id}.jpg'), "JPEG")

    # Cargar modelo entrenado:
    ensamble = load(os.path.join(THIS_FOLDER, 'ensamble.joblib'))

    # Transformar mapa de bits en array de numpy:
    x = [obs for fila in bitmap_norm for obs in fila]
    x = array(x).reshape(1, -1)

    # Predecir número empleando el modelo:
    prediccion = ensamble.predict(x)[0]

    return render_template(
    'resultado.html',
    estilo = url_for('static', filename = 'estilo.css'),
    imagen = imw_url,
    array = bitmap_norm,
    estimador = str(prediccion)
    )
