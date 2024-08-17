# GUIA: SISTEMA DE RECOMENDACION EN FASTAPI

En este repositorio vamos a seguir paso a paso una guía para montar un modelo de machine learning que nos pidieron. Este modelo debe darnos recomendaciones de películas en base a una película elegida. En este contexto específico, nos piden que tengamos en cuenta el tiempo que tardamos, priorizando la velocidad a la perfección.

Recorreremos los siguientes 5 puntos:

## 1. ETL

Tendremos dos archivos `.csv` en los que tendremos que:

- Elegir columnas a retirar
- Columnas a desanidar
- Tratar nulos
- Dar un formato específico a las fechas
- Generar columnas extras

Será fundamental tener en cuenta el tamaño de los dataframes finales que utilizaremos para poder trabajarlos en GitHub y posteriormente en una API desde Render.

## 2. API

Generaremos funciones para obtener datos específicos de los datasets y también para subir nuestro sistema de recomendación.

## 3. Render

Aprenderemos a utilizar la plataforma para levantar nuestra API y que se pueda probar por nuestros clientes.

## 4. EDA

Agregaremos un análisis EDA, no tan profundo (tendremos en cuenta priorizar la velocidad), que utilizaremos para mostrar algunas métricas para tomar dimensión y consciencia de cómo funcionan nuestros datasets.

## 5. Sistema de Recomendación

Desarrollaremos un modelo de machine learning que nos entregará cinco recomendaciones de películas en resultado a una película de referencia que le entregaremos al sistema.
