import sys
from flask import Blueprint,render_template,jsonify,flash
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


@user.route('/newUsercoldStartRecommendation/<string:userId>', methods=['GET']) 
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
RETURN a, udaljenost
ORDER BY udaljenost
LIMIT 10;
 """
          
    fetchNearestAttractions=db.execute_and_fetch(query)
    
    listOfNearestAttractions=[]
    listaa=list(fetchNearestAttractions)
    print(listaa)
    for item in listaa:
        listOfNearestAttractions.userend(item["a"])
    print(listOfNearestAttractions)
    
    results = attractions_schema.dump(listOfNearestAttractions)
    return jsonify(results)
    
@user.route('/planTrip', methods=['POST'])
@jwt_required()
# mislim da ovde treba da ide get ipak
def planTrip():
    distanceKm=1000000000000000
    cityName="Nis" 
    # mora destinacija da se odabere
    usersLatitude=45
    usersLongitude=45
    activities=[]
    durationH=444444
    durationM=45
    durationS=0
    duration=True
    familyFiendly=True
    parking=True
    # experience=True
    maxDestinations=4
    query=""
    if distanceKm==-1:
        distanceKm=sys.float_info.max
    
    whereConditions=[]
    
    query+=f"""MATCH (c:City{{name:'{cityName}'}})-[r1:HAS_ATTRACTION]->(a:Attraction)
    OPTIONAL MATCH (a)-[r2:HAS_ACTIVITY]->(activity:Activity)
    WHERE size({activities}) = 0 OR (size({activities}) > 0 AND activity.name IN {activities})
    WITH a, COLLECT(activity) AS activitiesForAttraction,COLLECT(r2) AS rels
       """

    if familyFiendly:
        whereConditions.append("a.familyFriendly = true ")
        
    if parking:
        whereConditions.append("a.parking = true ")
        
    if whereConditions:
        query+="WHERE "+" AND ".join(whereConditions)
        
    query+= f""" WITH a, activitiesForAttraction,rels,
     CASE 
       WHEN size({activities}) > 0 
       THEN REDUCE(s = 0, x IN activitiesForAttraction | s + CASE WHEN x.name IN {activities} THEN 1 ELSE 0 END)
       ELSE 0
     END AS commonActivities
    WITH a, activitiesForAttraction, commonActivities,rels,
    
     REDUCE(s = 0.0, r IN rels | s + COALESCE(toInteger(split(coalesce(toString(r.durationOfActivity), ""), ":")[0])*3600 + toInteger(split(coalesce(toString(r.durationOfActivity), ""), ":")[1])*60 + toInteger(split(coalesce(toString(r.durationOfActivity), ""), ":")[2]), 0.0))+(a.durationOfVisit.hour * 3600 + a.durationOfVisit.minute * 60 + a.durationOfVisit.second) AS totalDuration,
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
        WHERE udaljenost<{distanceKm}"""
        
    if(duration):
        query+= f""" AND totalDuration < ({durationH}* 3600+{durationM}*60+{durationS})
        """
    
    query+=f"""RETURN a,totalDuration,udaljenost,commonActivities
        ORDER BY udaljenost,commonActivities DESC 
        """
    if(maxDestinations>0):
        query+=f"""LIMIT {maxDestinations} """
    
    print(query)
    p=list(db.execute_and_fetch(query))
    print(p)
    recommendAttractions=[item["a"] for item in p]
    results = attractions_schema.dump(recommendAttractions)
    return jsonify(results)
    
@user.route('/serachEngineAll/<string:userId>', methods=['POST','GET'])
def serachEngineAll(userId):
    # userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
    # istorija,musteseeplaces,cultutralHeirtage,zabava
    listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
    useeWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]

    dummyString="c"
    query=f"""
    WITH toLower("{dummyString}") as dummystring
    MATCH (c:City)-[:HAS_ATTRACTION]->(a:Attraction)
    WHERE toLower(c.name) = dummystring
    OR toLower(a.name) STARTS WITH dummystring
    OR toLower(a.name) CONTAINS dummystring
    OR toLower(a.description) CONTAINS dummystring
    WITH a,CASE WHEN toLower(c.name) = dummystring THEN 1 ELSE 0 END as cityExists,
    CASE WHEN toLower(a.name) STARTS WITH dummystring THEN 1 ELSE 0 END as nameStartsWith,
    CASE WHEN toLower(a.name) CONTAINS dummystring THEN 1 ELSE 0 END as nameContains
    OPTIONAL MATCH (a)-[r:HAS_HASHTAG]-(h:Hashtag)
    WHERE h.name IN {useeWantsToSeehashtag}
    WITH a, cityExists, nameStartsWith, nameContains,COUNT(h) AS matchingHashtags
    RETURN a, cityExists, nameStartsWith,nameContains, COALESCE(matchingHashtags, 0) AS matchingHashtags
    ORDER BY cityExists DESC, nameStartsWith DESC,nameContains DESC,matchingHashtags DESC """
    p= list(db.execute_and_fetch(query))
    listOfResults=[item["a"] for item in p]
    results = attractions_schema.dump(listOfResults)
    return jsonify(results)
    
@user.route('/searchEngineAttractionName/<string:userId>', methods=['POST','GET'])
def searchEngineAttractionName(userId):
    # userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
    listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
    userWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]
    dummyString="va"

    query=f""" 
    WITH toLower("{dummyString}") as dummyString
    MATCH (a:Attraction)
    WHERE toLower(a.name) CONTAINS dummyString
    OR toLower(a.description) CONTAINS dummyString
    WITH a,
        CASE WHEN toLower(a.name) STARTS WITH dummyString THEN 1 ELSE 0 END as startsWithString,
        CASE WHEN toLower(a.name) CONTAINS dummyString THEN 1 ELSE 0 END as containsString,
        CASE WHEN toLower(a.description) STARTS WITH dummyString THEN 1 ELSE 0 END as descStartsWithString,
        CASE WHEN toLower(a.description) CONTAINS dummyString THEN 1 ELSE 0 END as descContainsString,
        dummyString
    WITH a, startsWithString, containsString, descStartsWithString, descContainsString, dummyString
    OPTIONAL MATCH (a)-[r:HAS_HASHTAG]-(h:Hashtag)
    WHERE h.name IN {userWantsToSeehashtag}
    AND (toLower(a.name) CONTAINS dummyString OR toLower(a.description) CONTAINS dummyString)
    WITH a, startsWithString, containsString, descStartsWithString, descContainsString, dummyString, COUNT(h) AS matchingHashtags, h
    RETURN a, startsWithString, containsString, descStartsWithString, descContainsString, COUNT(h) AS matchingHashtags, a.averageRate
    ORDER BY startsWithString DESC, containsString DESC, descStartsWithString DESC, descContainsString DESC, a.averageRate DESC

    """
    p= list(db.execute_and_fetch(query))
    listOfResults=[item["a"] for item in p]
    results = attractions_schema.dump(listOfResults)
    return jsonify(results)
    
@user.route('/searchEngineHashTag/<string:userId>', methods=['POST','GET'])
def searchEngineHashTag(userId):
    # userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
    listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
    userWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]
    dummyString="ist"
    query=f""" 
    WITH toLower("{dummyString}") AS dummyString
    MATCH (a:Attraction)-[:HAS_HASHTAG]->(h:Hashtag) 
    WHERE toLower(h.name) STARTS WITH dummyString 
    WITH a, collect(h.name) as hashtags
    with a, REDUCE(s = 0, i IN hashtags | s + CASE WHEN i IN {userWantsToSeehashtag} THEN 1 ELSE 0 END) AS rezultat
    RETURN a,rezultat,a.averageRate
    ORDER BY rezultat DESC, a.averageRate DESC
 """
    p= list(db.execute_and_fetch(query))
    listOfResults=[item["a"] for item in p]
    results = attractions_schema.dump(listOfResults)
    return jsonify(results)

@user.route('/searchEngineActivity/<string:userId>', methods=['POST','GET'])
def searchEngineActivity(userId):
    # userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
    listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
    userWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]
    dummyString="p"
    query=f""" 
    WITH toLower("{dummyString}") AS dummyString
    MATCH (a:Attraction)-[:HAS_ACTIVITY]->(h:Activity) 
    WHERE toLower(h.name) STARTS WITH dummyString 
    with a, collect(h.name) as activities

    RETURN a  ,a.averageRate,activities
    ORDER BY  a.averageRate DESC
 """
    p= list(db.execute_and_fetch(query))
    listOfResults=[item["a"] for item in p]
    results = attractions_schema.dump(listOfResults)
    return jsonify(results)
    
@user.route('/searchEngineCity/<string:userId>', methods=['POST','GET'])
def searchEngineCity(userId):
    # userId="9f130ecc-ab78-4d07-964a-1a38bc131675"
    listOfHashtags=list(db.execute_and_fetch(query=f""" MATCH (u:User)-[r:WANTS_TO_SEE]->(h:Hashtag) WHERE u.id="{userId}" return h.name """))
    userWantsToSeehashtag=[item["h.name"] for item in listOfHashtags]
    dummyString="Nis"
    query=f""" 
    WITH toLower("{dummyString}") AS dummyString
    MATCH (a:Attraction)<-[:HAS_ATTRACTION]-(c:City) 
    WHERE toLower(c.name) = dummyString 
    OPTIONAL MATCH (a)-[r:HAS_HASHTAG]-(h:Hashtag)
    WHERE h.name IN {userWantsToSeehashtag}
    WITH a,COUNT(h) AS matchingHashtags
    RETURN a, COALESCE(matchingHashtags, 0) AS matchingHashtags
    ORDER BY matchingHashtags DESC, a.averageRate DESC
 """
    p= list(db.execute_and_fetch(query))
    listOfResults=[item["a"] for item in p]
    results = attractions_schema.dump(listOfResults)
    return jsonify(results)   

    

    
    