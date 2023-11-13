
from ast import List
import datetime
import uuid
from click import DateTime
from flask import render_template,flash,redirect, url_for
from app import app , bcrypt, db
from app.forms import AddActivityForm, AddCityForm, AddHasActivityForm, AddHasHashForm, AddHashtagForm, AddVisitedForm, LogInForm, RegistrationForm,AddAttractionForm
from app.models import Activity, Attraction, City, HasActivity, HasHashtag, Hashtag, User, Visited
from gqlalchemy.query_builders.memgraph_query_builder import Operator
from gqlalchemy import match
from flask_login import login_user
import pandas as pd
import numpy as py
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans


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

@app.route("/addAttraction",methods=['GET','POST'])
def addAttraction():
    form= AddAttractionForm()
    if form.validate_on_submit():
        attraction=Attraction(id=str(uuid.uuid4()),name=form.name.data,description=form.description.data,longitude=form.longitude.data,latitude=form.latitude.data,familyFriendly=form.family_friendly.data,parking=form.parking.data,durationOfVisit=form.duration_of_visit.data)
        attraction.save(db)

        flash(f'Your attraction is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addAttraction.html', title='Add attraction', form=form)

@app.route("/createHashtag",methods=['GET','POST'])
def createHashtag():
    form = AddHashtagForm()
    if form.validate_on_submit():
        hashtag=Hashtag(id=str(uuid.uuid4()),name=form.name.data)
        hashtag.save(db)

        flash(f'Your type of attraction is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addHashtag.html', title='Add hashtag', form=form)
    
@app.route("/createActivity",methods=['GET','POST'])
def createActivity():
    form = AddActivityForm()
    if form.validate_on_submit():
        activity=Activity(id=str(uuid.uuid4()),name=form.name.data)
        activity.save(db)

        flash(f'Your activity is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addActivity.html', title='Add activity', form=form)

@app.route("/createCity",methods=['GET','POST'])
def createCity():
    form = AddCityForm()
    if form.validate_on_submit():
        city=City(id=str(uuid.uuid4()),name=form.name.data,description=form.description.data)
        city.save(db)

        flash(f'Your city is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addCity.html', title='Add city', form=form)

@app.route("/createRelationship_HAS_HASHTAG",methods=['GET','POST'])
def createRelationship_HAS_HASHTAG():
    form = AddHasHashForm()
    m=form.validate_on_submit()
    if m:
        
        HasHashtag(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1]).save(db)

        flash(f'Your relationship is added!','success')
        return redirect(url_for('createRelationship_HAS_HASHTAG'))
    
    
    return render_template('addHashashtag.html', title='Add has hastag', form=form)

@app.route("/createRelationship_HAS_ACTIVITY",methods=['GET','POST'])
def createRelationship_HAS_ACTIVITY():
    form = AddHasActivityForm()
    if form.validate_on_submit():
        HasActivity(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1],durationOfActivity=form.duration_of_activity.data,experience=form.experience.data,minAge=form.minAge.data,maxAge=form.maxAge.data).save(db)

        flash(f'Your relationship is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addHasActivity.html', title='Add has hastag', form=form)  

@app.route("/createRelationship_VISITED",methods=['GET','POST'])
def createRelationship_VISITED():
    form = AddVisitedForm()
    if form.validate_on_submit():
        Visited(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1],rate=form.rate.data,dateAndTime=datetime.datetime.now()).save(db)

        flash(f'Your relationship is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addVisited.html', title='Add has hastag', form=form)  

# DEO ZA RECOMMENDATION SYSTEM
# K-means clustering


def proba():
    
    hasHashtag=(
          match()
          .node(labels="Attraction",variable="a")
          .to(relationship_type="HAS_HASHTAG",variable="r")
          .node(labels="Hashtag",variable="h")
          .return_(results=["a","r","h"])
          .execute()
          )
    
    relationships=list(hasHashtag)
    dictioneryOfAttractionHashtags=dict()
    
    for item in relationships:
        attraction:Attraction=item["a"]
        hashtag:Hashtag=item["h"]
        idOfAttraction= attraction.id
        idOfHashTag=hashtag.id
        
        if idOfAttraction not in dictioneryOfAttractionHashtags:
            lista:List=[]
            dictioneryOfAttractionHashtags[idOfAttraction]=lista
        dictioneryOfAttractionHashtags[idOfAttraction].append(idOfHashTag)

    
    hashtags=(
          match()
          .node(labels="Hashtag",variable="hashtag")
          .return_()
          .execute()
          )
    
    listOfHashtags=[]
    for item in hashtags:
        listOfHashtags.append(item["hashtag"].id)
   
    dictioneryOfAttractionVector=dict()
    for attraction in dictioneryOfAttractionHashtags:
        dictioneryOfAttractionVector[attraction]=[1 if hashtag in dictioneryOfAttractionHashtags[attraction] else 0 for hashtag in listOfHashtags]
        
    
    x=py.array(list(dictioneryOfAttractionVector.values()))
    print(x)
    wcss=[]
    for i in range(1,20):
        kmeans=KMeans(n_clusters=i,init='k-means++',random_state=0)
        print(kmeans.fit(x))
        wcss.append(kmeans.inertia_)
    plt.plot(range(1,20),wcss)
    plt.title("The elbow method")
    plt.xlabel("Number of clusters")
    plt.ylabel("WCSS values")
    plt.show()
    
    kmeansmodel=KMeans(n_clusters=5,init='k-means++',random_state=0)
    y_kmeans= kmeansmodel.fit_predict(x)



proba()