# Algoritmo de identificación de dígitos manusccritos
 
Este repositorio contiene el código de un algoritmo que emplea un ensamble de modelos de aprendizaje automático (*machine learning*, o ML) para reconocer números manuscritos.

* El script principal es un `Jupyter notebook` en formato de presentación interactiva.
* El modelo final (un ensamble de votación) se almacena en un archivo `jobfile`.
* Este archivo se copia en la carpeta `webapp`, que contiene una aplicación web para que los usuarios puedan interactuar con el modelo.

La aplicación web está en línea en http://rleo.pythonanywhere.com.

Los modelos ML están entrenados usando un subconjunto de [esta base de datos](https://archive.ics.uci.edu/ml/datasets/optical+recognition+of+handwritten+digits). El módulo de Python empleado es `sckit-learn`.

¡Gracias!
