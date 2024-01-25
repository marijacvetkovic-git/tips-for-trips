import string
from datetime import time
import uuid
from flask import Blueprint, redirect,render_template,jsonify,flash, request, url_for
from flask_jwt_extended import jwt_required

from app.forms import *
from app.models import HasActivity, HasAttraction, HasHashtag, HasImage, Image, Visited, WantsToSee

admin= Blueprint("admin",__name__,static_folder="static",template_folder="templates")

@admin.route("/addImage/<string:attractionId>",methods=['POST'])
# @jwt_required()
def addImage(attractionId):
    req_data = request.get_json() 
    path=req_data.get("path")
    print(path)
    query=f""" MATCH (a:Attraction) WHERE a.id='{attractionId}'
    OPTIONAL MATCH (a)-[r:HAS_IMAGE]->(i) WHERE i.path='{path}'
    WITH a, COUNT(i) as images
    return a,images """
    p=(list(db.execute_and_fetch(query)))[0]
    attraction:Attraction=p["a"]
    number=p["images"]
    if(number>0):
        return jsonify({"error":"Path exists"}), 206
    image:Image=Image(id=str(uuid.uuid4()),path=path)
    image.save(db)
    
    HasImage(_start_node_id=attraction._id,_end_node_id=image._id).save(db)

    return jsonify(),200


@admin.route("/deleteAttraction/<string:attractionId>",methods=['DELETE'])  
@jwt_required()

def deleteAttraction(attractionId):
    query =f""" MATCH (a:Attraction) WHERE a.id='{attractionId}' return a"""
    attraction=list(db.execute_and_fetch(query))
    if(attraction):
        
        query=f""" MATCH (a:Attraction) WHERE a.id='{attractionId}'
        OPTIONAL MATCH (a)-[r:HAS_IMAGE]->(i:Image)
        DETACH DELETE a,r,i
        """
        db.execute(query)    
        return jsonify({}),200
    else:
        errors={"errors":"No attraction found!"}
        return jsonify(errors), 206
    
        
  
@admin.route("/createAttraction",methods=['POST'])
@jwt_required()

def createAttraction():
    req_data = request.get_json() 

    form= AddAttractionForm(
    name=req_data.get("name"),
    description=req_data.get("description"),
    duration_of_visit=req_data.get("duration"),
    family_friendly=req_data.get("familyFriendly"),
    latitude=req_data.get("latitude"),
    longitude=req_data.get("longitude"),
    parking=req_data.get("parking")
    )
    if form.validate_on_submit():
        id=str(uuid.uuid4())
        attraction=Attraction(id=id,name=form.name.data,description=form.description.data,longitude=form.longitude.data,latitude=form.latitude.data,familyFriendly=form.family_friendly.data,parking=form.parking.data,durationOfVisit=form.duration_of_visit.data,averageRate=0)
        attraction.save(db)

        
        return jsonify({"id":id}),200
    
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206
   
    
@admin.route("/deleteHashtag/<string:hashtagId>",methods=['DELETE'])  
@jwt_required()

def deleteHashtag(hashtagId):
    query=f""" MATCH (a:Hashtag) WHERE a.id='{hashtagId}' return a"""
    hashtag=list(db.execute_and_fetch(query))
    if(hashtag):
        query=f""" MATCH (a:Hashtag) WHERE a.id='{hashtagId}'
        DETACH DELETE a
        """
        db.execute(query)    
        return jsonify({"Message":"Hashtag deleted"}),200
    else:
        return jsonify({"errors":"Hashtag with that id does not exist!"}),206
   

@admin.route("/createHashtag/<string:hashName>",methods=['POST'])
@jwt_required()

def createHashtag(hashName):
    
    form = AddHashtagForm(
        name=hashName
    )
    if form.validate_on_submit():
        hashtag=Hashtag(id=str(uuid.uuid4()),name=form.name.data)
        hashtag.save(db)

        return jsonify({"Message":"Hashtag is created"}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206
    
    
@admin.route("/deleteActivity/<string:activityId>",methods=['DELETE'])  
@jwt_required()

def deleteActivity(activityId):
    query=f"""  MATCH (a:Activity) WHERE a.id='{activityId}' return a"""
    activity=list(db.execute_and_fetch(query))
    if(activity):
        query=f""" MATCH (a:Activity) WHERE a.id='{activityId}'
        DETACH DELETE a
        """
        db.execute(query)    
        return jsonify({"Message":"Activity deleted"}),200
    else:
        return jsonify({"errors":"Activity with that id does not exist"}),206
        
     
        
@admin.route("/createActivity/<string:activityName>",methods=['POST'])
@jwt_required()

def createActivity(activityName):
    
    form = AddActivityForm(
        name=activityName
    )
    if form.validate_on_submit():
        activity=Activity(id=str(uuid.uuid4()),name=form.name.data)
        activity.save(db)

        return jsonify({"Message":"Activity is created"}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206


@admin.route("/createCity",methods=['POST'])
@jwt_required()

def createCity():
    req_data = request.get_json()    
    form = AddCityForm(
    name=req_data.get("cityName"),
    description=req_data.get("cityDescription")
        
    )
    if form.validate_on_submit():
        city=City(id=str(uuid.uuid4()),name=form.name.data,description=form.description.data)
        city.save(db)

        return jsonify({"Message":"Grad dodat"}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206
    
    
@admin.route("/deleteCity/<string:cityId>",methods=['DELETE'])
@jwt_required()

def deleteCity(cityId):
    query=f"""  MATCH (a:City) WHERE a.id='{cityId}' RETURN a"""
    cities=list(db.execute_and_fetch(query))
    if(cities):
        query=f""" MATCH (a:City) WHERE a.id='{cityId}'
        DETACH DELETE a
        """
        db.execute(query)
        return jsonify({"Message":"City deleted"}),200
    else:
        return jsonify({"errors":"City with that id does not exist"}),206
        
    

@admin.route("/createRelationship_HAS_HASHTAG/<string:idOfAttraction>/<string:idOfHashtag>",methods=['POST'])
@jwt_required()
def createRelationship_HAS_HASHTAG(idOfAttraction,idOfHashtag,):
    form = AddHasHashForm(
        idOfAttraction=idOfAttraction,
        idOfHashtag=idOfHashtag
        
    )
    m=form.validate_on_submit()
    if m:
        
        HasHashtag(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1]).save(db)

        return jsonify({"Message":"HAS_HASHTAG added"}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206

@admin.route("/deleteRelationship_HAS_HASHTAG/<string:idOfAttraction>/<string:idOfHashtag>",methods=['DELETE'])
@jwt_required()
def deleteRelationship_HAS_HASHTAG(idOfAttraction,idOfHashtag):
    form = DeleteHasHashtagForm(
        idOfAttraction=idOfAttraction,
        idOfHashtag=idOfHashtag
        
    )
    m=form.validate_on_submit()
    if m:
        query=f""" MATCH (a:Attraction{{id:"{idOfAttraction}"}})-[r:HAS_HASHTAG]->(h:Hashtag{{id:"{idOfHashtag}"}}) DELETE r
        """
        db.execute(query)

        return jsonify({"Message":"HAS_HASHTAG deleted"}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206


@admin.route("/createRelationship_HAS_ACTIVITY",methods=['POST'])
@jwt_required()
def createRelationship_HAS_ACTIVITY():
    req_data=request.get_json()
    form = AddHasActivityForm(
    idOfAttraction=req_data.get("idOfAttractionCHasActivity"),
    idOfActivity=req_data.get("idOfActivityCHasActivity"),
    duration_of_activity=req_data.get("durationOfActivity"),
    experience=req_data.get("experience"),
    minAge=req_data.get("minAge"),
    maxAge=req_data.get("maxAge")
    )
    if form.validate_on_submit():
        HasActivity(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1],durationOfActivity=form.duration_of_activity.data,experience=form.experience.data,minAge=form.minAge.data,maxAge=form.maxAge.data).save(db)

        return jsonify({"Message":"HAS_ACTIVITY added"}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206  


@admin.route("/deleteRelationship_HAS_ACTIVITY/<string:idOfAttraction>/<string:idOfActivity>",methods=['DELETE'])
@jwt_required()
def deleteRelationship_HAS_ACTIVITY(idOfAttraction,idOfActivity):
    form = DeleteHasActivityForm(
        idOfAttraction=idOfAttraction,
        idOfActivity=idOfActivity
        
    )
    m=form.validate_on_submit()
    if m:
        query=f""" MATCH (a:Attraction{{id:"{idOfAttraction}"}})-[r:HAS_ACTIVITY]->(h:Activity{{id:"{idOfActivity}"}})  DELETE r"""

        db.execute(query)

        return jsonify({"Message":"HAS_ACTIVITY deleted"}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206
    
    

@admin.route("/createRelationship_VISITED",methods=['POST'])
@jwt_required()
def createRelationship_VISITED():
    req_data=request.get_json()

    form = AddVisitedForm(
        idOfAttraction=req_data.get("idOfAttraction"),
        idOfUser=req_data.get("idOfUser"),
        rate=req_data.get("rate")
        
    )
    if form.validate_on_submit():
        Visited(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1],rate=form.rate.data,dateAndTime=datetime.datetime.now()).save(db)
        query=f""" MATCH (a:Attraction)<-[r:VISITED]-() WHERE a.id='{form.idOfAttraction.data}'
                   WITH a, AVG(r.rate) AS prosecnaOcena
                   SET a.averageRate = prosecnaOcena;
                   """
        db.execute(query)
        return jsonify({"Message":"VISITED added"}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206  

@admin.route("/deleteRelationship_VISITED/<string:idOfAttraction>/<string:idOfUser>",methods=['POST'])
@jwt_required()
def deleteRelationship_VISITED(idOfAttraction,idOfUser):

    form = DeleteVisitedForm(
        idOfAttraction=idOfAttraction,
        idOfUser=idOfUser
    )
    if form.validate_on_submit():
        query=f""" MATCH (a:Attraction{{id:'{form.idOfAttraction.data}'}})<-[r:VISITED]-(u:User{{id:'{form.idOfUser.data}'}}) 
        DELETE r"""
        db.execute(query)
        query=f""" MATCH (a:Attraction)<-[r:VISITED]-() WHERE a.id='{form.idOfAttraction.data}'
                   WITH a, AVG(r.rate) AS prosecnaOcena
                   SET a.averageRate = prosecnaOcena;
                   """          
        db.execute(query)
        return jsonify({"Message":"VISITED deleted"}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206  


@admin.route("/createRelationship_HAS_ATTRACTION",methods=['POST'])
@jwt_required()
def createRelationship_HAS_ATTRACTION():
    req_data = request.get_json() 
    form = AddHasAttractionForm(
    idOfCity=req_data.get("idOfCityCHasAttraction"),
    idOfAttraction=req_data.get("idOfAttractionCHasAttraction")
    )
    if form.validate_on_submit():
        HasAttraction(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1]).save(db)

        flash(f'Your relationship is added!','success')
        return jsonify({"Message":"Relationship has_attraction is created"}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206
    
    
@admin.route("/deleteRelationship_HAS_ATTRACTION/<string:idOfCity>/<string:idOfAttraction>",methods=['DELETE'])
@jwt_required()
def deleteRelationship_HAS_ATTRACTION(idOfCity,idOfAttraction):
    form = DeleteHasAttractionForm(
    idOfCity=idOfCity,
    idOfAttraction=idOfAttraction
    )
    if form.validate_on_submit():
        query=f""" MATCH (c:City{{id:'{idOfCity}'}})-[r:HAS_ATTRACTION]->(a:Attraction{{id:'{idOfAttraction}'}})  DELETE r """
        
        db.execute(query)

        return jsonify({"Message":"Relationship has_attraction is delete"}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206