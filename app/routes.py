
import uuid
from flask import render_template,flash,redirect, url_for
from app import app , bcrypt, db
from app.forms import ActivityCreateForm, LogInForm, RegistrationForm,AttractionCreateForm,TypeOfAttractionCreateForm
from app.models import Activity, Attraction, TypeOfAttraction, User
from gqlalchemy.query_builders.memgraph_query_builder import Operator
from gqlalchemy import match
from flask_login import login_user

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
            user=User(id=str(uuid.uuid4()),username=form.username.data,password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
                     email=form.email.data,dateOfBirth=form.date_of_birth.data,longitude=form.longitude.data,latitude=form.latitude.data)
            user.save(db)

            flash(f'Your accound is now created, now you can log in and plan your next trip!','success')
            return redirect(url_for('login'))
        
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
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
                login_user(user,remember=form.remember.data)
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
        
    return render_template('login.html', title='Login', form=form)

@app.route("/createAttraction",methods=['GET','POST'])
def createAttraction():
    form= AttractionCreateForm()
    if form.validate_on_submit():
        attraction=Attraction(id=str(uuid.uuid4()),name=form.name.data,description=form.description.data,longitude=form.longitude.data,latitude=form.latitude.data,familyFriendly=form.family_friendly.data,parking=form.parking.data,durationOfVisit=form.duration_of_visit.data)
        attraction.save(db)

        flash(f'Your attraction is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addAttraction.html', title='Add attraction', form=form)

@app.route("/createTypeOfAttraction",methods=['GET','POST'])
def createTypeOfAttraction():
    form = TypeOfAttractionCreateForm()
    if form.validate_on_submit():
        typeOfAttraction=TypeOfAttraction(id=str(uuid.uuid4()),name=form.name.data)
        typeOfAttraction.save(db)

        flash(f'Your type of attraction is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addTypeOfAttraction.html', title='Add type of attraction', form=form)
    
@app.route("/createActivity",methods=['GET','POST'])
def createActivity():
    form = ActivityCreateForm()
    if form.validate_on_submit():
        activity=Activity(id=str(uuid.uuid4()),name=form.name.data)
        activity.save(db)

        flash(f'Your activity is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addActivity.html', title='Add activity', form=form)
    
  
    
    
    