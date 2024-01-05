
import datetime
import random
import sys
import uuid
from flask import jsonify, render_template,flash,redirect, url_for
from app import app , bcrypt, db ,ma
from app.blueprints.auth import auth
from app.blueprints.admin import admin
from app.blueprints.user import user
from app.blueprints.helpers import helpers

from app.forms import AddActivityForm, AddCityForm, AddHasActivityForm, AddHasAttractionForm, AddHasHashForm, AddHashtagForm, AddVisitedForm, AddWantsToSeeForm, LogInForm, RegistrationForm,AddAttractionForm
from app.models import Activity, Attraction, City, HasActivity, HasAttraction, HasHashtag, Hashtag, User, Visited, WantsToSee
from gqlalchemy.query_builders.memgraph_query_builder import Operator
from gqlalchemy import match
# from auth import auth
# from admin import admin
# from user import user
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
)

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

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(helpers,url_prefix='/helpers')
# class AttractionSchema(ma.Schema):
#     class Meta:
#         fields = ('id','name','latitude','longitude','description','familyFriendly','durationOfVisit','parking','averageRate')
  
# attraction_schema = AttractionSchema()
# attractions_schema = AttractionSchema(many=True)
  


# @app.route("/")
# @app.route("/home")
# def home():
#     return render_template('home.html', posts=posts)


# @app.route("/about")
# def about():
#     return render_template('about.html', title='About')


# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#             user=User(id=str(uuid.uuid4()),username=form.username.data,password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
#                      email=form.email.data,dateOfBirth=form.date_of_birth.data,longitude=form.longitude.data,latitude=form.latitude.data)
#             user.save(db)
           
#             # flash(f'Your accound is now created, now you can log in and plan your next trip!','success')
#             return jsonify({"username":user.username,"id":user.id})
#     else :
#         errors = {"errors": form.errors}
#         return jsonify(errors), 400

        
   


# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     form = LogInForm()
#     if form.validate_on_submit():
#         users=(
#           match()
#           .node(labels="User",variable="u")
#           .where(item="u.username",operator=Operator.EQUAL,literal=form.username.data)
#           .return_(("u","user"))
#           .execute()
#           )
#         listOfUsers=list(users)
#         if not listOfUsers :
#             flash('Login Unsuccessful. Please check username and password', 'danger')
#         else: 
            
#             user:User=(listOfUsers[0])['user']
#             if not bcrypt.check_password_hash(user.password,form.password.data):
#                 flash('Login Unsuccessful. Please check username and password', 'danger')
#             else:
#                 expires_delta = datetime.timedelta(minutes=60)  # Token važi 15 minuta
#                 access_token = create_access_token(identity=user.username,expires_delta=expires_delta)
#                 refresh_token = create_refresh_token(identity=user.username)

#         # access_token = create_access_token(identity=user_id, expires_delta=expires_delta, fresh=True, additional_claims={'roles': users[user_id]['roles']})
#                 return jsonify(
#                 {"access_token": access_token, "refresh_token": refresh_token}
#             )
        
#     return render_template('login.html', title='Login', form=form)



# @app.route("/addAttraction",methods=['GET','POST'])
# @jwt_required()

# def addAttraction():
#     form= AddAttractionForm()
#     if form.validate_on_submit():
#         attraction=Attraction(id=str(uuid.uuid4()),name=form.name.data,description=form.description.data,longitude=form.longitude.data,latitude=form.latitude.data,familyFriendly=form.family_friendly.data,parking=form.parking.data,durationOfVisit=form.duration_of_visit.data)
#         attraction.save(db)

#         flash(f'Your attraction is added!','success')
#         return redirect(url_for('home'))
    
    
#     return render_template('addAttraction.html', title='Add attraction', form=form)

# @app.route("/createHashtag",methods=['GET','POST'])
# @jwt_required()

# def createHashtag():
#     form = AddHashtagForm()
#     if form.validate_on_submit():
#         hashtag=Hashtag(id=str(uuid.uuid4()),name=form.name.data)
#         hashtag.save(db)

#         flash(f'Your type of attraction is added!','success')
#         return redirect(url_for('home'))
    
    
#     return render_template('addHashtag.html', title='Add hashtag', form=form)
    
# @app.route("/createActivity",methods=['GET','POST'])
# @jwt_required()

# def createActivity():
#     form = AddActivityForm()
#     if form.validate_on_submit():
#         activity=Activity(id=str(uuid.uuid4()),name=form.name.data)
#         activity.save(db)

#         flash(f'Your activity is added!','success')
#         return redirect(url_for('home'))
    
    
#     return render_template('addActivity.html', title='Add activity', form=form)

# @app.route("/createCity",methods=['GET','POST'])
# @jwt_required()

# def createCity():
#     form = AddCityForm()
#     if form.validate_on_submit():
#         city=City(id=str(uuid.uuid4()),name=form.name.data,description=form.description.data)
#         city.save(db)

#         flash(f'Your city is added!','success')
#         return redirect(url_for('home'))
    
    
#     return render_template('addCity.html', title='Add city', form=form)

# @app.route("/createRelationship_HAS_HASHTAG",methods=['GET','POST'])
# @jwt_required()

# def createRelationship_HAS_HASHTAG():
#     form = AddHasHashForm()
#     m=form.validate_on_submit()
#     if m:
        
#         HasHashtag(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1]).save(db)

#         flash(f'Your relationship is added!','success')
#         return redirect(url_for('createRelationship_HAS_HASHTAG'))
    
    
#     return render_template('addHashashtag.html', title='Add has hastag', form=form)

# @app.route("/createRelationship_HAS_ACTIVITY",methods=['GET','POST'])
# @jwt_required()
# def createRelationship_HAS_ACTIVITY():
#     form = AddHasActivityForm()
#     if form.validate_on_submit():
#         HasActivity(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1],durationOfActivity=form.duration_of_activity.data,experience=form.experience.data,minAge=form.minAge.data,maxAge=form.maxAge.data).save(db)

#         flash(f'Your relationship is added!','success')
#         return redirect(url_for('home'))
    
    
#     return render_template('addHasActivity.html', title='Add has hastag', form=form)  

# @app.route("/createRelationship_VISITED",methods=['GET','POST'])
# @jwt_required()
# def createRelationship_VISITED():
#     form = AddVisitedForm()
#     if form.validate_on_submit():
#         Visited(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1],rate=form.rate.data,dateAndTime=datetime.datetime.now()).save(db)
#         query=f""" MATCH (a:Attraction)<-[r:VISITED]-() WHERE a.id='{form.idOfAttraction.data}'
#                    WITH a, AVG(r.rate) AS prosecnaOcena
#                    SET a.averageRate = prosecnaOcena;
#                    """
#         db.execute(query)
#         flash(f'Your relationship is added!','success')
#         return redirect(url_for('home'))
    
    
#     return render_template('addVisited.html', title='Add has hastag', form=form)  


# @app.route("/createRelationship_WANTS_TO_SEE",methods=['GET','POST'])
# @jwt_required()
# def createRelationship_WANTS_TO_SEE():
#     form = AddWantsToSeeForm()
#     if form.validate_on_submit():
#         WantsToSee(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1]).save(db)

#         flash(f'Your relationship is added!','success')
#         return redirect(url_for('home'))
    
    
#     return render_template('addWantsToSee.html', title='Add has hastag', form=form)


# @app.route("/createRelationship_HAS_ATTRACTION",methods=['GET','POST'])
# @jwt_required()
# def createRelationship_HAS_ATTRACTION():
#     form = AddHasAttractionForm()
#     if form.validate_on_submit():
#         HasAttraction(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1]).save(db)

#         flash(f'Your relationship is added!','success')
#         return redirect(url_for('home'))
    
    
#     return render_template('addHasAttraction.html', title='Add has hastag', form=form)
# DEO ZA RECOMMENDATION SYSTEM
# K-means clustering
# @app.route('/newUsercoldStartRecommendation', methods=['GET']) 
# def newUsercoldStartRecommendation(userId):
#     #TODO: Poziva se prilikom registracije korisnika
#     query=f""" MATCH (u:User)-[:WANTS_TO_SEE]->(h:Hashtag)<-[:HAS_HASHTAG]-(a:Attraction) WHERE u.id="{userId}"
#     RETURN a.id
#     ORDER BY a.averageRate DESC
#     LIMIT 5 """
#     result=list(db.execute_and_fetch(query))
#     listOfAttributes = [item["a.id"] for item in result]
#     query=f""" MATCH (u:User) WHERE u.id='{userId}'
#                 MATCH(a:Attraction) WHERE a.id IN {listOfAttributes}
#                 MERGE(a)-[r:RECOMMENDED_FOR]->(u) 
#         """
#     db.execute(query)


# @app.route('/recommend/<string:userId>', methods=['GET']) 
# @jwt_required()
# def recommend(userId):
#     query=f""" MATCH (u:User)<-[r:RECOMMENDED_FOR]-(a:Attraction) WHERE u.id="{userId}"
#     RETURN a
#     ORDER BY a.averageRate DESC
#     """
#     result=list(db.execute_and_fetch(query))
#     recommendAttractions=[item["a"] for item in result]
#     results = attractions_schema.dump(recommendAttractions)
#     return jsonify(results)
  
  
   
# @app.route('/nearYouRecommendation', methods=['GET']) 
# @jwt_required()
# def nearYouRecommendation():
#     usersId="9f130ecc-ab78-4d07-964a-1a38bc131675"
#     latitudeAndLongitudeOfTheUser=(
#         match()
#         .node(labels="User",variable="u")
#         .where(item="u.id",operator=Operator.EQUAL,literal=usersId)
#         .return_(["u.longitude","u.latitude"])
#         .execute()
#     )
  
#     lista=list(latitudeAndLongitudeOfTheUser)
#     usersLongitude=lista[0]["u.longitude"]
#     usersLatitude=lista[0]["u.latitude"]
    
    
#     query=f""" 
# MATCH (a:Attraction)
# WITH a,
#     6371 * 2 * atan2(
#         sqrt(
#             sin((a.latitude - {usersLatitude}) * 3.14 / 360) * 
#             sin((a.latitude - {usersLatitude}) * 3.14 / 360) +
#             cos({usersLatitude} * 3.14 / 180) * 
#             cos(a.latitude * 3.14 / 180) * 
#             sin((a.longitude - {usersLongitude}) * 3.14 / 360) * 
#             sin((a.longitude - {usersLongitude}) * 3.14 / 360)
#         ),
#         sqrt(
#             1 - sin((a.latitude - {usersLatitude}) * 3.14 / 360) * 
#             sin((a.latitude - {usersLatitude}) * 3.14 / 360) +
#             cos({usersLatitude} * 3.14 / 180) * 
#             cos(a.latitude * 3.14 / 180) * 
#             sin((a.longitude - {usersLongitude}) * 3.14 / 360) * 
#             sin((a.longitude - {usersLongitude}) * 3.14 / 360)
#         )
#     ) AS udaljenost
# RETURN a, udaljenost
# ORDER BY udaljenost
# LIMIT 10;
#  """
          
#     fetchNearestAttractions=db.execute_and_fetch(query)
    
#     listOfNearestAttractions=[]
#     listaa=list(fetchNearestAttractions)
#     print(listaa)
#     for item in listaa:
#         listOfNearestAttractions.append(item["a"])
#     print(listOfNearestAttractions)
    
#     results = attractions_schema.dump(listOfNearestAttractions)
#     return jsonify(results)
    
# @app.route('/planTrip', methods=['POST'])
# @jwt_required()
# def planTrip():
#     distanceKm=1000000000000000
#     cityName="Nis" 
#     # mora destinacija da se odabere
#     usersLatitude=45
#     usersLongitude=45
#     activities=[]
#     durationH=444444
#     durationM=45
#     durationS=0
#     duration=True
#     familyFiendly=True
#     parking=True
#     # experience=True
#     maxDestinations=4
#     query=""
#     if distanceKm==-1:
#         distanceKm=sys.float_info.max
    
#     whereConditions=[]
    
#     query+=f"""MATCH (c:City{{name:'{cityName}'}})-[r1:HAS_ATTRACTION]->(a:Attraction)
#     OPTIONAL MATCH (a)-[r2:HAS_ACTIVITY]->(activity:Activity)
#     WHERE size({activities}) = 0 OR (size({activities}) > 0 AND activity.name IN {activities})
#     WITH a, COLLECT(activity) AS activitiesForAttraction,COLLECT(r2) AS rels
#        """

#     if familyFiendly:
#         whereConditions.append("a.familyFriendly = true ")
        
#     if parking:
#         whereConditions.append("a.parking = true ")
        
#     if whereConditions:
#         query+="WHERE "+" AND ".join(whereConditions)
        
#     query+= f""" WITH a, activitiesForAttraction,rels,
#      CASE 
#        WHEN size({activities}) > 0 
#        THEN REDUCE(s = 0, x IN activitiesForAttraction | s + CASE WHEN x.name IN {activities} THEN 1 ELSE 0 END)
#        ELSE 0
#      END AS commonActivities
#     WITH a, activitiesForAttraction, commonActivities,rels,
    
#      REDUCE(s = 0.0, r IN rels | s + COALESCE(toInteger(split(coalesce(toString(r.durationOfActivity), ""), ":")[0])*3600 + toInteger(split(coalesce(toString(r.durationOfActivity), ""), ":")[1])*60 + toInteger(split(coalesce(toString(r.durationOfActivity), ""), ":")[2]), 0.0))+(a.durationOfVisit.hour * 3600 + a.durationOfVisit.minute * 60 + a.durationOfVisit.second) AS totalDuration,
#         6371 * 2 * atan2(
#         sqrt(
#                 sin((a.latitude - {usersLatitude}) * 3.14 / 360) * 
#                 sin((a.latitude - {usersLatitude}) * 3.14 / 360) +
#                 cos({usersLatitude} * 3.14 / 180) * 
#                 cos(a.latitude * 3.14 / 180) * 
#                 sin((a.longitude - {usersLongitude}) * 3.14 / 360) * 
#                 sin((a.longitude - {usersLongitude}) * 3.14 / 360)
#             ),
#         sqrt(
#                 1 - sin((a.latitude - {usersLatitude}) * 3.14 / 360) * 
#                 sin((a.latitude - {usersLatitude}) * 3.14 / 360) +
#                 cos({usersLatitude} * 3.14 / 180) * 
#                 cos(a.latitude * 3.14 / 180) * 
#                 sin((a.longitude - {usersLongitude}) * 3.14 / 360) * 
#                 sin((a.longitude - {usersLongitude}) * 3.14 / 360)
#             )
#         ) AS udaljenost
#         WHERE udaljenost<{distanceKm}"""
        
#     if(duration):
#         query+= f""" AND totalDuration < ({durationH}* 3600+{durationM}*60+{durationS})
#         """
    
#     query+=f"""RETURN a,totalDuration,udaljenost,commonActivities
#         ORDER BY udaljenost,commonActivities DESC 
#         """
#     if(maxDestinations>0):
#         query+=f"""LIMIT {maxDestinations} """
    
#     print(query)
#     p=list(db.execute_and_fetch(query))
#     print(p)
#     recommendAttractions=[item["a"] for item in p]
#     results = attractions_schema.dump(recommendAttractions)
#     return jsonify(results)
    
    
    
#     # da su do odredjene udaljenosti od mene
#     # da ima neke od aktivnosti
#     # vremensko trajanje ture
#     # da atrakcije budu za jednu osobu/vise
#     # da li se moze doci kolima
     
     
# @app.route('/serachEngineAll', methods=['POST','GET'])
# def serachEngineAll():
#     userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
#     # istorija,musteseeplaces,cultutralHeirtage,zabava
#     listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
#     useeWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]

#     dummyString="c"
#     query=f"""
#     WITH toLower("{dummyString}") as dummystring
#     MATCH (c:City)-[:HAS_ATTRACTION]->(a:Attraction)
#     WHERE toLower(c.name) = dummystring
#     OR toLower(a.name) STARTS WITH dummystring
#     OR toLower(a.name) CONTAINS dummystring
#     OR toLower(a.description) CONTAINS dummystring
#     WITH a,CASE WHEN toLower(c.name) = dummystring THEN 1 ELSE 0 END as cityExists,
#     CASE WHEN toLower(a.name) STARTS WITH dummystring THEN 1 ELSE 0 END as nameStartsWith,
#     CASE WHEN toLower(a.name) CONTAINS dummystring THEN 1 ELSE 0 END as nameContains
#     OPTIONAL MATCH (a)-[r:HAS_HASHTAG]-(h:Hashtag)
#     WHERE h.name IN {useeWantsToSeehashtag}
#     WITH a, cityExists, nameStartsWith, nameContains,COUNT(h) AS matchingHashtags
#     RETURN a, cityExists, nameStartsWith,nameContains, COALESCE(matchingHashtags, 0) AS matchingHashtags
#     ORDER BY cityExists DESC, nameStartsWith DESC,nameContains DESC,matchingHashtags DESC """
#     p= list(db.execute_and_fetch(query))
#     listOfResults=[item["a"] for item in p]
#     results = attractions_schema.dump(listOfResults)
#     return jsonify(results)
    
# @app.route('/searchEngineAttractionName', methods=['POST','GET'])
# def searchEngineAttractionName():
#     userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
#     listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
#     userWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]
#     dummyString="va"

#     query=f""" 
#     WITH toLower("{dummyString}") as dummyString
#     MATCH (a:Attraction)
#     WHERE toLower(a.name) CONTAINS dummyString
#     OR toLower(a.description) CONTAINS dummyString
#     WITH a,
#         CASE WHEN toLower(a.name) STARTS WITH dummyString THEN 1 ELSE 0 END as startsWithString,
#         CASE WHEN toLower(a.name) CONTAINS dummyString THEN 1 ELSE 0 END as containsString,
#         CASE WHEN toLower(a.description) STARTS WITH dummyString THEN 1 ELSE 0 END as descStartsWithString,
#         CASE WHEN toLower(a.description) CONTAINS dummyString THEN 1 ELSE 0 END as descContainsString,
#         dummyString
#     WITH a, startsWithString, containsString, descStartsWithString, descContainsString, dummyString
#     OPTIONAL MATCH (a)-[r:HAS_HASHTAG]-(h:Hashtag)
#     WHERE h.name IN {userWantsToSeehashtag}
#     AND (toLower(a.name) CONTAINS dummyString OR toLower(a.description) CONTAINS dummyString)
#     WITH a, startsWithString, containsString, descStartsWithString, descContainsString, dummyString, COUNT(h) AS matchingHashtags, h
#     RETURN a, startsWithString, containsString, descStartsWithString, descContainsString, COUNT(h) AS matchingHashtags, a.averageRate
#     ORDER BY startsWithString DESC, containsString DESC, descStartsWithString DESC, descContainsString DESC, a.averageRate DESC

#     """
#     p= list(db.execute_and_fetch(query))
#     listOfResults=[item["a"] for item in p]
#     results = attractions_schema.dump(listOfResults)
#     return jsonify(results)
    
# @app.route('/searchEngineHashTag', methods=['POST','GET'])
# def searchEngineHashTag():
#     userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
#     listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
#     userWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]
#     dummyString="ist"
#     query=f""" 
#     WITH toLower("{dummyString}") AS dummyString
#     MATCH (a:Attraction)-[:HAS_HASHTAG]->(h:Hashtag) 
#     WHERE toLower(h.name) STARTS WITH dummyString 
#     WITH a, collect(h.name) as hashtags
#     with a, REDUCE(s = 0, i IN hashtags | s + CASE WHEN i IN {userWantsToSeehashtag} THEN 1 ELSE 0 END) AS rezultat
#     RETURN a,rezultat,a.averageRate
#     ORDER BY rezultat DESC, a.averageRate DESC
#  """
#     p= list(db.execute_and_fetch(query))
#     listOfResults=[item["a"] for item in p]
#     results = attractions_schema.dump(listOfResults)
#     return jsonify(results)

# @app.route('/searchEngineActivity', methods=['POST','GET'])
# def searchEngineActivity():
#     userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
#     listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
#     userWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]
#     dummyString="p"
#     query=f""" 
#     WITH toLower("{dummyString}") AS dummyString
#     MATCH (a:Attraction)-[:HAS_ACTIVITY]->(h:Activity) 
#     WHERE toLower(h.name) STARTS WITH dummyString 
#     with a, collect(h.name) as activities

#     RETURN a  ,a.averageRate,activities
#     ORDER BY  a.averageRate DESC
#  """
#     p= list(db.execute_and_fetch(query))
#     listOfResults=[item["a"] for item in p]
#     results = attractions_schema.dump(listOfResults)
#     return jsonify(results)
    
# @app.route('/searchEngineCity', methods=['POST','GET'])
# def searchEngineCity():
#     userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
#     listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
#     userWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]
#     dummyString="Nis"
#     query=f""" 
#     WITH toLower("{dummyString}") AS dummyString
#     MATCH (a:Attraction)<-[:HAS_ATTRACTION]-(c:City) 
#     WHERE toLower(c.name) = dummyString 
#     OPTIONAL MATCH (a)-[r:HAS_HASHTAG]-(h:Hashtag)
#     WHERE h.name IN {userWantsToSeehashtag}
#     WITH a,COUNT(h) AS matchingHashtags
#     RETURN a, COALESCE(matchingHashtags, 0) AS matchingHashtags
#     ORDER BY matchingHashtags DESC, a.averageRate DESC
#  """
#     p= list(db.execute_and_fetch(query))
#     listOfResults=[item["a"] for item in p]
#     results = attractions_schema.dump(listOfResults)
#     return jsonify(results)   

    

    
    

#TODO: Dodaj role i u deo za login onda dodaj claims
    
    
    
    
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