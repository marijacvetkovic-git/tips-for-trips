import datetime
import string
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
            user=User(id=str(uuid.uuid4()),username=form.username.data,password=bcrypt.generate_password_hash(form.password.data),
                     email=form.email.data,dateOfBirth=1,longitude=form.longitude.data,latitude=form.latitude.data)
            
            user.save(db)
            return jsonify({"username":user.username,"id":user.id}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206
   
@auth.route("/login/<string:username>/<string:password>/<float:latitude>/<float:longitude>", methods=['GET'])
def login(username,password,latitude,longitude):
    form = LogInForm(
        username=username,
        password=password,
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
            return jsonify({"message":'Login Unsuccessful. Please check username and password'}),206
        else:  
            query=f"""MATCH (u:User) WHERE u.username='{username}' SET u.latitude={latitude} SET u.longitude={longitude} """
            db.execute(query)
            user:User=(listOfUsers[0])['user']
            print(user.password)
            print(form.password.data)
            if not bcrypt.check_password_hash(user.password,form.password.data):
                return jsonify({"message":'Login Unsuccessful. Please check username and password'}),206
            else:
                expires_delta = datetime.timedelta(minutes=60) 
                # access_token = create_access_token(identity=user.username,expires_delta=expires_delta)
                access_token = create_access_token(identity=user.id, expires_delta=expires_delta, fresh=True, additional_claims={'username': user.username,'id':user.id})
                return jsonify(
                {"token": access_token}
            ),200
        
@auth.route("/createRelationship_WANTS_TO_SEE",methods=['POST'])
def createRelationship_WANTS_TO_SEE():
    req_data = request.get_json()    
    # idsOfHashtags=','.join(req_data.get("idsOfHashtags"))
    # p:string=""+idsOfHashtags
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
        return jsonify(errors), 206
    
         
    
    

@auth.route('/newUsercoldStartRecommendation/<string:userId>', methods=['POST']) 
def newUsercoldStartRecommendation(userId):
    #TODO: Poziva se prilikom registracije korisnika
    query=f""" MATCH (u:User)-[:WANTS_TO_SEE]->(h:Hashtag)<-[:HAS_HASHTAG]-(a:Attraction) WHERE u.id="{userId}"
    RETURN DISTINCT a.id
    ORDER BY a.averageRate DESC
    LIMIT 5 """
    result=list(db.execute_and_fetch(query))
    listOfAttributes = [item["a.id"] for item in result]
    print(userId)
    print(listOfAttributes)
    query=f""" MATCH (u:User) WHERE u.id='{userId}'
                MATCH (a:Attraction) WHERE a.id IN {listOfAttributes}
                MERGE (a)-[r:RECOMMENDED_FOR]->(u) 
                return u,r,a
                
        """
    p=list(db.execute_and_fetch(query))
    return jsonify({"message": "Success"}), 200