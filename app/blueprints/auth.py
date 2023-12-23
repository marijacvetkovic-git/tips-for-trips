import datetime
import uuid
from flask import Blueprint,render_template,jsonify,flash
from app import app , bcrypt, db ,ma
from gqlalchemy import match
from gqlalchemy.query_builders.memgraph_query_builder import Operator
from app.forms import LogInForm, RegistrationForm
from app.models import User
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
)



jwtM=JWTManager(app)
auth= Blueprint("auth",__name__,static_folder="static",template_folder="templates")

@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
            user=User(id=str(uuid.uuid4()),username=form.username.data,password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
                     email=form.email.data,dateOfBirth=form.date_of_birth.data,longitude=form.longitude.data,latitude=form.latitude.data)
            user.save(db)
           
            # flash(f'Your accound is now created, now you can log in and plan your next trip!','success')
            return jsonify({"username":user.username,"id":user.id})
    else :
        errors = {"errors": form.errors}
        return jsonify(errors), 400

        
   


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        users=(
          match()
          .node(labels="User",variable="u")
          .where(item="u.username",operator=Operator.EQUAL,literal=form.username.data)
          .return_(("u","user"))
          .execute()
          )
        listOfUsers=list(users)
        if not listOfUsers :
            flash('Login Unsuccessful. Please check username and password', 'danger')
        else: 
            
            user:User=(listOfUsers[0])['user']
            if not bcrypt.check_password_hash(user.password,form.password.data):
                flash('Login Unsuccessful. Please check username and password', 'danger')
            else:
                expires_delta = datetime.timedelta(minutes=60) 
                access_token = create_access_token(identity=user.username,expires_delta=expires_delta)
                refresh_token = create_refresh_token(identity=user.username)

        # access_token = create_access_token(identity=user_id, expires_delta=expires_delta, fresh=True, additional_claims={'roles': users[user_id]['roles']})
                return jsonify(
                {"access_token": access_token, "refresh_token": refresh_token}
            )
        
    return render_template('login.html', title='Login', form=form)