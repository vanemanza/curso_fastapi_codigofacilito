# conexion al proyecto y nuestra db
import hashlib 

from peewee import *

from datetime import datetime


# mediante argumentos y parametros establecemos la conexion a la db
# usando la clase PostgresqlDatabase de peewee

# Configuración de la base de datos
DATABASE_NAME = 'fastapi_project'
DATABASE_USER = 'postgres'
DATABASE_PASSWORD = 'postgres'
DATABASE_HOST = 'localhost'  
DATABASE_PORT = 5432  

# Configurar la conexión a la base de datos
database = PostgresqlDatabase(
    DATABASE_NAME,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    host=DATABASE_HOST,
    port=DATABASE_PORT,
)

class User(Model):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.username
    
    @classmethod
    def create_password_hash(cls, password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))
        return h.hexdigest() 
    
    class Meta:
        database = database
        table_name = 'users'        
        
        
class Movie(Model):
    title = CharField(max_length=50)   
    created_at = DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.title
    
    class Meta:
        database = database
        table_name = 'movies'
        
class UserReview(Model):
    user = ForeignKeyField(User, backref='reviews')
    movie = ForeignKeyField(Movie, backref='reviews')
    review = TextField()
    score = IntegerField()
    created_at = DateTimeField(default=datetime.now)
    
    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'
    
    class Meta:
        database = database
        table_name = 'users_reviews'
        
        