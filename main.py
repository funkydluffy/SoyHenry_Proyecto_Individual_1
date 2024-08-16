from fastapi import FastAPI, HTTPException
from typing import Optional
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar los datasets
movies_df = pd.read_csv('movies_reducido.csv')
cast_df = pd.read_csv('df_cast_expanded.csv')
crew_df = pd.read_csv('filtered_credits_crew.csv')
df_movies_released = pd.read_csv('movies_released.csv')

app = FastAPI()

# Convertir las columnas de texto a minúsculas para uniformidad
df_movies_released['TITLE'] = df_movies_released['TITLE'].str.lower()
df_movies_released['GENRES_NAME'] = df_movies_released['GENRES_NAME'].str.lower()
df_movies_released['ORIGINAL_LANGUAGE'] = df_movies_released['ORIGINAL_LANGUAGE'].str.lower()
df_movies_released['PRODUCTION_COUNTRIES_NAME'] = df_movies_released['PRODUCTION_COUNTRIES_NAME'].str.lower()

# Crear una columna que combine todas las características relevantes para la recomendación
df_movies_released['combined_features'] = df_movies_released.apply(
    lambda row: f"{row['REVENUE']} {row['BUDGET']} {row['RETURN']} {row['TITLE']} {row['GENRES_NAME']} {row['ORIGINAL_LANGUAGE']} {row['PRODUCTION_COUNTRIES_NAME']} {row['VOTE_AVERAGE']}",
    axis=1
)

# Vectorizar las características combinadas usando TfidfVectorizer
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(df_movies_released['combined_features'])

@app.get("/recomendacion/{titulo}")
async def recomendacion(titulo: str, num_recommendations: int = 5):
    # Convertir el título a minúsculas para uniformidad
    titulo = titulo.lower()

    # Encontrar el índice de la película dada
    try:
        movie_idx = df_movies_released[df_movies_released['TITLE'] == titulo].index[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="La película no fue encontrada en la base de datos")

    # Calcular la similitud del coseno entre la película dada y todas las demás
    cosine_similarities = cosine_similarity(feature_vectors[movie_idx], feature_vectors).flatten()

    # Obtener los índices de las películas más similares, excluyendo la película dada
    similar_indices = cosine_similarities.argsort()[-num_recommendations-1:-1][::-1]

    # Obtener los títulos de las películas recomendadas
    similar_movies = df_movies_released.iloc[similar_indices]['TITLE'].tolist()

    return {"message": f"Películas recomendadas similares a {titulo}: {similar_movies}"}

@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes: str):
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    mes_num = meses.get(mes.lower())
    if not mes_num:
        raise HTTPException(status_code=400, detail="Mes no válido")
    
    try:
        # Filtrar películas por el mes
        movies_df['RELEASE_DATE'] = pd.to_datetime(movies_df['RELEASE_DATE'], errors='coerce')
        count = movies_df[movies_df['RELEASE_DATE'].dt.month == mes_num].shape[0]
        return {"message": f"{count} películas fueron estrenadas en el mes de {mes.capitalize()}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al procesar la solicitud")
    
@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia: str):
    dias = {
        "lunes": "monday", "martes": "tuesday", "miércoles": "wednesday", 
        "jueves": "thursday", "viernes": "friday", "sábado": "saturday", 
        "domingo": "sunday"
    }
    dia_en = dias.get(dia.lower())
    
    if dia_en is not None:
        # Asegurarse de que RELEASE_DATE es de tipo datetime
        movies_df['RELEASE_DATE'] = pd.to_datetime(movies_df['RELEASE_DATE'], errors='coerce')

        # Extraer el día de la semana de las fechas de estreno
        movies_df['day_of_week'] = movies_df['RELEASE_DATE'].dt.day_name().str.lower()

        # Contar las películas estrenadas en el día de la semana solicitado
        count = movies_df[movies_df['day_of_week'] == dia_en].shape[0]
        return {"message": f"{count} películas fueron estrenadas en los días {dia.capitalize()}"}
    
    return {"message": "Día no válido"}

@app.get("/score_titulo/{titulo}")
async def score_titulo(titulo: str):
    movie = movies_df[movies_df['TITLE'].str.contains(titulo, case=False, na=False)]
    if not movie.empty:
        release_date = movie.iloc[0]['RELEASE_DATE']
        # Verificar si RELEASE_DATE no es nulo y manejar datetime o string adecuadamente
        if pd.notna(release_date):
            if isinstance(release_date, str) and len(release_date) >= 4:
                release_year = release_date[:4]
            elif isinstance(release_date, pd.Timestamp):
                release_year = release_date.year
            else:
                release_year = "Desconocido"
        else:
            release_year = "Desconocido"
        
        popularity = movie.iloc[0]['POPULARITY'] if pd.notna(movie.iloc[0]['POPULARITY']) else "Desconocido"
        
        return {
            "message": f"La película {titulo} fue estrenada en el año {release_year} con un score/popularidad de {popularity}"
        }
    
    return {"message": "Película no encontrada"}

@app.get("/votos_titulo/{titulo}")
async def votos_titulo(titulo: str):
    movie = movies_df[movies_df['TITLE'].str.contains(titulo, case=False, na=False)]
    if not movie.empty:
        vote_count = movie.iloc[0]['VOTE_COUNT'] if pd.notna(movie.iloc[0]['VOTE_COUNT']) else 0
        vote_average = movie.iloc[0]['VOTE_AVERAGE'] if pd.notna(movie.iloc[0]['VOTE_AVERAGE']) else "Desconocido"
        
        release_date = movie.iloc[0]['RELEASE_DATE']
        if pd.notna(release_date):
            if isinstance(release_date, str) and len(release_date) >= 4:
                release_year = release_date[:4]
            elif isinstance(release_date, pd.Timestamp):
                release_year = release_date.year
            else:
                release_year = "Desconocido"
        else:
            release_year = "Desconocido"
        
        if vote_count >= 2000:
            return {
                "message": f"La película {titulo} fue estrenada en el año {release_year}. "
                           f"La misma cuenta con un total de {vote_count} valoraciones, con un promedio de {vote_average}"
            }
        else:
            return {"message": "Película no encontrada o menos de 2000 valoraciones"}
    
    return {"message": "Película no encontrada"}
@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor: str):
    # Buscar en cast_df para obtener los datos del actor
    actor_movies = cast_df[cast_df['name'].str.contains(nombre_actor, case=False, na=False)]
    if not actor_movies.empty:
        actor_id = actor_movies['id'].iloc[0]
        movies = movies_df[movies_df['ID'].isin(actor_movies['id'])]
        total_movies = len(movies)
        total_return = movies['RETURN'].sum()  # Asumiendo que 'RETURN' se usa como retorno, puede necesitar ajuste
        avg_return = movies['RETURN'].mean()  # Asumiendo que 'RETURN' se usa como retorno, puede necesitar ajuste
        return {"message": f"El actor {nombre_actor} ha participado en {total_movies} películas, con un retorno total de {total_return} y un promedio de retorno de {avg_return}"}
    return {"message": "Actor no encontrado"}

@app.get("/get_director/{nombre_director}")
async def get_director(nombre_director: str):
    # Buscar en crew_df para obtener los datos del director
    director_movies = crew_df[
        (crew_df['name'].str.contains(nombre_director, case=False, na=False)) &
        (crew_df['job'].str.lower() == 'director')
    ]
    if not director_movies.empty:
        director_id = director_movies['id'].iloc[0]
        movies = movies_df[movies_df['ID'].isin(director_movies['id'])]
        movies_info = movies[['TITLE', 'RELEASE_DATE', 'POPULARITY', 'BUDGET', 'RETURN']]  # Asumiendo que 'RETURN' se usa como retorno, puede necesitar ajuste
        movies_list = movies_info.to_dict(orient='records')
        return {"message": f"El director {nombre_director} ha dirigido las siguientes películas:", "movies": movies_list}
    return {"message": "Director no encontrado"}