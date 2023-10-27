import datetime
from gqlalchemy import Node,Relationship, Field,match
from typing import Optional
from app import db,login_menager
from datetime import date, timedelta
from flask_login import UserMixin
from gqlalchemy.query_builders.memgraph_query_builder import Operator
@login_menager.user_loader
def load_user(user_id):
    users=(
          match()
          .node(labels="User",variable="u")
          .where(item="u.id",operator=Operator.EQUAL,literal=user_id)
          .return_(("u","user"))
          .execute()
          )
    return list(users)[0]["user"]

class User(Node,UserMixin):
    id:str = Field(index=True, unique=True, exists=True, db=db)
    username:str = Field(index=True, unique=True, exists=True, db=db)
    password:str = Field(exists=True,db=db)
    email:str = Field(unique=True, exists=True, db=db)
    dateOfBirth:date = Field(exists=True, db=db)
    latitude: float = Field(exists=True, db=db)
    longitude: float = Field(exists=True, db=db)
        
class Attraction(Node):
    id:str = Field(index=True, unique=True, exists=True, db=db)
    name:str=Field(index=True, unique=True, exists=True, db=db)
    latitude: float = Field(exists=True, db=db)
    longitude: float = Field(exists=True, db=db)
    description:str = Field(exists=True,db=db)
    familyFriendly:bool=Field(exists=True,db=db)
    # TODO: Vidi treba li exists true da bude
    durationOfVisit:timedelta=Field(exists=True,db=db)
    parking:bool=Field(exists=True,db=db)

class TypeOfAttraction(Node):
    id:str= Field(index=True, unique=True, exists=True, db=db)
    name:str= Field(index=True, unique=True, exists=True, db=db)
    
class Activities(Node):
    id:str= Field(index=True, unique=True, exists=True, db=db)
    name:str= Field(index=True, unique=True, exists=True, db=db)
   
class Likes(Relationship,type="LIKES"):
    dateAndTime:datetime = Field(exists=True, db=db)
    
class Visited(Relationship,type="VISITED"):
    dateAndTime:datetime = Field(exists=True, db=db)
    # TODO: Da li da se pamti rate ovde? ili da napravim klasu komentar i rate

class HasActivity(Relationship,type="HAS_ACTIVITY"):
    durationOfActivity:timedelta=Field(exists=True,db=db)
    experience:bool=Field(exists=True,db=db)
    minAge:int=Field(exists=True,db=db)
    maxAge:int=Field(exists=True,db=db)
    # TODO: Da li da se pamti min i max age ili samo d ali je za decu...jer sam gore napomenula u znamenitostima da ima samo d ali je family friendly..pod time mislice na decu
    

     

    


    

    