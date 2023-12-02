from contextlib import nullcontext
from gqlalchemy import Memgraph

def recommendationColdStart():
    db= Memgraph("127.0.0.1", 7687)
    query=f""" MATCH (u:User)-[:WANTS_TO_SEE]->(h:Hashtag)<-[:HAS_HASHTAG]-(a:Attraction)
    WHERE NOT EXISTS ((u)-[:VISITED]->())
    WITH a,u
    OPTIONAL MATCH (a)<-[r:VISITED]-(:User)
    WITH u,a, COALESCE(COLLECT(r.rate), [0]) AS ratings
    WITH u,a, REDUCE(s = 0, rating IN ratings | s + rating) AS sumRatings, SIZE(ratings) AS numRatings
    WITH u,a, 
        CASE WHEN numRatings > 0 THEN TOFLOAT(sumRatings) / TOFLOAT(numRatings) ELSE 0 END AS averageRating
    WITH u.username AS username, a AS attraction, averageRating
    ORDER BY username, averageRating DESC
    WITH username, COLLECT({{attractionId: attraction.id, averageRating: averageRating}})[..5] AS topAttractions
    UNWIND topAttractions AS attraction
    RETURN username, attraction.attractionId, attraction.averageRating;"""


    result=list(db.execute_and_fetch(query))
    user_attractions_dict = {}
    # if result[0]["username"]==None:
    #     return
    # AND NOT EXISTS ((:Attraction)-[:RECOMMENDED_FOR]->(u))
    for result in list(result):
        username = result['username']
        attraction_id = result['attraction.attractionId']
        
        if username not in user_attractions_dict:
            user_attractions_dict[username] = [attraction_id]
        else:
            user_attractions_dict[username].append(attraction_id)
    queries=[]

    for username in user_attractions_dict:
        lista=user_attractions_dict[username]
        query=f"""
        MATCH (:Attraction)-[r:RECOMMENDED_FOR]->(u:User) WHERE u.username="{username}"
        DELETE r
        WITH u
        MATCH (a:Attraction) WHERE a.id IN {lista}
        MERGE (a)-[r1:RECOMMENDED_FOR]->(u)
        RETURN a, u, r1;

        """
        queries.append(query)

    for query in queries:
        result=db.execute_and_fetch(query)
    return

recommendationColdStart()
#TODO: Da li samo u atrakciji da cuvam prosecnu ocenu umesto da racunma ovo svaki put...ili da ostane ovako pa da uzmem pagerank da radim gde ce tezina grane rate da bude