import sys
from flask import Blueprint,render_template,jsonify,flash, request
from flask_jwt_extended import jwt_required
from app import app , bcrypt, db ,ma
from gqlalchemy import match
from gqlalchemy.query_builders.memgraph_query_builder import Operator

user= Blueprint("user",__name__,static_folder="static",template_folder="templates")
class AttractionSchema(ma.Schema):
    class Meta:
        fields = ('id','name','latitude','longitude','description','familyFriendly','durationOfVisit','parking','averageRate')
  
attraction_schema = AttractionSchema()
attractions_schema = AttractionSchema(many=True)


@user.route('/recommend/<string:userId>', methods=['GET']) 
@jwt_required()
def recommend(userId):
    query=f""" MATCH (u:User)<-[r:RECOMMENDED_FOR]-(a:Attraction) WHERE u.id="{userId}"
    RETURN a
    ORDER BY a.averageRate DESC
    """
    result=list(db.execute_and_fetch(query))
    recommendAttractions=[item["a"] for item in result]
    results = attractions_schema.dump(recommendAttractions)
    return jsonify(results)
  
  
   
@user.route('/nearYouRecommendation/<string:usersId>', methods=['GET']) 
@jwt_required()
def nearYouRecommendation(usersId):
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
RETURN a.id as id, a.name as name , udaljenost
ORDER BY udaljenost
LIMIT 10;
 """
          
    fetchNearestAttractions=db.execute_and_fetch(query)
    
    # listOfNearestAttractions=[]
    listaa=list(fetchNearestAttractions)
    # print(listaa)
    # for item in listaa:
    #     listOfNearestAttractions.append(item["a"])
    # print(listOfNearestAttractions)
    
    # results = attractions_schema.dump(listOfNearestAttractions)
    return jsonify(listaa)
    
@user.route('/planTrip', methods=['POST'])
# @user.route('/planTrip/<string:pickedCity>/<string:pickedAct>/<string:pickedDuration>/<string:pickedKm>/<int:parking>/<int:familyFriendly>/<string:maxDest>/<string:latitude>/<string:longitude>', methods=['GET'])
@jwt_required()
# mislim da ovde treba da ide get ipak
def planTrip():
    req_data = request.get_json()    
    pickedCity=req_data.get("pickedCity")
    pickedAct=req_data.get("pickedAct")
    pickedDuration=req_data.get("pickedDuration")
    pickedKm=req_data.get("pickedKm")
    familyFriendly=req_data.get("familyFriendly")
    maxDest=req_data.get("maxDest")
    latitude=req_data.get("latitude")
    longitude=req_data.get("longitude")
    
    
    duration=False
    parking=req_data.get("parking")
    maxDest=(int(maxDest))
    latitude=(float(latitude))
    longitude=(float(longitude))
    activities=pickedAct.split(',')
    if(pickedDuration!=""):
        duration=True
        durationH, durationM, durationS = map(int, pickedDuration.split(':'))
    pickedM=float(pickedKm)*1000
    
    query=""

    
    whereConditions=[]
    
    query+=f"""MATCH (c:City{{id:'{pickedCity}'}})-[r1:HAS_ATTRACTION]->(a:Attraction)
    OPTIONAL MATCH (a)-[r2:HAS_ACTIVITY]->(activity:Activity)
    WHERE size({activities}) = 0 OR (size({activities}) > 0 AND activity.id IN {activities})
    WITH a, COLLECT(activity) AS activitiesForAttraction,COLLECT(r2) AS rels
       """

    if familyFriendly:
        whereConditions.append("a.familyFriendly = true ")
        
    if parking:
        whereConditions.append("a.parking = true ")
        
    if whereConditions:
        query+="WHERE "+" AND ".join(whereConditions)
        
    query+= f""" WITH a, activitiesForAttraction,rels,
     CASE 
       WHEN size({activities}) > 0 
       THEN REDUCE(s = 0, x IN activitiesForAttraction | s + CASE WHEN x.id IN {activities} THEN 1 ELSE 0 END)
       ELSE 0
     END AS commonActivities
    WITH a, activitiesForAttraction, commonActivities,rels,
    
     REDUCE(s = 0.0, r IN rels | s + COALESCE(toInteger(split(coalesce(toString(r.durationOfActivity), ""), ":")[0])*3600 + toInteger(split(coalesce(toString(r.durationOfActivity), ""), ":")[1])*60 + toInteger(split(coalesce(toString(r.durationOfActivity), ""), ":")[2]), 0.0))+(a.durationOfVisit.hour * 3600 + a.durationOfVisit.minute * 60 + a.durationOfVisit.second) AS totalDuration,
        6371 * 2 * atan2(
        sqrt(
                sin((a.latitude - {latitude}) * 3.14 / 360) * 
                sin((a.latitude - {latitude}) * 3.14 / 360) +
                cos({latitude} * 3.14 / 180) * 
                cos(a.latitude * 3.14 / 180) * 
                sin((a.longitude - {longitude}) * 3.14 / 360) * 
                sin((a.longitude - {longitude}) * 3.14 / 360)
            ),
        sqrt(
                1 - sin((a.latitude - {latitude}) * 3.14 / 360) * 
                sin((a.latitude - {latitude}) * 3.14 / 360) +
                cos({latitude} * 3.14 / 180) * 
                cos(a.latitude * 3.14 / 180) * 
                sin((a.longitude - {longitude}) * 3.14 / 360) * 
                sin((a.longitude - {longitude}) * 3.14 / 360)
            )
        ) AS udaljenost """
    if (int(pickedKm)!=0):
        query+=f"""WHERE udaljenost<{pickedM}"""
        
    if(duration):
        if (int(pickedKm)==0):
            query+=f"""WHERE """
        else:
            query+=f"""AND """
            
        query+= f"""  totalDuration < ({durationH}* 3600+{durationM}*60+{durationS})
        """
    
    query+=f"""RETURN a.id as id, a.name as name, a.averageRate as avgRate , toInteger(totalDuration/3600) as houres, toInteger((totalDuration % 3600) / 60) as minutes,toInteger(totalDuration % 60) as seconds,
       commonActivities as matchedActivities,udaljenost/1000 as distaneInKm

        ORDER BY udaljenost,commonActivities DESC 
        """
    if(maxDest>0):
        query+=f"""LIMIT {maxDest} """
    
    print(query)
    p=list(db.execute_and_fetch(query))
    print(p)
    # recommendAttractions=[item["a"] for item in p]
    # results = attractions_schema.dump(recommendAttractions)
    return jsonify(p)
    
@user.route('/searchEngineAll/<string:userId>/<string:searchText>', methods=['GET'])
@jwt_required()

def searchEngineAll(userId,searchText):
    # userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
    # istorija,musteseeplaces,cultutralHeirtage,zabava
    listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
    useeWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]

    
    query=f"""
    WITH toLower("{searchText}") as searchText
    MATCH (c:City)-[:HAS_ATTRACTION]->(a:Attraction)
    WHERE toLower(c.name) = searchText
    OR toLower(a.name) STARTS WITH searchText
    OR toLower(a.name) CONTAINS searchText
    OR toLower(a.description) CONTAINS searchText
    WITH a,CASE WHEN toLower(c.name) = searchText THEN 1 ELSE 0 END as cityExists,
    CASE WHEN toLower(a.name) STARTS WITH searchText THEN 1 ELSE 0 END as nameStartsWith,
    CASE WHEN toLower(a.name) CONTAINS searchText THEN 1 ELSE 0 END as nameContains
    OPTIONAL MATCH (a)-[r:HAS_HASHTAG]-(h:Hashtag)
    WHERE h.name IN {useeWantsToSeehashtag}
    WITH a, cityExists, nameStartsWith, nameContains,COUNT(h) AS matchingHashtags
    RETURN a.name as name, a.id as id, cityExists, nameStartsWith,nameContains, COALESCE(matchingHashtags, 0) AS matchingHashtags
    ORDER BY cityExists DESC, nameStartsWith DESC,nameContains DESC,matchingHashtags DESC """
    listOfResult=list(db.execute_and_fetch(query))
    print(listOfResult[0]["name"])
    if(len(listOfResult)==1 and listOfResult[0]["name"] is None):
        listOfResult=[]
    return jsonify(listOfResult)
    
@user.route('/searchEngineAttractionName/<string:userId>/<string:searchText>', methods=['GET'])
@jwt_required()

def searchEngineAttractionName(userId,searchText):
    # userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
    listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
    userWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]

    query=f""" 
    WITH toLower("{searchText}") as searchText
MATCH (a:Attraction)
WHERE toLower(a.name) CONTAINS searchText
   OR toLower(a.description) CONTAINS searchText
WITH a,
    CASE WHEN toLower(a.name) STARTS WITH searchText THEN 1 ELSE 0 END as startsWithString,
    CASE WHEN toLower(a.name) CONTAINS searchText THEN 1 ELSE 0 END as containsString,
    CASE WHEN toLower(a.description) STARTS WITH searchText THEN 1 ELSE 0 END as descStartsWithString,
    CASE WHEN toLower(a.description) CONTAINS searchText THEN 1 ELSE 0 END as descContainsString,
    searchText
WITH a, startsWithString, containsString, descStartsWithString, descContainsString, searchText
OPTIONAL MATCH (a)-[r:HAS_HASHTAG]-(h:Hashtag)
WHERE h.name IN {userWantsToSeehashtag}
  AND (toLower(a.name) CONTAINS searchText OR toLower(a.description) CONTAINS searchText)
WITH a, startsWithString, containsString, descStartsWithString, descContainsString, searchText, COUNT(h) AS matchingHashtags
RETURN a.name as name ,a.id as id, startsWithString, containsString, descStartsWithString, descContainsString, matchingHashtags, a.averageRate
ORDER BY startsWithString DESC, containsString DESC, descStartsWithString DESC, descContainsString DESC, a.averageRate DESC;

    """
    listOfResult=list(db.execute_and_fetch(query))
    print(listOfResult[0]["name"])
    if(len(listOfResult)==1 and listOfResult[0]["name"] is None):
        listOfResult=[]
    return jsonify(listOfResult)
    
@user.route('/searchEngineHashtag/<string:userId>/<string:searchText>', methods=['GET'])
@jwt_required()
def searchEngineHashTag(userId,searchText):
    # userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
    listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
    userWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]
    # searchText="ist"
    query=f""" 
    WITH toLower("{searchText}") AS searchText
    MATCH (a:Attraction)-[:HAS_HASHTAG]->(h:Hashtag) 
    WHERE toLower(h.name) STARTS WITH searchText 
    WITH a, collect(h.name) as hashtags
    with a, REDUCE(s = 0, i IN hashtags | s + CASE WHEN i IN {userWantsToSeehashtag} THEN 1 ELSE 0 END) AS rezultat
    RETURN a.id as id, a.name as name ,rezultat,a.averageRate
    ORDER BY rezultat DESC, a.averageRate DESC
 """
    listOfResult=list(db.execute_and_fetch(query))
    print(listOfResult[0]["name"])
    if(len(listOfResult)==1 and listOfResult[0]["name"] is None):
        listOfResult=[]
    return jsonify(listOfResult)

@user.route('/searchEngineActivity/<string:userId>/<string:searchText>', methods=['GET'])
@jwt_required()

def searchEngineActivity(userId,searchText):
    # userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
    listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
    # userWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]
    # searchText="p"
    query=f""" 
    WITH toLower("{searchText}") AS searchText
    MATCH (a:Attraction)-[:HAS_ACTIVITY]->(h:Activity) 
    WHERE toLower(h.name) STARTS WITH searchText 
    with a, collect(h.name) as activities

    RETURN a.name as name , a.id as id ,a.averageRate,activities
    ORDER BY  a.averageRate DESC
 """
 
    listOfResult=list(db.execute_and_fetch(query))
    print(listOfResult[0]["name"])
    if(len(listOfResult)==1 and listOfResult[0]["name"] is None):
        listOfResult=[]
    return jsonify(listOfResult)
    
@user.route('/searchEngineCity/<string:userId>/<string:searchText>', methods=['GET'])
@jwt_required()

def searchEngineCity(userId,searchText):
    # userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
    listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
    userWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]
    # searchText="Nis"
    query=f""" 
    WITH toLower("{searchText}") AS searchText
    MATCH (a:Attraction)<-[:HAS_ATTRACTION]-(c:City) 
    WHERE toLower(c.name) = searchText 
    OPTIONAL MATCH (a)-[r:HAS_HASHTAG]-(h:Hashtag)
    WHERE h.name IN {userWantsToSeehashtag}
    WITH a,COUNT(h) AS matchingHashtags
    RETURN a.name as name, a.id as id , COALESCE(matchingHashtags, 0) AS matchingHashtags
    ORDER BY matchingHashtags DESC, a.averageRate DESC
 """
    listOfResult=list(db.execute_and_fetch(query))
    print(listOfResult[0]["name"])
    if(len(listOfResult)==1 and listOfResult[0]["name"] is None):
        listOfResult=[]
    return jsonify(listOfResult)  

@user.route('/searchEngineNotLoggedIn/<string:searchText>',methods=['GET']) 
def searchEngineNotLoggedIn(searchText):
    query=f""" WITH toLower("{searchText}") as searchText
    MATCH (c:City)-[:HAS_ATTRACTION]->(a:Attraction)
    WHERE toLower(c.name) = searchText
    OR toLower(a.name) STARTS WITH searchText
    OR toLower(a.name) CONTAINS searchText
    OR toLower(a.description) CONTAINS searchText
    WITH a,CASE WHEN toLower(c.name) = searchText THEN 1 ELSE 0 END as cityExists,
    CASE WHEN toLower(a.name) STARTS WITH searchText THEN 1 ELSE 0 END as nameStartsWith,
    CASE WHEN toLower(a.name) CONTAINS searchText THEN 1 ELSE 0 END as nameContains
    RETURN a.id as id ,a.name as name, cityExists, nameStartsWith,nameContains
    ORDER BY cityExists DESC ,nameStartsWith DESC ,nameContains DESC
    """
    listOfResult=list(db.execute_and_fetch(query))
    return jsonify(listOfResult)

    
    