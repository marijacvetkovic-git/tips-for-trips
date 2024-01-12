
import string
from app import db
from flask import Blueprint,jsonify
from gqlalchemy import match
from gqlalchemy.query_builders.memgraph_query_builder import Operator
from datetime import time





helpers= Blueprint("helpers",__name__,static_folder="static",template_folder="templates")

@helpers.route("/getHashtags", methods=['GET'])
def getHashtags():
    query="MATCH (h:Hashtag) return h.id as id ,h.name as name"
    listOfHashtags=list(db.execute_and_fetch(query))
    print(listOfHashtags)
    p=jsonify(listOfHashtags)
    print(p)
    return p

@helpers.route("/removeUser/<string:username>", methods=['DELETE'])
def removeUser(username):
    u=username
    query="MATCH (u:Username) WHERE u.username='{u}' DELETE u"
    db.execute(query)
    return jsonify({"message":"Successfuly deleted user"})

@helpers.route("/returnMostRecommendedAttractions", methods=['GET'])
def returnMostRecommendedAttractions():
    query=f"""MATCH (a:Attraction)-[r:RECOMMENDED_FOR]->(u) 
    WITH a,COUNT(r) as numberOfRecommendation
    RETURN a.id as id ,a.name as name,numberOfRecommendation
    ORDER BY numberOfRecommendation DESC
    """
    listOfAttractions=list(db.execute_and_fetch(query))
    return jsonify({"listOfAttractions":listOfAttractions})

@helpers.route("/returnAttraction/<string:id>", methods=['GET'])
def returnAttraction(id):
    query=f"""MATCH (a:Attraction) WHERE a.id='{id}'
OPTIONAL MATCH (a)-[r:HAS_ACTIVITY]->(activity:Activity) 
OPTIONAL MATCH (a)-[r1:HAS_HASHTAG]->(h:Hashtag)
 WITH a,COLLECT(DISTINCT activity.name) AS activitiesForAttraction,COLLECT(DISTINCT r) as relationship , COLLECT(DISTINCT h.name) as hashtags
    return a.id as id , a.name as name ,a.description as description, a.averageRate as avgRate,activitiesForAttraction,relationship, hashtags
    """
    resultList=list(db.execute_and_fetch(query))
    listOfAttractionInformation=[]
    for item in resultList:
        # hasActivity=[i.properties for i in item["relationship"]]
        hasActivity = [{k: str(v) if k == "durationOfActivity" else v for k, v in i.properties.items()} for i in item["relationship"]]

        listOfAttractionInformation.append({"name":item["name"],"description":item["description"],"avgRate":item["avgRate"],"activities":item["activitiesForAttraction"],
                                            "relationship":hasActivity,"hashtags":item["hashtags"]})
    return jsonify(listOfAttractionInformation)
#  NISAM JOS ISKORISTILA FJU..A VERV BI TREBALO
@helpers.route("/removeOldUsers",methods=["GET"])
def removeOldUsers():
    query=f"""MATCH (user:User)
    WHERE NOT EXISTS ((:Hashtag)<-[:WANTS_TO_SEE]-(user))
    RETURN user.username"""
    resultList=list(db.execute_and_fetch(query))
    return jsonify(resultList)

@helpers.route("/getCities",methods=["GET"])
def getCities():
    query=f""" MATCH (c:City)
    RETURN c.name as name, c.id as id
    """
    resultList=list(db.execute_and_fetch(query))
    return jsonify(resultList)

@helpers.route("/getActivities",methods=["GET"])
def getActivities():
    query=f"""  MATCH (a:Activity)<-[r:HAS_ACTIVITY]-()
    WITH DISTINCT a
    RETURN a.name as name, a.id as id
    """
    resultList=list(db.execute_and_fetch(query))
    return jsonify(resultList)

@helpers.route("/getLongitudeLatitude/<string:userId>",methods=["GET"])
def getLongitudeLatitude(userId):
    query=f"""  MATCH (u:User) where u.id='{userId}' RETURN u.longitude as longitude, u.latitude as latitude"""
    resultList=list(db.execute_and_fetch(query))
    return jsonify(resultList)