
from app import db
from flask import Blueprint,jsonify




helpers= Blueprint("helpers",__name__,static_folder="static",template_folder="templates")

@helpers.route("/getHashtags", methods=['GET'])
def getHashtags():
    query="MATCH (h:Hashtag) return h.id as id ,h.name as name"
    listOfHashtags=list(db.execute_and_fetch(query))
    print(listOfHashtags)
    p=jsonify(listOfHashtags)
    print(p)
    return p