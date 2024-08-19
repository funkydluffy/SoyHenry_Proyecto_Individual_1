from fastapi import FastAPI, HTTPException
from typing import Optional
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargamos los datasets
movies_df = pd.read_csv('Datasets/movies_reducido.csv')
cast_df = pd.read_csv('Datasets/df_cast_expanded.csv')
crew_df = pd.read_csv('Datasets/filtered_credits_crew.csv')
df_movies_released = pd.read_csv('Datasets/movies_released.csv')

app = FastAPI()

# Convertimos las columnas de texto a minúsculas para uniformidad
df_movies_released['TITLE'] = df_movies_released['TITLE'].str.lower()
df_movies_released['GENRES_NAME'] = df_movies_released['GENRES_NAME'].str.lower()
df_movies_released['ORIGINAL_LANGUAGE'] = df_movies_released['ORIGINAL_LANGUAGE'].str.lower()
df_movies_released['PRODUCTION_COUNTRIES_NAME'] = df_movies_released['PRODUCTION_COUNTRIES_NAME'].str.lower()

# Creamos una columna que combine todas las características relevantes para la recomendación
df_movies_released['combined_features'] = df_movies_released.apply(
    lambda row: f"{row['REVENUE']} {row['BUDGET']} {row['RETURN']} {row['GENRES_NAME']} {row['ORIGINAL_LANGUAGE']} {row['PRODUCTION_COUNTRIES_NAME']} {row['VOTE_AVERAGE']}",
    axis=1
)

# Vectorizamos las características combinadas usando TfidfVectorizer
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(df_movies_released['combined_features'])

@app.get("/recomendacion/{titulo}")
async def recomendacion(titulo: str, num_recommendations: int = 5):
    # Convertimos el título a minúsculas para uniformidad
    titulo = titulo.lower()

    # Encontramos el índice de la película dada
    try:
        movie_idx = df_movies_released[df_movies_released['TITLE'] == titulo].index[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="La película no fue encontrada en la base de datos")

    # Calculamos la similitud del coseno entre la película dada y todas las demás
    cosine_similarities = cosine_similarity(feature_vectors[movie_idx], feature_vectors).flatten()

    # Obtenemos los índices de las películas más similares, excluyendo la película dada
    similar_indices = cosine_similarities.argsort()[-num_recommendations-1:-1][::-1]

    # Obtenemos los títulos de las películas recomendadas
    similar_movies = df_movies_released.iloc[similar_indices]['TITLE'].tolist()

    return {f"Películas recomendadas similares a {titulo}: {similar_movies}"}

@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    # Le otorgamos un valor a cada mes para que pueda ser encontrado en la columna tipo datetime
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    # Normalizamos el nombre del mes a minúsculas para evitar errores cuando se ingrese el valor
    mes_num = meses.get(mes.lower())
    # Planteamos mensajes de error
    if not mes_num:
        raise HTTPException(status_code=400, detail="Mes no válido")
    
    try:
        # Filtramos películas por el mes
        movies_df['RELEASE_DATE'] = pd.to_datetime(movies_df['RELEASE_DATE'], errors='coerce')
        count = movies_df[movies_df['RELEASE_DATE'].dt.month == mes_num].shape[0]
        return {f"{count} películas fueron estrenadas en el mes de {mes.capitalize()}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al procesar la solicitud")
    
@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia: str):
    #Transformamos los valores posibles entrantes para que puedan ser trabajados
    dias = {
        "lunes": "monday", "martes": "tuesday", "miércoles": "wednesday", "miercoles": "wednesday", 
        "jueves": "thursday", "viernes": "friday", "sábado": "saturday", "sabado": "saturday", 
        "domingo": "sunday"
    }
    # Normalizamos el nombre del mes a minúsculas para evitar errores
    dia_en = dias.get(dia.lower())
    
    if dia_en is not None:
        # Aseguramos que RELEASE_DATE es de tipo datetime
        movies_df['RELEASE_DATE'] = pd.to_datetime(movies_df['RELEASE_DATE'], errors='coerce')

        # Extraemos el día de la semana de las fechas de estreno
        movies_df['day_of_week'] = movies_df['RELEASE_DATE'].dt.day_name().str.lower()

        # Contamos las películas estrenadas en el día de la semana solicitado
        count = movies_df[movies_df['day_of_week'] == dia_en].shape[0]
        return {f"{count} películas fueron estrenadas en los días {dia.capitalize()}"}
    
    return {"Día no válido"}

@app.get("/score_titulo/{titulo}")
async def score_titulo(titulo: str):
    # Filtramos el DataFrame para encontrar la película que coincida con el título proporcionado (ignorando mayúsculas/minúsculas)
    movie = movies_df[movies_df['TITLE'].str.contains(titulo, case=False, na=False)]
    # Verificamos si la película fue encontrada
    if not movie.empty:
        # Obtenemos la fecha de estreno de la primera coincidencia
        release_date = movie.iloc[0]['RELEASE_DATE']
        # Verificamos si la fecha de estreno no es nula
        if pd.notna(release_date):
            # Si la fecha de estreno es una cadena y tiene al menos 4 caracteres, extraemos el año
            if isinstance(release_date, str) and len(release_date) >= 4:
                release_year = release_date[:4]
            # Si la fecha de estreno es un objeto Timestamp (fecha y hora), extraemos el año
            elif isinstance(release_date, pd.Timestamp):
                release_year = release_date.year
            # Si no se puede determinar el año, lo marcamos como "Desconocido"
            else:
            # Si la fecha de estreno es nula, también la marcamos como "Desconocido"
                release_year = "Desconocido"
        else:
            # Si la fecha de estreno es nula, también la marcamos como "Desconocido"
            release_year = "Desconocido"
        
        # Obtenemos la popularidad de la película si está disponible, de lo contrario, la marcamos como "Desconocido"
        popularity = movie.iloc[0]['POPULARITY'] if pd.notna(movie.iloc[0]['POPULARITY']) else "Desconocido"
        
        # Retornamos un mensaje con el título de la película, año de estreno y su popularidad
        return {
            f"La película {titulo} fue estrenada en el año {release_year} con un score/popularidad de {popularity}"
        }
    
    # Si no se encuentra la película, devolvemos un mensaje indicando que no fue encontrada
    return {"Película no encontrada"}

@app.get("/votos_titulo/{titulo}")
async def votos_titulo(titulo: str):
    # Filtramos el DataFrame para encontrar la película que coincida con el título proporcionado (ignorando mayúsculas/minúsculas)
    movie = movies_df[movies_df['TITLE'].str.contains(titulo, case=False, na=False)]
    # Filtramos el DataFrame para encontrar la película que coincida con el título proporcionado (ignorando mayúsculas/minúsculas)
    if not movie.empty:
        # Obtenemos el conteo de votos de la primera coincidencia, o 0 si es nulo
        vote_count = movie.iloc[0]['VOTE_COUNT'] if pd.notna(movie.iloc[0]['VOTE_COUNT']) else 0
        # Obtenemos el promedio de votaciones, o lo marcamos como "Desconocido" si es nulo
        vote_average = movie.iloc[0]['VOTE_AVERAGE'] if pd.notna(movie.iloc[0]['VOTE_AVERAGE']) else "Desconocido"
        
        # Obtenemos la fecha de estreno
        release_date = movie.iloc[0]['RELEASE_DATE']
        # Verificamos si la fecha de estreno no es nula
        if pd.notna(release_date):
            # Si la fecha de estreno es una cadena y tiene al menos 4 caracteres, extraemos el año
            if isinstance(release_date, str) and len(release_date) >= 4:
                release_year = release_date[:4]
            # Si la fecha de estreno es un objeto Timestamp, extraemos el año
            elif isinstance(release_date, pd.Timestamp):
                release_year = release_date.year
            # Si no se puede determinar el año, lo marcamos como "Desconocido"
            else:
                release_year = "Desconocido"
        else:
            # Si la fecha de estreno es nula, también la marcamos como "Desconocido"
            release_year = "Desconocido"
        
        # Si la película tiene al menos 2000 valoraciones, devolvemos los detalles
        if vote_count >= 2000:
            return {
                f"La película {titulo} fue estrenada en el año {release_year}. "
                f"La misma cuenta con un total de {vote_count} valoraciones, con un promedio de {vote_average}"
            }
        else:
            # Si no tiene al menos 2000 valoraciones, devolvemos un mensaje de error
            return {"Película no encontrada o menos de 2000 valoraciones"}
    
    # Si no se encuentra la película, devolvemos un mensaje indicando que no fue encontrada
    return {"Película no encontrada"}

@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor: str):
    # Buscamos en el DataFrame `cast_df` para encontrar las películas en las que ha participado el actor
    actor_movies = cast_df[cast_df['name'].str.contains(nombre_actor, case=False, na=False)]
    # Verificamos si el actor fue encontrado
    if not actor_movies.empty:
        # Obtenemos el ID del actor (asumimos que está en la columna 'id')
        actor_id = actor_movies['id'].iloc[0]
        # Filtramos el DataFrame `movies_df` para obtener las películas en las que el actor ha participado
        movies = movies_df[movies_df['ID'].isin(actor_movies['id'])]
        # Contamos el número total de películas en las que ha participado el actor
        total_movies = len(movies)
        # Calculamos la ganancia total de las películas
        total_return = movies['RETURN'].sum()  # Asumiendo que 'RETURN' se usa como retorno, puede necesitar ajuste
        # Calculamos la ganancia promedio de las películas
        avg_return = movies['RETURN'].mean()  # Asumiendo que 'RETURN' se usa como retorno, puede necesitar ajuste
        # Devolvemos un mensaje con el número de películas, el retorno total y el promedio de retorno
        return {f"El actor {nombre_actor} ha participado en {total_movies} películas, con un retorno total de {total_return} y un promedio de retorno de {avg_return}"}
    # Si no se encuentra el actor, devolvemos un mensaje indicando que no fue encontrado
    return {"Actor no encontrado"}

@app.get("/get_director/{nombre_director}")
async def get_director(nombre_director: str):
    # Buscamos en el DataFrame `crew_df` para encontrar las películas dirigidas por el director
    director_movies = crew_df[
        (crew_df['name'].str.contains(nombre_director, case=False, na=False)) &
        (crew_df['job'].str.lower() == 'director')
    ]
    # Verificamos si el director fue encontrado
    if not director_movies.empty:
        # Obtenemos el ID del director (asumimos que está en la columna 'id')
        director_id = director_movies['id'].iloc[0]
        # Filtramos el DataFrame `movies_df` para obtener las películas dirigidas por el director
        movies = movies_df[movies_df['ID'].isin(director_movies['id'])]
        # Seleccionamos la información relevante de las películas (título, fecha de estreno, popularidad, presupuesto, ganancia)
        movies_info = movies[['TITLE', 'RELEASE_DATE', 'POPULARITY', 'BUDGET', 'RETURN']]  # Asumiendo que 'RETURN' se usa como retorno, puede necesitar ajuste
        # Convertimos la información de las películas a un formato de diccionario para su retorno
        movies_list = movies_info.to_dict(orient='records')
        # Devolvemos un mensaje con la lista de películas dirigidas por el director
        return {f"El director {nombre_director} ha dirigido las siguientes películas: {movies_list}"}
    # Si no se encuentra el director, devolvemos un mensaje indicando que no fue encontrado
    return {"Director no encontrado"}