from gqlalchemy import Node,Relationship, Field,match
from typing import Optional
from app import db,login_menager
from datetime import date
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
        