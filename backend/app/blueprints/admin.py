import string
import uuid
from flask import Blueprint, redirect,render_template,jsonify,flash, request, url_for
from flask_jwt_extended import jwt_required

from app.forms import *
from app.models import HasActivity, HasAttraction, HasHashtag, HasImage, Image, Visited, WantsToSee

admin= Blueprint("admin",__name__,static_folder="static",template_folder="templates")

@admin.route("/addImage/<string:attractionId>",methods=['POST'])
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


# @admin.route("/getImages/<string:attractionId>",methods=['GET'])  
# def getImages(attractionId):
#     query=f""" MATCH (a:Attraction) WHERE a.id='{attractionId}'
#     OPTIONAL MATCH (a)-[r:HAS_IMAGE]->(i:Image)
#     return i.path as path
#     """
#     listOfImgPaths=[item["path"] for item in list(db.execute_and_fetch(query))]
    
#     if None in listOfImgPaths:
#         return jsonify({"Error":"No photos"}),206
    
#     return jsonify(listOfImgPaths)
        


    
    
@admin.route("/addAttraction",methods=['GET','POST'])
@jwt_required()

def addAttraction():
    form= AddAttractionForm()
    if form.validate_on_submit():
        attraction=Attraction(id=str(uuid.uuid4()),name=form.name.data,description=form.description.data,longitude=form.longitude.data,latitude=form.latitude.data,familyFriendly=form.family_friendly.data,parking=form.parking.data,durationOfVisit=form.duration_of_visit.data)
        attraction.save(db)

        flash(f'Your attraction is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addAttraction.html', title='Add attraction', form=form)

@admin.route("/createHashtag",methods=['GET','POST'])
@jwt_required()

def createHashtag():
    form = AddHashtagForm()
    if form.validate_on_submit():
        hashtag=Hashtag(id=str(uuid.uuid4()),name=form.name.data)
        hashtag.save(db)

        flash(f'Your type of attraction is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addHashtag.html', title='Add hashtag', form=form)
    
@admin.route("/createActivity",methods=['GET','POST'])
@jwt_required()

def createActivity():
    
    form = AddActivityForm()
    if form.validate_on_submit():
        activity=Activity(id=str(uuid.uuid4()),name=form.name.data)
        activity.save(db)

        flash(f'Your activity is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addActivity.html', title='Add activity', form=form)

@admin.route("/createCity",methods=['POST'])
@jwt_required()

def createCity():
    req_data = request.get_json()    
    form = AddCityForm(
    name=req_data.get("name"),
    description=req_data.get("description")
        
    )
    if form.validate_on_submit():
        city=City(id=str(uuid.uuid4()),name=form.name.data,description=form.description.data)
        city.save(db)

        return jsonify({"Message":"Grad dodat"}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206

@admin.route("/createRelationship_HAS_HASHTAG",methods=['GET','POST'])
@jwt_required()

def createRelationship_HAS_HASHTAG():
    form = AddHasHashForm()
    m=form.validate_on_submit()
    if m:
        
        HasHashtag(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1]).save(db)

        flash(f'Your relationship is added!','success')
        return redirect(url_for('createRelationship_HAS_HASHTAG'))
    
    
    return render_template('addHashashtag.html', title='Add has hastag', form=form)

@admin.route("/createRelationship_HAS_ACTIVITY",methods=['GET','POST'])
@jwt_required()
def createRelationship_HAS_ACTIVITY():
    form = AddHasActivityForm()
    if form.validate_on_submit():
        HasActivity(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1],durationOfActivity=form.duration_of_activity.data,experience=form.experience.data,minAge=form.minAge.data,maxAge=form.maxAge.data).save(db)

        flash(f'Your relationship is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addHasActivity.html', title='Add has hastag', form=form)  

@admin.route("/createRelationship_VISITED",methods=['GET','POST'])
@jwt_required()
def createRelationship_VISITED():
    form = AddVisitedForm()
    if form.validate_on_submit():
        Visited(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1],rate=form.rate.data,dateAndTime=datetime.datetime.now()).save(db)
        query=f""" MATCH (a:Attraction)<-[r:VISITED]-() WHERE a.id='{form.idOfAttraction.data}'
                   WITH a, AVG(r.rate) AS prosecnaOcena
                   SET a.averageRate = prosecnaOcena;
                   """
        db.execute(query)
        flash(f'Your relationship is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addVisited.html', title='Add has hastag', form=form)  


@admin.route("/createRelationship_WANTS_TO_SEE",methods=['GET','POST'])
@jwt_required()
def createRelationship_WANTS_TO_SEE():
    form = AddWantsToSeeForm()
    if form.validate_on_submit():
        WantsToSee(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1]).save(db)

        flash(f'Your relationship is added!','success')
        return redirect(url_for('home'))
    
    
    return render_template('addWantsToSee.html', title='Add has hastag', form=form)


@admin.route("/createRelationship_HAS_ATTRACTION",methods=['POST'])
@jwt_required()
def createRelationship_HAS_ATTRACTION():
    req_data = request.get_json() 
    form = AddHasAttractionForm(
    idOfCity=req_data.get("idOfCity"),
    idOfAttraction=req_data.get("idOfAttraction")
    )
    if form.validate_on_submit():
        HasAttraction(_start_node_id=form.tupleForResult[0],_end_node_id=form.tupleForResult[1]).save(db)

        flash(f'Your relationship is added!','success')
        return jsonify({"Message":"Relationship has_attraction is created"}),200
    else:
        errors = {"errors": form.errors}
        return jsonify(errors), 206