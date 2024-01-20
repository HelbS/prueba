# Dashboard usando Dash

## 1. Introducción.

Crear un Dashboard web simple, que permita comparar la evolución mes a mes de los
ingresos y Costo de servicios para una compañía de ejemplo:
- El proyecto se debe desarrollar usando Dash (plotly) en lenguaje Python.
https://dash.plotly.com/
- El Dashboard debe contener una sola gráfica que permita comparar fácilmente la
evolución de los costos e ingresos.
- El Dashboard debe contener un filtro de selección múltiple que permita actualizar la
gráfica incluyendo o descartando líneas de negocio.


## 2. Consideraciones
- Se hizo la carga de los datasets y su limpieza. Aunque los datasets son similares, tienen factores que diferencian su tratamiento, por ejm la presencia del signo $.
- Se hizo la agregacion de datos a nivel de "Line of business", pues es el nivel de granularidad necesario para el dashboard.
- Ejecute el programa app.py en su terminal.