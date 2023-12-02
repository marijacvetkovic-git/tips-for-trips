from ast import List
from gqlalchemy import Memgraph
from gqlalchemy.query_builders.memgraph_query_builder import Operator,Order
from gqlalchemy import match
from sklearn.cluster import KMeans
import numpy as py
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt



def recommendationKMeansClustering():
    db= Memgraph("127.0.0.1", 7687)
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
        
        
    query= f""" MATCH (u:User)-[r:VISITED]->(a:Attraction) 
    RETURN u.id,a.id
    ORDER BY u.id , r.rate DESC , r.dateAndTime DESC
    """
    userVisited=list(db.execute_and_fetch(query))
    dictioneryUserAttraction={}
    
    for item in userVisited:
        if item["u.id"] not in dictioneryUserAttraction.keys():
            dictioneryUserAttraction[item["u.id"]]=[]
        dictioneryUserAttraction[item["u.id"]].append(item["a.id"])
        
    vectors=list(dictioneryOfAttractionVector.values())
    x=py.array(vectors)  
    kmeansmodel=KMeans(n_clusters=8,init='k-means++',random_state=0)
    y_kmeans= kmeansmodel.fit_predict(x)
    data_with_clusters = py.column_stack((x, y_kmeans))
    i=0
    for vektor in dictioneryOfAttractionVector.items():
        vektor[1].append(y_kmeans[i])
        i=i+1
    
    userId="4fdcb146-f8f4-487a-9f1a-053ce40661ce"
    usersAttraction=dictioneryUserAttraction[userId]
    cluster=dictioneryOfAttractionVector[usersAttraction[0]][-1]
    kljucevi = [kljuc for kljuc, vektor in dictioneryOfAttractionVector.items() if vektor[-1] == cluster and kljuc not in usersAttraction]
    recommendedClusters=[]
    recommendedClusters.append(cluster)
    i=1
    
    while len(kljucevi)<5 and i<len(usersAttraction):
            cluster=dictioneryOfAttractionVector[usersAttraction[i]][-1]
            if cluster not in recommendedClusters:
                kljucevi.extend([kljuc for kljuc, vektor in dictioneryOfAttractionVector.items() if vektor[-1] == cluster])
                recommendedClusters.append(cluster)
            i+=1
    if len(kljucevi)<5 :
        remaining=5-len(kljucevi)
        query=f""" MATCH (u:User)-[:WANTS_TO_SEE]->(h:Hashtag)<-[:HAS_HASHTAG]-(a:Attraction) WHERE u.id='{userId}'AND a.id NOT IN {kljucevi} AND a.id NOT IN {usersAttraction}
        WITH a,u
        OPTIONAL MATCH (a)<-[r:VISITED]-(:User)
        WITH u,a, COALESCE(COLLECT(r.rate), [0]) AS ratings
        WITH u,a, REDUCE(s = 0, rating IN ratings | s + rating) AS sumRatings, SIZE(ratings) AS numRatings
        WITH u,a, 
        CASE WHEN numRatings > 0 THEN TOFLOAT(sumRatings) / TOFLOAT(numRatings) ELSE 0 END AS averageRating
        WITH u.username AS username, a AS attraction, averageRating
        ORDER BY username, averageRating DESC
        WITH username, COLLECT({{attractionId: attraction.id, averageRating: averageRating}})[..{remaining}] AS topAttractions
        UNWIND topAttractions AS attraction
        RETURN attraction.attractionId"""
        result=list(db.execute_and_fetch(query))
        kljucevi.append([item["attraction.attractionId"] for item in result])

    query=f""" MATCH (a:Attraction) WHERE a.id IN {kljucevi}
    WITH a
    OPTIONAL MATCH (a)<-[r:VISITED]-(:User)
    WITH a, COALESCE(COLLECT(r.rate), [0]) AS ratings
    WITH a, REDUCE(s = 0, rating IN ratings | s + rating) AS sumRatings, SIZE(ratings) AS numRatings
    WITH a, 
        CASE WHEN numRatings > 0 THEN TOFLOAT(sumRatings) / TOFLOAT(numRatings) ELSE 0 END AS averageRating
    WITH  a AS attraction, averageRating
    return attraction,averageRating
    ORDER BY  averageRating DESC
    LIMIT 5
    """



            

        
        

    


    
   
        
        
    
    
    
    
recommendationKMeansClustering()

        

    
        