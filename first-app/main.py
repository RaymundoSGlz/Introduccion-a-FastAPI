from fastapi import Body, FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()
app.title = "My First App with FastAPI"
app.version = "0.0.1"

# Lista con movies
movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Aventura",
    },
    {
        "id": 2,
        "title": "Avengers: Endgame",
        "overview": "Después de los eventos devastadores de Avengers: Infinity War, el universo ...",
        "year": "2019",
        "rating": 8.4,
        "category": "Acción",
    },
]


# Podemos agregar tags para agrupar endpoints
@app.get("/", tags=["home"])
def message():
    return HTMLResponse(
        """
        <h1>Welcome to my first app with FastAPI</h1>
    """
    )


@app.get("/movies", tags=["movies"])
def get_movies():
    return movies


# get con path params
@app.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: int):
    movie = None
    for m in movies:
        if m["id"] == movie_id:
            movie = m
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


# get con query params
@app.get("/movies/", tags=["movies"])
def get_movies_by_category(category: str, year: int = None):
    movies_by_category = []
    for m in movies:
        if m["category"] == category:
            if year is None:
                movies_by_category.append(m)
            elif m["year"] == str(year):
                movies_by_category.append(m)
    if len(movies_by_category) == 0:
        raise HTTPException(status_code=404, detail="Movies not found")
    return movies_by_category


# post con body
@app.post("/movies", tags=["movies"])
def create_movie(
    id: int = Body(),
    title: str = Body(),
    overview: str = Body(),
    year: str = Body(),
    rating: float = Body(),
    category: str = Body(),
):
    movie = {
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category,
    }
    movies.append(movie)
    return movies


# put con body
@app.put("/movies/{movie_id}", tags=["movies"])
def update_movie(
    movie_id: int,
    title: str = Body(),
    overview: str = Body(),
    year: str = Body(),
    rating: float = Body(),
    category: str = Body(),
):
    movie = None
    for m in movies:
        if m["id"] == movie_id:
            movie = m
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie["title"] = title
    movie["overview"] = overview
    movie["year"] = year
    movie["rating"] = rating
    movie["category"] = category
    return movie


# delete con path params
@app.delete("/movies/{movie_id}", tags=["movies"])
def delete_movie(movie_id: int):
    movie = None
    for m in movies:
        if m["id"] == movie_id:
            movie = m
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    movies.remove(movie)
    return movies
