from datetime import date
from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, StringField,PasswordField,SubmitField,DateField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app import db
from gqlalchemy import connection




class RegistrationForm(FlaskForm):
    
    def validate_date_range(form, field):
        min_date = date.min
        max_date = date.today()
        if field.data < min_date or field.data > max_date:
           raise ValidationError('The date of birth must not be in the future.')
        
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
    
    
