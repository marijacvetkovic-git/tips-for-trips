from gqlalchemy import Node,Relationship, Field
from typing import Optional
from app import db
from datetime import date
class User(Node):
    id:str = Field(index=True, unique=True, exists=True, db=db)
    username:str = Field(index=True, unique=True, exists=True, db=db)
    password:str = Field(exists=True,db=db)
    email:str = Field(unique=True, exists=True, db=db)
    dateOfBirth:date = Field(exists=True, db=db)
    latitude: float = Field(exists=True, db=db)
    longitude: float = Field(exists=True, db=db)
        