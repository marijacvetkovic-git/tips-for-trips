
from ast import List
from collections import OrderedDict
import datetime
import random
import uuid
from click import DateTime
from flask import render_template,flash,redirect, url_for
from app import app , bcrypt, db
from app.forms import AddActivityForm, AddCityForm, AddHasActivityForm, AddHasHashForm, AddHashtagForm, AddVisitedForm, AddWantsToSeeForm, LogInForm, RegistrationForm,AddAttractionForm
from app.models import Activity, Attraction, City, HasActivity, HasHashtag, Hashtag, User, Visited, WantsToSee
from gqlalchemy.query_builders.memgraph_query_builder import Operator,Order
from gqlalchemy import match
from flask_login import login_user
import pandas as pd
import numpy as py
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist


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
        # query=f""" MATCH (a:Attraction)<-[r:VISITED]-() WHERE a.id='{form.idOfAttraction.data}'
        #            WITH a, AVG(r.rate) AS prosecnaOcena
        #            SET a.averageRate = prosecnaOcena;
        #            """
        # db.execute(query)
        flash(f'Your relationship is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addVisited.html', title='Add has hastag', form=form)  


@app.route("/createRelationship_WANTS_TO_SEE",methods=['GET','POST'])
def createRelationship_WANTS_TO_SEE():
    form = AddWantsToSeeForm()
    if form.validate_on_submit():
        WantsToSee(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1]).save(db)

        flash(f'Your relationship is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addWantsToSee.html', title='Add has hastag', form=form)
# DEO ZA RECOMMENDATION SYSTEM
# K-means clustering


def newUsercoldStartRecommendation(userId):
    #TODO: Poziva se prilikom registracije korisnika
    query=f""" MATCH (u:User)-[:WANTS_TO_SEE]->(h:Hashtag)<-[:HAS_HASHTAG]-(a:Attraction) WHERE u.id="{userId}"
    WITH a
    OPTIONAL MATCH (a)<-[r:VISITED]-(:User)
    WITH a, COALESCE(COLLECT(r.rate), [0]) AS ratings
    WITH a, REDUCE(s = 0, rating IN ratings | s + rating) AS sumRatings, SIZE(ratings) AS numRatings
    WITH a, 
        CASE WHEN numRatings > 0 THEN TOFLOAT(sumRatings) / TOFLOAT(numRatings) ELSE 0 END AS averageRating
    RETURN a.id
    ORDER BY averageRating DESC
    LIMIT 5 """
    result=list(db.execute_and_fetch(query))
    listOfAttributes = [item["a.id"] for item in result]
    query=f""" MATCH (u:User) WHERE u.id='{userId}'
                MATCH(a:Attraction) WHERE a.id IN {listOfAttributes}
                MERGE(a)-[r:RECOMMENDED_FOR]->(u) 
        """
    db.execute(query)
    
def recommend(userId):
    query=f""" MATCH (u:User)<-[r:RECOMMENDED_FOR]-(a:Attraction) WHERE u.id="{userId}"
    WITH a
    OPTIONAL MATCH (a)<-[r:VISITED]-(:User)
    WITH a, COALESCE(COLLECT(r.rate), [0]) AS ratings
    WITH a, REDUCE(s = 0, rating IN ratings | s + rating) AS sumRatings, SIZE(ratings) AS numRatings
    WITH a, 
        CASE WHEN numRatings > 0 THEN TOFLOAT(sumRatings) / TOFLOAT(numRatings) ELSE 0 END AS averageRating
    RETURN a
    ORDER BY averageRating DESC
    """
    result=list(db.execute_and_fetch(query))
    recommendAttractions=[item["a"] for item in result]
    return recommendAttractions
#TODO: Da li samo u atrakciji da cuvam prosecnu ocenu umesto da racunma ovo svaki put...ili da ostane ovako pa da uzmem pagerank da radim gde ce tezina grane rate da bude
    

def kMeansClustering(userId):
    
    hasHashtag=(
          match()
          .node(labels="Attraction",variable="a")
          .to(relationship_type="HAS_HASHTAG",variable="r")
          .node(labels="Hashtag",variable="h")
          .return_(results=["a.id","r","h.id"])
          .execute()
          )
    relationships=list(hasHashtag)
    dictioneryOfAttractionHashtags=dict()
    
    for item in relationships:
        idOfAttraction= item["a.id"]
        idOfHashTag=item["h.id"]
        
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
    userWantsToSee=(
            match()
            .node(labels="User",variable="u")
            .to(relationship_type="WANTS_TO_SEE",variable="r")
            .node(labels="Hashtag",variable="h")
            .where(item="u.id",operator=Operator.EQUAL,literal=userId)
            .return_(results=["h.id"])
            .execute()
    )
    listOfWantsToSee=[]
    for item in list(userWantsToSee):
        listOfWantsToSee.append(item["h.id"])
        
    userWantsToSee=[1 if hashtag in listOfWantsToSee else 0 for hashtag in listOfHashtags]
    vectors=list(dictioneryOfAttractionVector.values())
    vectors.append(userWantsToSee)
    x=py.array(vectors)
    print(x)
    wcss=[]
    distortions=[]
    for i in range(1,20):
        kmeans=KMeans(n_clusters=i,init='k-means++',random_state=0)
        print(kmeans.fit(x))
        wcss.append(kmeans.inertia_)
        distortions.append(sum(py.min(cdist(x, kmeans.cluster_centers_, 'euclidean'), axis=1)) / x.shape[0])
# da li umesto euclidean moze kosinusna da se ukljuci za k-means
    diff = py.diff(distortions, 2)
    elbow_point = py.argmax(diff) + 2
    #TODO: MOZDA DA SE PROMENI NACIN NALAZENJA ELBOW_POINTA
    
    kmeansmodel=KMeans(n_clusters=elbow_point,init='k-means++',random_state=0)
    y_kmeans= kmeansmodel.fit_predict(x)
    
    dictioneryAttractionIdCluster={}
    i=0
    for item in dictioneryOfAttractionVector:
        dictioneryAttractionIdCluster[item]=y_kmeans[i]
        i+=1
    return (dictioneryAttractionIdCluster,y_kmeans[len(y_kmeans)-1])
    
def recommendByUsingkMeansClustering():
    userId="9f130ecc-ab78-4d07-964a-1a38bc131675"

    (dictioneryAttractionIdCluster,clusterForUser) = kMeansClustering(userId)
    recommendAttractionId=[]
    for item in dictioneryAttractionIdCluster:
        if(dictioneryAttractionIdCluster[item]==clusterForUser):
            recommendAttractionId.append(item)
    query=f"""MATCH (a:Attraction) WHERE a.id IN {recommendAttractionId} RETURN a"""
    recommendAttraction=db.execute_and_fetch(query)
    recommendAttractionList:List(Attraction)=[]
    p=list(recommendAttraction)
    for item in p:
        recommendAttractionList.append(item["a"])
    print(recommendAttractionList)
    
def nearYouRecommendation():
    usersId="9f130ecc-ab78-4d07-964a-1a38bc131675"
    latitudeAndLongitudeOfTheUser=(
        match()
        .node(labels="User",variable="u")
        .where(item="u.id",operator=Operator.EQUAL,literal=usersId)
        .return_(["u.longitude","u.latitude"])
        .execute()
    )
  
    lista=list(latitudeAndLongitudeOfTheUser)
    usersLongitude=lista[0]["u.longitude"]
    usersLatitude=lista[0]["u.latitude"]
    
    
    query=f""" 
MATCH (a:Attraction)
WITH a,
    6371 * 2 * atan2(
        sqrt(
            sin((a.latitude - {usersLatitude}) * 3.14 / 360) * 
            sin((a.latitude - {usersLatitude}) * 3.14 / 360) +
            cos({usersLatitude} * 3.14 / 180) * 
            cos(a.latitude * 3.14 / 180) * 
            sin((a.longitude - {usersLongitude}) * 3.14 / 360) * 
            sin((a.longitude - {usersLongitude}) * 3.14 / 360)
        ),
        sqrt(
            1 - sin((a.latitude - {usersLatitude}) * 3.14 / 360) * 
            sin((a.latitude - {usersLatitude}) * 3.14 / 360) +
            cos({usersLatitude} * 3.14 / 180) * 
            cos(a.latitude * 3.14 / 180) * 
            sin((a.longitude - {usersLongitude}) * 3.14 / 360) * 
            sin((a.longitude - {usersLongitude}) * 3.14 / 360)
        )
    ) AS udaljenost
RETURN a, udaljenost
ORDER BY udaljenost
LIMIT 10;
 """
          
    fetchNearestAttractions=db.execute_and_fetch(query)
    
    listOfNearestAttractions=[]
    listaa=list(fetchNearestAttractions)
    print(listaa)
    for item in listaa:
        listOfNearestAttractions.append(item["a"])
    print(listOfNearestAttractions)


     
    
    
    
    
    

    
    
    
    
    
    
    
    
    
#dodavanjeAtrakcijaNaBrzinu ne radi zbog glupog vremena za durationOfVisit
def dodavanjeAtrakcijaNaBrzinu():
    attractions = [
    {"name": "Machu Picchu", "longitude": -72.5450, "latitude": -13.1631, "description": "Drevni Inka grad smešten na vrhu Anda."},
    {"name": "Eiffel Tower", "longitude": 2.2945, "latitude": 48.8588, "description": "Ikonična čelična kula u Parizu."},
    {"name": "Grand Canyon", "longitude": -112.1120, "latitude": 36.0551, "description": "Veliki kanjon u saveznoj državi Arizona."},
    {"name": "Great Barrier Reef", "longitude": 147.7167, "latitude": -18.2864, "description": "Svetski poznat koralni greben u Koralnom moru."},
    {"name": "Colosseum", "longitude": 12.4924, "latitude": 41.8902, "description": "Antički amfiteatar u Rimu."},
    {"name": "Petra", "longitude": 35.4444, "latitude": 30.3285, "description": "Arheološki lokalitet poznat po kamenim strukturama."},
    {"name": "Statue of Liberty", "longitude": -74.0445, "latitude": 40.6892, "description": "Simbol slobode u luci New Yorka."},
    {"name": "Serengeti National Park", "longitude": 34.9206, "latitude": -2.1540, "description": "Nacionalni park poznat po migraciji divljih životinja."},
    {"name": "Sydney Opera House", "longitude": 151.2140, "latitude": -33.8568, "description": "Ikonična operska kuća u Sidneju."},
    {"name": "Angkor Wat", "longitude": 103.8567, "latitude": 13.4125, "description": "Veliki hramski kompleks u Kambodži."},
    {"name": "Yellowstone National Park", "longitude": -110.5885, "latitude": 44.4279, "description": "Prvi nacionalni park na svetu."},
    {"name": "Acropolis", "longitude": 23.7263, "latitude": 37.9715, "description": "Stari grad na vrhu brda u Atini."},
    {"name": "Vatican City", "longitude": 12.4523, "latitude": 41.9022, "description": "Nezavisna država unutar Rima, dom Papina."},
    {"name": "Mount Everest", "longitude": 86.9250, "latitude": 27.9881, "description": "Najviša planina na svetu."},
    {"name": "Amazon Rainforest", "longitude": -62.8460, "latitude": -3.4653, "description": "Najveća prašuma na svetu."},
    {"name": "Stonehenge", "longitude": -1.8262, "latitude": 51.1789, "description": "Misteriozne kamene strukture u Engleskoj."},
    {"name": "Neuschwanstein Castle", "longitude": 10.7498, "latitude": 47.5576, "description": "Romantični dvorac izgrađen u 19. veku."},
    {"name": "Kyoto", "longitude": 135.7681, "latitude": 35.0116, "description": "Tradicionalni grad sa brojnim hramovima i baštama."},
]

    queries = []

    for attraction in attractions:
        unique_id = str(uuid.uuid4())
        family_friendly = random.choice([True, False])   
        parking = random.choice([True, False])           
        duration_of_visit = {
        "hour": random.randint(0, 5),
        "minute": random.randint(0, 59),
        "second": random.randint(0, 59),
        "nanosecond": 0
    }

        query = f""" MATCH(a:Attraction) WHERE a.name='{attraction['name']}' DELETE a """
        queries.append(query)

    for query in queries:
        db.execute(query)
        
def dodavanjeHashTagaoNaBrzinu():
    hashtags = [
    "TouristSpot",
    "BucketList",
    "AdventureAwaits",
    "DiscoverEarth",
    "MustSeePlaces",
    "WorldExplorer",
    "CulturalHeritage",
    "NatureEscape",
    "Landmarks",
    "TravelDreams",
    "BeautifulPlaces",
    "GlobalTourism",
    "HistoricSites",
    "NaturalWonders",
    "TourismAdventure",
    "Sightseeing",
    "JourneyOfDiscovery"]
    for hashtag in hashtags:
        unique_id = str(uuid.uuid4())
        query = f"""
    CREATE (:Hashtag {{
        id: '{unique_id}',
        name: '{hashtag}'
    }});
    """
        db.execute(query)
        
def dodavanjeAktivnostiNaBriznu():
    general_activities = [
    "Zabeležavanje trenutaka fotografijama",
    "Praktikovanje joge",
    "Isprobavanje internacionalnih recepata",
    "Slušanje podkasta ili muzike",
    "Vežbanje na otvorenom",
    "Meditacija radi opuštanja",
    "Piknik u prirodi",
    "Učestvovanje u uređenju zajedničkog vrta",
    "Igranje društvenih igara",
    "Planinarenje",
    "Kampovanje",
    "Biciklizam",
    "Planinarenje po prirodnim rezervatima",
    "Ribolov",
    "Kajak/kanu vožnja",
    "Penjanje na stene",
    "Picigin na plaži",
    "Vrtlarenje",
    "Orijentiring",
    "Frisbee golf",
    "Plivanje",]

    for activity in general_activities:
        unique_id = str(uuid.uuid4())
        query = f"""
        CREATE (:Activity {{
            id: '{unique_id}',
            name: '{activity}'
        }});
        """
        db.execute(query)
           
def dodavanjeHasHastagNaBriznu():
    
    dictionery={
        "Taj Mahal":["CulturalHeritage","Landmarks"],
        "Machu Picchu":["Istorija","DiscoverEarth","HistoricSites","JourneyOfDiscovery"],
        "Eiffel Tower":["Bucket List","MustSeePlaces","TravelDreams","GlobalTourism","Landmarks"],
        "Grand Canyon" :["Priroda","NatureEscape","Sightseeing"],
        "Great Barrier Reef" :["Priroda", "DiscoverEarth","MustSeePlaces","WorldExplorer","NatureEscape", "BeautifulPlaces","GlobalTourism","NaturalWonders","TourismAdventure","Sightseeing"],
        "Colosseum" :["HistoricSites","Landmarks","Sightseeing","CulturalHeritage","TravelDreams","MustSeePlaces","GlobalTourism","AdventureAwaits","JourneyOfDiscovery"],
        "Petra" :["Priroda","HistoricSites","Landmarks","Sightseeing","CulturalHeritage","TravelDreams","MustSeePlaces","GlobalTourism","AdventureAwaits","JourneyOfDiscovery"],
        "Statue of Liberty":["Landmarks","Spomenik","TouristSpot","MustSeePlaces"],
        "Serengeti National Park" :["Park","Priroda","AdventureAwaits","JourneyOfDiscover","NatureEscape"],
        "Sydney Opera House":["Zabava","Nocni zivot","BeautifulPlaces","GlobalTourism"],
        "Angkor Wat" :["Istorija","DiscoverEarth","HistoricSites","JourneyOfDiscovery","Priroda","HistoricSites","Landmarks","Sightseeing","CulturalHeritage","TravelDreams","MustSeePlaces"],
        "Yellowstone National Park":["Park","Priroda","AdventureAwaits","JourneyOfDiscover", "DiscoverEarth","MustSeePlaces","WorldExplorer","NatureEscape"],
        "Acropolis" :["Istorija","DiscoverEarth","HistoricSites","JourneyOfDiscovery","Landmarks","Sightseeing","CulturalHeritage"],
        "Vatican City" :["Istorija","DiscoverEarth","HistoricSites","JourneyOfDiscovery","Landmarks","Sightseeing","CulturalHeritage"],
        "Mount Everest" : ["Priroda","DiscoverEarth","JourneyOfDiscovery","NatureEscape"],
        "Amazon Rainforest": ["Priroda","DiscoverEarth","JourneyOfDiscovery","NatureEscape"],
        "Stonehenge": ["Landmarks","HistoricSites","Istorija","CulturalHeritage","AdventureAwaits","JourneyOfDiscovery"],
        "Neuschwanstein Castle": ["Dvorac","Istorija","CulturalHeritage","HistoricSites"],
        "Kyoto": ["Zabava","HistoricSites","JourneyOfDiscovery","MustSeePlaces","WorldExplorer"]
    }
    queries=[]
    for attraction in dictionery:
        for hashtag in dictionery[attraction]:
            query=f"""     
            MATCH (a:Attraction {{name: '{attraction}'}}), (h:Hashtag {{name: '{hashtag}'}})
            MERGE (a)-[:HAS_HASHTAG]->(h)
            """
            queries.append(query)
            
    
    for query in queries:
        db.execute(query)

def dodavanjeVisited():
    dictionery={
        
        'maruuja_c'	
        'ana_c'
        'peca_cvetkovic'
	    'stejsaa'
        'kata'	
        'bazlooka'
        'mixzzz'	
        'tqic'
        'savov'
        'jeca'
        'bici'	
        'mikica'
        'pistac'
        'daca'
        'acko_nikolic'
        'isa00'
        'micika00'	
        'kacica00'
        'ema_dj'
        'mara_trajkovic'
        'jojaa'
    }