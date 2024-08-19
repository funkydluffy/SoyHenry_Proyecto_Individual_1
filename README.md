# GUIA: SISTEMA DE RECOMENDACION EN FASTAPI+RENDER

En este repositorio vamos a seguir paso a paso una guía para montar un modelo de machine learning que nos pidieron. Este modelo debe darnos recomendaciones de películas en base a una película elegida. En este contexto específico, nos piden que tengamos en cuenta el tiempo que tardamos, priorizando la velocidad antes que la perfección.

Recorreremos los siguientes 5 puntos:

## 1. ETL

Tendremos dos archivos `.csv` en los que tendremos que:

- Elegir columnas a retirar
- Columnas a desanidar
- Tratar nulos
- Dar un formato específico a las fechas
- Generar columnas extras

Será fundamental tener en cuenta el tamaño de los dataframes finales que utilizaremos para poder trabajarlos en GitHub y posteriormente en una API desde Render.
Tenemos un archivo ETL_PI1.ipynb en donde hay una guía tipo sugerencia para poder realizar la limpieza deseada de los datos, procederemos a descargar y seguir los pasos.

## 2. API

Una API es una Interfaz de Programación de Aplicaciones (por sus siglas en inglés, Application Programming Interface), es un conjunto de reglas y definiciones que permiten que diferentes aplicaciones se comuniquen entre sí. En esencia, una API define la forma en que los desarrolladores pueden interactuar con un servicio o aplicación, proporcionando un medio para que diferentes programas puedan solicitar y enviar información entre sí.
Dentro de ella generaremos funciones para obtener datos específicos de los datasets y también para subir nuestro sistema de recomendación.
Tenemos un archivo main.py donde están desarrolladas las funciones y en donde tenemos comentado cada uno de los pasos para poder entender el código que visualizaremos.

## 3. Render

Render es una plataforma de cloud hosting que permite a los desarrolladores desplegar aplicaciones web, APIs, bases de datos, y otros servicios de manera sencilla y eficiente. Render se enfoca en la automatización y simplicidad, permitiendo que los desarrolladores se concentren más en el desarrollo de sus aplicaciones y menos en la gestión de infraestructura.
Aprenderemos a utilizar la plataforma para levantar nuestra API por medio de este tutorial: https://github.com/HX-FNegrete/render-fastapi-tutorial y que se pueda probar por nuestros clientes.
Haremos que Render tome nuestro main.py y nuestros datasets para correr nuestra API obteniendo un link que nos permitira compartirla.
Así se ve el link otorgado por Render de este repositorio: https://soyhenry-proyecto-individual-1.onrender.com/docs

## 4. EDA

Tenemos un análisis EDA (PI1_EDA.ipynb), no tan profundo (tendremos en cuenta priorizar la velocidad), que utilizaremos para mostrar algunas métricas para tomar dimensión y consciencia de cómo funcionan nuestros datasets.

## 5. Sistema de Recomendación

Desarrollaremos un modelo de machine learning que nos entregará cinco recomendaciones de películas en resultado a una película de referencia que le entregaremos al sistema.
Este mismo está desarrollado en nuestro main.py y se puede acceder por medio de Render en nuestra FASTAPI.

Espero que toda esta guia y documentación se fácil de entender y que pueda ayudar a cualquiera con los conocimientos necesarios a poder desarrollar este proyecto.

Este proyecto fué realizado por Gabriel Coria. (https://www.linkedin.com/in/coriagabriel/)
El pedido del proyecto está hecho por SoyHenry con el objetivo de poner en práctica los conocimientos adquiridos en el bootcamp de Data Science. (https://www.linkedin.com/school/henryok)

