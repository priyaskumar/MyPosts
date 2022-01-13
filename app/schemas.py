from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

from sqlalchemy.sql.functions import user

# a schema/pydantic model -> defines the structure of the request 
#                          sent from server to fastapi (posts)
class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True

# extends PostBase class
# defines the structure of the details of the new post 
class PostCreate(PostBase):
    pass

# defines the structure of the response(user details) sent from fastapi to server
class User(BaseModel):
    email: EmailStr
    id : int
    created_at : datetime

    class Config:
        orm_mode = True

# defines the structure of the response (post details) sent from fastapi to server 
class Post(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : User

    # converts a sqlalchemy model to the pydantic model
    # basically reads the data if it is not a dict, but an ORM model
    # Note : pydantic models read only dict 
    class Config:
        orm_mode = True

# defines the structure of the response (post details) sent from fastapi to server 
class PostOut(BaseModel):
    Post : Post
    votes : int

    # converts a sqlalchemy model to the pydantic model
    # basically reads the data if it is not a dict, but an ORM model
    # Note : pydantic models read only dict 
    class Config:
        orm_mode = True

# a schema/pydantic model -> defines the structure of the request 
#                          sent from server to fastapi (creating new users)
class UserCreate(BaseModel):
    email: EmailStr
    password:str
    


# defines the structure of the request (user details) sent to fastapi from server
class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
# defines the structure of the request (token sent by the user) sent to fastapi
class Token(BaseModel):
    access_token : str
    token_type : str

# defines the structure of the data embedded into the access_token
class TokenData(BaseModel):
    id : Optional[str] = None

# defines the structure of the request (vote details) sent to fastapi from server
class Vote(BaseModel):
    post_id : int
    dir : conint(le=1)
    

    