
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
 WITH a,COLLECT(activity.name) AS activitiesForAttraction,COLLECT(r) as relationship
    return a.name,a.description,activitiesForAttraction,relationship
    """
    resultList=list(db.execute_and_fetch(query))
    listOfAttractionInformation=[]
    for item in resultList:
        # hasActivity=[i.properties for i in item["relationship"]]
        hasActivity = [{k: str(v) if k == "durationOfActivity" else v for k, v in i.properties.items()} for i in item["relationship"]]

        listOfAttractionInformation.append({"name":item["a.name"],"description":item["a.description"],"activities":item["activitiesForAttraction"],
                                            "relationship":hasActivity})
    return jsonify({"listOfAttractionInformation":listOfAttractionInformation})
#  NISAM JOS ISKORISTILA FJU..A VERV BI TREBALO
@helpers.route("/removeOldUsers",methods=["GET"])
def removeOldUsers():
    query=f"""MATCH (user:User)
    WHERE NOT EXISTS ((:Hashtag)<-[:WANTS_TO_SEE]-(user))
    RETURN user.username"""
    resultList=list(db.execute_and_fetch(query))
    return jsonify(resultList)