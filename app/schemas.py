from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# SCHEMA
# Pydantic from base model
# Decorater specifies it's an API  "/" is the path
#  Order matterns in the way that first path is it 


class User(BaseModel): 
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    createdAt: datetime
    
    class Config:
        orm_model = True
        
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    
    
class PostBase(BaseModel): 
    title: str
    content: str 
    published: bool = True

class PostCreate(PostBase):
    # Will have all attributes of PostBase
    pass

# class PostUpdate(PostBase):

class Post(PostBase):
    # title: str
    # content: str
    # published: bool
    owner: UserOut
    id: int
    createdAt: datetime
    owner_id: int 
    
    class Config:
        orm_model = True
        
        # Saying that it can be a orm model

class Token(BaseModel):
    access_token: str
    token_type: str 
    
class TokenData(BaseModel):
    id : Optional[str] = None
    
class Vote(BaseModel):
    post_id: int 
    dir: bool
    
class PostOut(BaseModel):
    Post: Post
    votes: int 
    
    class Config:
        orm_model = True