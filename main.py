from typing import List
from fastapi import FastAPI, HTTPException
from database import database as connection
from database import User, Movie, UserReview
from schemas import (
    UserRequestModel, 
    UserResponseModel,
    ReviewRequestModel,
    ReviewResponseModel,
    MovieRequestModel,
    MovieResponseModel,
    ReviewRequestPutModel
)

app = FastAPI(
    title="Proyecto para reseñar películas",
    description="API para reseñar películas",
    version="0.1.0"
)

@app.on_event("startup")
def startup_event():
    if connection.is_closed():
        connection.connect()
    print("-----Iniciando servidor...")
    print("-----Conectando a la db...")
    connection.create_tables([User, Movie, UserReview])
    print("-----Creando tablas en la db...")

@app.on_event("shutdown")
def shutdown_event():
    if not connection.is_closed():
        connection.close()
    print("-----Apagando servidor...")
    print("-----Cerrando la conexión a la db...")

@app.get("/")
async def index():
    return "Hola FastAPI desde mi primer servidor."

@app.post("/users", response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    if User.select().where(User.username == user.username).exists():
        raise HTTPException(status_code=409, detail='El nombre de usuario ya existe')
    
    hash_password = User.create_password_hash(user.password)
    
    user = User.create(
        username=user.username,
        password=hash_password
    )
    return user

@app.post("/reviews", response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):
    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code=404, detail='Usuario no encontrado')
    
    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail='Película no encontrada')
    
    user_review = UserReview.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score
    )
    return user_review

@app.post("/movies", response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):
    movie = Movie.create(
        title=movie.title
    )
    return movie

@app.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(page: int = 1, limit: int= 10):
    reviews = UserReview.select().paginate(page, limit) # select * from user_review
    return [review for review in reviews]

@app.get('/reviews/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail='Reseña no encontrada')
    return user_review    

@app.put('/reviews/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail='Reseña no encontrada')
    
    user_review.review = review_request.review
    user_review.score = review_request.score
    user_review.save()
    
    return user_review

@app.delete('/reviews/{review_id}', response_model=ReviewResponseModel)
async def delete_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail='Reseña no encontrada')
    
    user_review.delete_instance()
    #return {'message': 'Reseña eliminada exitosamente'}
    return user_review