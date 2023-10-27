from datetime import date
from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, StringField,PasswordField,SubmitField,DateField, ValidationError,TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app import db
from gqlalchemy import match
from gqlalchemy.query_builders.memgraph_query_builder import Operator

class RegistrationForm(FlaskForm):
          
    username=StringField('Username', validators=[DataRequired(),Length(min=2,max=50)])
    email= StringField('Email', validators=[DataRequired(), Email()] )
    password= PasswordField('Password', validators=[DataRequired()])
    confirm_password=PasswordField('Confirm password', validators=[DataRequired(),EqualTo('password')])
    date_of_birth=DateField('Date of Birth', validators=[DataRequired()])
    longitude=FloatField('Longitude', validators=[DataRequired()])
    latitude=FloatField('Latitude', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
  
    def validate_username(self,username):
        users=db.execute_and_fetch(
        "MATCH (u:User {username: $username}) RETURN u.username ;",
       {"username": username.data}
        )
        
        if list(users):
            raise ValidationError('User with specific username already exist')
        
    def validate_email(self,email):
        users= db.execute_and_fetch(
        "MATCH (u:User {email: $email}) RETURN u",
        {"email":email.data})
        if list(users):
            raise ValidationError('User with specific email already exist')
    
    def validate_date_of_birth(form, field):
        min_date = date.min
        max_date = date.today()
        if field.data < min_date or field.data > max_date:
           raise ValidationError('The date of birth must not be in the future.')
    
class LogInForm(FlaskForm):
    
    username=StringField('Username', validators=[DataRequired(),Length(min=2,max=50)])
    password= PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')
    
class AttractionCreateForm(FlaskForm):
    def validate_longitude(formica,l):
        p=formica.longitude.data
        l=formica.latitude.data
        attractions=(
          match()
          .node(labels="Attraction",variable="a")
          .where(item="a.longitude",operator=Operator.EQUAL,literal=formica.longitude.data)
          .and_where(item="a.latitude",operator=Operator.EQUAL,literal=formica.latitude.data)
          .return_(("a","attraction"))
          .execute()
          )
        listOfAttractions=list(attractions)
        if listOfAttractions:
            raise ValidationError('Some attraction already exists at that location') 
            
    name=StringField('Name', validators=[DataRequired()])
    description= StringField('Description', validators=[DataRequired()])
    longitude=FloatField('Longitude', validators=[DataRequired(),validate_longitude])
    latitude=FloatField('Latitude', validators=[DataRequired(),validate_longitude])
    duration_of_visit=TimeField('Duration of visit', validators=[DataRequired()])
    parking=BooleanField("Parking")
    family_friendly=BooleanField("Family friendly")
    submit = SubmitField('Add')
    
class TypeOfAttractionCreateForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add')
    
    def validate_name(self,name): 
        n=name    
        typeOfAttractions=(
          match()
          .node(labels="TypeOfAttraction",variable="a")
          .where(item="a.name",operator=Operator.EQUAL,literal=name.data)
          .return_(("a","typeOfAttraction"))
          .execute()
          )
        listOftypeOfAttractions=list(typeOfAttractions)
        if listOftypeOfAttractions:
            raise ValidationError('Type of attraction with that name already exists !')
  

class ActivityCreateForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add')
    
    def validate_name(self,name): 
        n=name    
        activities=(
          match()
          .node(labels="Activity",variable="a")
          .where(item="a.name",operator=Operator.EQUAL,literal=name.data)
          .return_(("a","activity"))
          .execute()
          )
        listOfactivities=list(activities)
        if listOfactivities:
            raise ValidationError('Activity with that name already exists !')
  

        
