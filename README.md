# Galería de proyectos de Python
 
## Qué es esto

Este repositorio contiene el código de dos proyectos hechos en Python:

* Un algoritmo de que emplea un ensamble de modelos de aprendizaje automático (*machine learning*, o ML) para reconocer números manuscritos.
* Un visualizador de datos globales del COVID-19.

Los dos proyectos están en línea en http://rleo.pythonanywhere.com.

## Notas

* El modelo ML está entrenado usando un subconjunto de [esta base de datos](https://archive.ics.uci.edu/ml/datasets/optical+recognition+of+handwritten+digits). El módulo de Python empleado es `sckit-learn`.
* Los datos del COVID-19 provienen del [repositorio abierto](https://github.com/owid/covid-19-data) de datos recoletados por [Our World in Data](https://ourworldindata.org). El análisis de los datos se hace mediante `pandas`, y las visualizaciones con `dash` y `plotly`.
* En ambos casos usé `flask` para crear las aplicaciones web a partir de código Python.

¡Gracias!
