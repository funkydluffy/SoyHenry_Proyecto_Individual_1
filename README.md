# GUIDE: RECOMMENDATION SYSTEM IN FASTAPI+RENDER

In this repository, we will follow a step-by-step guide to build a machine learning model that was requested. This model should give us movie recommendations based on a chosen movie. In this specific context, we are asked to consider the time it takes, prioritizing speed over perfection.

We will cover the following 5 points:

## 1. ETL

We will have two `.csv` files where we will need to:

- Choose columns to drop
- Unnest columns
- Handle null values
- Format dates to a specific format
- Generate additional columns

It will be essential to consider the size of the final dataframes we will use to ensure we can work with them on GitHub and later in an API from Render.
We have a file called `ETL_PI1.ipynb`, which includes a suggested guide to help clean the data as needed. We will download it and follow the steps.

## 2. API

An API (Application Programming Interface) is a set of rules and definitions that allow different applications to communicate with each other. Essentially, an API defines how developers can interact with a service or application, providing a means for different programs to request and send information between them.
Within it, we will create functions to obtain specific data from the datasets and also to upload our recommendation system.
We have a file `main.py` where the functions are developed, and each step is commented on to help us understand the code that we will visualize.

## 3. Render

Render is a cloud hosting platform that allows developers to deploy web applications, APIs, databases, and other services easily and efficiently. Render focuses on automation and simplicity, enabling developers to focus more on developing their applications and less on managing infrastructure.
We will learn to use the platform to launch our API through this tutorial: https://github.com/HX-FNegrete/render-fastapi-tutorial, allowing our clients to test it.
We will have Render take our `main.py` and our datasets to run our API, obtaining a link that will allow us to share it.
Here’s the link provided by Render for this repository: https://soyhenry-proyecto-individual-1.onrender.com/docs

## 4. EDA

We have an EDA analysis (`PI1_EDA.ipynb`), not too deep (since we are prioritizing speed), which we will use to show some metrics and get an idea of how our datasets work.

## 5. Recommendation System

We will develop a machine learning model that will give us five movie recommendations as a result of inputting a reference movie into the system.
This is developed in our `main.py` and can be accessed through Render in our FASTAPI.

I hope this guide and documentation are easy to understand and help anyone with the necessary knowledge to develop this project.

This project was carried out by Gabriel Coria. (https://www.linkedin.com/in/coriagabriel/)
The project request was made by SoyHenry to put into practice the knowledge acquired in the Data Science bootcamp. (https://www.linkedin.com/school/henryok)


---


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

