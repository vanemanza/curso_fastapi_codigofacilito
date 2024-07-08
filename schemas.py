from typing import Any                                            
from pydantic import BaseModel, ConfigDict, field_validator
from peewee import ModelSelect
from pydantic.v1.utils import GetterDict

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        return res
            
class ResponseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        getter_dict=PeeweeGetterDict
    )

# ---------- User Schemas ----------           

class UserRequestModel(BaseModel):
    username: str
    password: str
    
    @field_validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('Username must be between 3 and 50 characters')
        return username
    
class UserResponseModel(ResponseModel):
    id: int
    username: str   
    
# ---------- Movie Schemas ----------  
        
class MovieRequestModel(BaseModel):
    title: str
        

class MovieResponseModel(ResponseModel):
    id: int
    title: str    
    
# ---------- Review Schemas ----------      

class ReviewRequestModel(BaseModel):
    user_id: int
    movie_id: int
    review: str
    score: int   
    
    @field_validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError('El puntaje debe ser entre 1 y 5')
        return score
    
    
class ReviewResponseModel(ResponseModel):
    id: int
    movie: MovieResponseModel    
    review: str
    score: int    
    
class ReviewRequestPutModel(BaseModel):
    review: str 
    score: int   
    
    @field_validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError('El puntaje debe ser entre 1 y 5')
        return score
