from contextlib import nullcontext
from gqlalchemy import Memgraph

def recommendationColdStart():
    db= Memgraph("127.0.0.1", 7687)
    query=f""" MATCH (u:User)-[:WANTS_TO_SEE]->(h:Hashtag)<-[:HAS_HASHTAG]-(a:Attraction)
    WHERE NOT EXISTS ((u)-[:VISITED]->())
    WITH u.username AS username, a AS attraction, a.averageRate AS averageRating
    ORDER BY username, averageRating DESC
    WITH username, COLLECT({{attractionId: attraction.id, averageRating: averageRating}})[..5] AS topAttractions
    UNWIND topAttractions AS attraction
    RETURN username, attraction.attractionId, attraction.averageRating;
    """


    result=list(db.execute_and_fetch(query))
    user_attractions_dict = {}

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
        DELETE r """
        db.execute(query)
        query=f"""
        MATCH (u:User) WHERE u.username="{username}"
        MATCH (a:Attraction) WHERE a.id IN {lista}
        MERGE (a)-[r1:RECOMMENDED_FOR]->(u)
        RETURN a, u, r1;
        """
        db.execute(query)


    return

recommendationColdStart()
