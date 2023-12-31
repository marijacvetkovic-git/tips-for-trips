import datetime
import uuid
from flask import Blueprint,render_template,jsonify,flash, request
from app import app , bcrypt, db ,ma
from gqlalchemy import match
from gqlalchemy.query_builders.memgraph_query_builder import Operator
from app.forms import AddWantsToSeeForm, LogInForm, RegistrationForm
from app.models import User, WantsToSee

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
)



jwtM=JWTManager(app)
auth= Blueprint("auth",__name__,static_folder="static",template_folder="templates")

@auth.route("/register", methods=['GET','POST'])
# kada stavim da je post metoda forma nece da se kreira
def register():
    req_data = request.get_json() 
    # dateOfBirth=datetime.date(year=req_data.get("dateofbirth")["year"],month=req_data.get("dateofbirth")["month"],day=req_data.get("dateofbirth")["day"])
    form = RegistrationForm(
    username=req_data.get("username"),
    email=req_data.get("email"),
    password=req_data.get("password"),
    confirm_password= req_data.get("confirm_password"),
    dateofbirth=req_data.get("dateOfBirth"),
    longitude=req_data.get("longitude"),
    latitude=req_data.get("latitude")
    )
    if form.validate_on_submit():
            # dateOfBirth=datetime.date(year=(form.dateofbirth.data["year"]),month=form.dateofbirth.data["month"],day=form.dateofbirth.data["day"])
            user=User(id=str(uuid.uuid4()),username=form.username.data,password=bcrypt.generate_password_hash(form.password.data),
                     email=form.email.data,dateOfBirth=1,longitude=form.longitude.data,latitude=form.latitude.data)
            
            user.save(db)
            return jsonify({"username":user.username,"id":user.id}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 406
   
@auth.route("/login", methods=['GET'])
def login():
    req_data = request.get_json() 
    form = LogInForm(
    username=req_data.get("username"),
    password= req_data.get("password"),
    remember=req_data.get("remember")
    )
    if form.validate():
        users=(
          match()
          .node(labels="User",variable="u")
          .where(item="u.username",operator=Operator.EQUAL,literal=form.username.data)
          .return_(("u","user"))
          .execute()
          )
        listOfUsers=list(users)
        if not listOfUsers :
            return jsonify({"message":'Login Unsuccessful. Please check username and password'}),400
        else:   
            user:User=(listOfUsers[0])['user']
            print(user.password)
            print(form.password.data)
            if not bcrypt.check_password_hash(user.password,form.password.data):
                return jsonify({"message":'Login Unsuccessful. Please check username and password'}),400
            else:
                expires_delta = datetime.timedelta(minutes=60) 
                access_token = create_access_token(identity=user.username,expires_delta=expires_delta)
        # access_token = create_access_token(identity=user_id, expires_delta=expires_delta, fresh=True, additional_claims={'roles': users[user_id]['roles']})
                return jsonify(
                {"access_token": access_token}
            ),200
        
@auth.route("/createRelationship_WANTS_TO_SEE",methods=['POST'])
def createRelationship_WANTS_TO_SEE():
    req_data = request.get_json()
    form = AddWantsToSeeForm(
    idOfUser=req_data.get("idOfUser"),
    idsOfHashtags=req_data.get("idsOfHashtags")
    )
    if form.validate_on_submit():
        resultList=[]
        for hashtag in form.tupleForResult[1]:
            WantsToSee(_start_node_id=form.tupleForResult[0],_end_node_id=hashtag).save(db)
            resultList.append((form.tupleForResult[0],hashtag))
        return jsonify(resultList),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 406
    
         
    
    

@auth.route('/newUsercoldStartRecommendation/<string:userId>', methods=['GET']) 
def newUsercoldStartRecommendation(userId):
    #TODO: Poziva se prilikom registracije korisnika
    query=f""" MATCH (u:User)-[:WANTS_TO_SEE]->(h:Hashtag)<-[:HAS_HASHTAG]-(a:Attraction) WHERE u.id="{userId}"
    RETURN a.id
    ORDER BY a.averageRate DESC
    LIMIT 5 """
    result=list(db.execute_and_fetch(query))
    listOfAttributes = [item["a.id"] for item in result]
    query=f""" MATCH (u:User) WHERE u.id='{userId}'
                MATCH(a:Attraction) WHERE a.id IN {listOfAttributes}
                MERGE(a)-[r:RECOMMENDED_FOR]->(u) 
        """
    db.execute(query)
  