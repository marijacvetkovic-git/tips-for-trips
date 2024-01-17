from datetime import date
import datetime
from time import strptime
from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, FloatField, IntegerField, StringField,PasswordField,SubmitField,DateField, ValidationError,TimeField
from wtforms.validators import DataRequired, Length, EqualTo,Email
from app import db
from gqlalchemy import match
from gqlalchemy.query_builders.memgraph_query_builder import Operator

from app.models import Activity, Attraction, City, Hashtag, User

class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(),Length(min=2,max=50)])
    email= StringField('Email', validators=[DataRequired(), Email()] )
    password= PasswordField('Password', validators=[DataRequired()])
    confirm_password=PasswordField('Confirm password', validators=[DataRequired(),EqualTo('password')])
    dateofbirth=DateField('Date of Birth', validators=[DataRequired()])
    longitude=FloatField('Longitude', validators=[DataRequired()])
    latitude=FloatField('Latitude', validators=[DataRequired()])
    submit=SubmitField('Register')
  
    def validate_username(self,username):
        users=db.execute_and_fetch(
        "MATCH (u:User {username: $username}) RETURN u.username ;",
       {"username": username.data}
        )
        p=list(users)
        print(len(list(users)))
        
        if p:
            raise ValidationError('User with specific username already exist')
        
    def validate_email(self,email):
        query=f"""MATCH (u:User{{email:'{email.data}'}}) RETURN u"""
        users= db.execute_and_fetch(query)
        p=list(users)
        if p:
            raise ValidationError('User with specific email already exist')
    
    def validate_dateofbirth(self, dateofbirth):
        min_date = date.min
        max_date = date.today()
        date_object = date.fromisoformat(dateofbirth.data)

        if date_object < min_date or date_object > max_date:
            raise ValidationError('The date of birth must not be in the future.')
    
    
class LogInForm(FlaskForm):
    
    username=StringField('Username', validators=[DataRequired(),Length(min=2,max=50)])
    password= PasswordField('Password', validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    
class AddAttractionForm(FlaskForm):
    def validate_longitude(formica,l):
        p=formica.longitude.data
        l=formica.latitude.data
        attractions=(
          match()
          .node(labels="Attraction",variable="a")
          .where(item="a.longitude",operator=Operator.EQUAL,literal=formica.longitude.data)
          .and_where(item="a.latitude",operator=Operator.EQUAL,literal=formica.latitude.data)
          .return_(("a","attraction"))
          .execute()
          )
        listOfAttractions=list(attractions)
        if listOfAttractions:
            raise ValidationError('Some attraction already exists at that location') 
        attractions=(
          match()
          .node(labels="Attraction",variable="a")
          .where(item="a.name",operator=Operator.EQUAL,literal=formica.name.data)
          .return_(("a","attraction"))
          .execute()
          )
        listOfAttractions=list(attractions)

        if listOfAttractions:
            raise ValidationError('Some attraction already exists with that name') 
        
            
    name=StringField('Name', validators=[DataRequired()])
    description= StringField('Description', validators=[DataRequired()])
    longitude=FloatField('Longitude', validators=[DataRequired(),validate_longitude])
    latitude=FloatField('Latitude', validators=[DataRequired(),validate_longitude])
    duration_of_visit=TimeField('Duration of visit', validators=[DataRequired()])
    parking=BooleanField("Parking")
    family_friendly=BooleanField("Family friendly")
    submit = SubmitField('Add')
    
class AddHashtagForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add')
    
    def validate_name(self,name): 
        
        hashtags=(
          match()
          .node(labels="Hashtag",variable="hashtag")
          .where(item="hashtag.name",operator=Operator.EQUAL,literal=name.data)
          .return_(("hashtag","hashtag"))
          .execute()
          )
        listOfhashtags=list(hashtags)
        if listOfhashtags:
            raise ValidationError('Hashtag with that name already exists !')
  
class AddActivityForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Add')
    
    def validate_name(self,name): 
        activities=(
          match()
          .node(labels="Activity",variable="a")
          .where(item="a.name",operator=Operator.EQUAL,literal=name.data)
          .return_(("a","activity"))
          .execute()
          )
        listOfactivities=list(activities)
        if listOfactivities:
            raise ValidationError('Activity with that name already exists !')
  
class AddCityForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    description=StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Add')
    
    def validate_name(self,name): 
        cities=(
          match()
          .node(labels="City",variable="c")
          .where(item="c.name",operator=Operator.EQUAL,literal=name.data)
          .return_(("c","city"))
          .execute()
          )
        listOfCities=list(cities)
        if listOfCities:
            raise ValidationError('City with that name already exists !')
        
class AddHasHashForm(FlaskForm):
    idOfAttraction=StringField("Id of attraction",validators=[DataRequired()])
    idOfHashtag=StringField("Id of hashtag",validators=[DataRequired()])
    submit = SubmitField('Add')
    tupleForResult=("","")
    
    def validate_idOfAttraction(form,nzm):
        attractions=(
            match()
            .node(labels="Attraction",variable="attraction")
            .where(item="attraction.id",operator=Operator.EQUAL,literal=form.idOfAttraction.data)
            .return_("attraction")
            .execute()    
        )
        listOfAttractions=list(attractions)
        if not listOfAttractions:
            raise ValidationError('Attraction with specific id does not exist!')
        attraction:Attraction =listOfAttractions[0]["attraction"]
        idOfAttraction=attraction._id
       
        hashtags=(
            match()
            .node(labels="Hashtag",variable="hashtag")
            .where(item="hashtag.id",operator=Operator.EQUAL,literal=form.idOfHashtag.data)
            .return_("hashtag")
            .execute()    
        )
        listOfhashtags=list(hashtags)
        if not listOfhashtags:
            raise ValidationError('Hashtag with specific id does not exist!')
        hashtag:Hashtag =listOfhashtags[0]["hashtag"]
        idOfHashtag=hashtag._id
        
        
        hasHashtag=(
            match()
            .node(labels="Attraction",variable="attraction",id=form.idOfAttraction.data)
            .to(relationship_type="HAS_HASHTAG")
            .node(labels="Hashtag",variable="hashtag",id=form.idOfHashtag.data)
            .return_(results=["attraction","hashtag"])
            .execute()
        )
        listOfhasHashtag=list(hasHashtag)
        if listOfhasHashtag:
            raise ValidationError('Attraction with specific id already has hastag with specific id !')
        form.tupleForResult=(idOfAttraction,idOfHashtag)
            
class AddHasActivityForm(FlaskForm):
    idOfAttraction=StringField("Id of attraction",validators=[DataRequired()])
    idOfActivity=StringField("Id of activity",validators=[DataRequired()])
    duration_of_activity=TimeField('Duration of activity', validators=[DataRequired()])
    experience=BooleanField("Experience")
    minAge=IntegerField("Min age",validators=[DataRequired()])
    maxAge=IntegerField("Max age",validators=[DataRequired()])
    submit = SubmitField('Add')
    tupleForResult=("","")
    
   
    
    def validate_idOfAttraction(form,nzm):
        attractions=(
            match()
            .node(labels="Attraction",variable="attraction")
            .where(item="attraction.id",operator=Operator.EQUAL,literal=form.idOfAttraction.data)
            .return_("attraction")
            .execute()    
        )
        listOfAttractions=list(attractions)
        if not listOfAttractions:
            raise ValidationError('Attraction with specific id does not exist!')
        attraction:Attraction =listOfAttractions[0]["attraction"]
        idOfAttraction=attraction._id
       
        activities=(
            match()
            .node(labels="Activity",variable="activity")
            .where(item="activity.id",operator=Operator.EQUAL,literal=form.idOfActivity.data)
            .return_("activity")
            .execute()    
        )
        listOfactivities=list(activities)
        if not listOfactivities:
            raise ValidationError('Activity with specific id does not exist!')
        activity:Activity =listOfactivities[0]["activity"]
        idOfActivity=activity._id
        
        
        hasActivity=(
            match()
            .node(labels="Attraction",variable="attraction",id=form.idOfAttraction.data)
            .to(relationship_type="HAS_ACTIVITY")
            .node(labels="Activity",variable="activity",id=form.idOfActivity.data)
            .return_(results=["attraction","activity"])
            .execute()
        )
        listOfhasActivity=list(hasActivity)
        if listOfhasActivity:
            raise ValidationError('Attraction with specific id already has activity with specific id !')
        form.tupleForResult=(idOfAttraction,idOfActivity)
              
class AddVisitedForm(FlaskForm):
    idOfAttraction=StringField("Id of attraction",validators=[DataRequired()])
    idOfUser=StringField("Id of user",validators=[DataRequired()])
    rate=IntegerField("Rate visit",validators=[DataRequired()])
    submit = SubmitField('Add')
    tupleForResult=("","")
    
    def validate_idOfAttraction(form,nzm):
        attractions=(
            match()
            .node(labels="Attraction",variable="attraction")
            .where(item="attraction.id",operator=Operator.EQUAL,literal=form.idOfAttraction.data)
            .return_("attraction")
            .execute()    
        )
        listOfAttractions=list(attractions)
        if not listOfAttractions:
            raise ValidationError('Attraction with specific id does not exist!')
        attraction:Attraction =listOfAttractions[0]["attraction"]
        idOfAttraction=attraction._id
       
        users=(
            match()
            .node(labels="User",variable="user")
            .where(item="user.id",operator=Operator.EQUAL,literal=form.idOfUser.data)
            .return_("user")
            .execute()    
        )
        listOfusers=list(users)
        if not listOfusers:
            raise ValidationError('User with specific id does not exist!')
        user:Hashtag =listOfusers[0]["user"]
        idOfUser=user._id
        
        
        visited=(
            match()
            .node(labels="User",variable="user",id=form.idOfUser.data)
            .to(relationship_type="VISITED")
            .node(labels="Attraction",variable="attraction",id=form.idOfAttraction.data)
            .return_(results=["user","attraction"])
            .execute()
        )
        listOfvisits=list(visited)
        if listOfvisits:
            raise ValidationError('User with specific id already visited attraction with specific id !')
        form.tupleForResult=(idOfUser,idOfAttraction)
  
class AddWantsToSeeForm(FlaskForm):
    idOfUser=StringField("Id of user",validators=[DataRequired()])
    idsOfHashtags=StringField("Ids of hashtags",validators=[DataRequired()])
    submit = SubmitField('Add')
    tupleForResult=("",[])
    def validate_idOfUser(form,nzm):
        print(form.idsOfHashtags.data)
        users=(
            match()
            .node(labels="User",variable="user")
            .where(item="user.id",operator=Operator.EQUAL,literal=form.idOfUser.data)
            .return_("user")
            .execute()    
        )
        listOfUsers=list(users)
        if not listOfUsers:
            raise ValidationError('User with specific id does not exist!')
        user:User =listOfUsers[0]["user"]
        idOfUser=user._id
        listOfIdsHashtag = form.idsOfHashtags.data.split(',')
        listToReturn=[]

        for hashtag in listOfIdsHashtag:
            hashtags=(
                match()
                .node(labels="Hashtag",variable="hashtag")
                .where(item="hashtag.id",operator=Operator.EQUAL,literal=hashtag)
                .return_("hashtag")
                .execute()    
            )
            listOfhashtags=list(hashtags)
            if not listOfhashtags:
                raise ValidationError('Hashtag with specific id does not exist!')
            h:Hashtag =listOfhashtags[0]["hashtag"]
            listToReturn.append(h._id)
        
        for hashtag in listOfIdsHashtag:
            wantsToSee=(
                match()
                .node(labels="User",variable="user",id=form.idOfUser.data)
                .to(relationship_type="WANTS_TO_SEE")
                .node(labels="Hashtag",variable="hashtag",id=hashtag)
                .return_(results=["user","hashtag"])
                .execute()
            )
            listOfwantsToSee=list(wantsToSee)
            if listOfwantsToSee:
                raise ValidationError('User with specific id already has hastag with specific id !')
        form.tupleForResult=(idOfUser,listToReturn)
    
class AddHasAttractionForm(FlaskForm):
    idOfCity=StringField("Id of city",validators=[DataRequired()])
    idOfAttraction=StringField("Id of attraction",validators=[DataRequired()])
    submit = SubmitField('Add')
    tupleForResult=("","")
    
    def validate_idOfCity(form,nzm):
        cities=(
            match()
            .node(labels="City",variable="city")
            .where(item="city.id",operator=Operator.EQUAL,literal=form.idOfCity.data)
            .return_("city")
            .execute()    
        )
        listOfCities=list(cities)
        if not listOfCities:
            raise ValidationError('City with specific id does not exist!')
        city:City =listOfCities[0]["city"]
        idOfCity=city._id
       
        attractions=(
            match()
            .node(labels="Attraction",variable="attraction")
            .where(item="attraction.id",operator=Operator.EQUAL,literal=form.idOfAttraction.data)
            .return_("attraction")
            .execute()    
        )
        listOfattractions=list(attractions)
        if not listOfattractions:
            raise ValidationError('Attraction with specific id does not exist!')
        attraction:Attraction =listOfattractions[0]["attraction"]
        idOfAttraction=attraction._id
        
        
        hasAttraction=(
            match()
            .node(labels="City",variable="city",id=form.idOfCity.data)
            .to(relationship_type="HAS_ATTRACTION")
            .node(labels="Attraction",variable="attraction",id=form.idOfAttraction.data)
            .return_(results=["city","attraction"])
            .execute()
        )
        listOfHasAttraction=list(hasAttraction)
        if listOfHasAttraction:
            raise ValidationError('City with specific id already has attraction with specific id !')
        form.tupleForResult=(idOfCity,idOfAttraction)
 
class DeleteHasHashtagForm(FlaskForm):
    idOfAttraction=StringField("Id of attraction",validators=[DataRequired()])
    idOfHashtag=StringField("Id of hashtag",validators=[DataRequired()])

    
    def validate_idOfAttraction(form,nzm):
        attractions=(
            match()
            .node(labels="Attraction",variable="attraction")
            .where(item="attraction.id",operator=Operator.EQUAL,literal=form.idOfAttraction.data)
            .return_("attraction")
            .execute()    
        )
        listOfAttractions=list(attractions)
        if not listOfAttractions:
            raise ValidationError('Attraction with specific id does not exist!')
        attraction:Attraction =listOfAttractions[0]["attraction"]
        idOfAttraction=attraction._id
       
        hashtags=(
            match()
            .node(labels="Hashtag",variable="hashtag")
            .where(item="hashtag.id",operator=Operator.EQUAL,literal=form.idOfHashtag.data)
            .return_("hashtag")
            .execute()    
        )
        listOfhashtags=list(hashtags)
        if not listOfhashtags:
            raise ValidationError('Hashtag with specific id does not exist!')
        hashtag:Hashtag =listOfhashtags[0]["hashtag"]
        idOfHashtag=hashtag._id
        
        
        hasHashtag=(
            match()
            .node(labels="Attraction",variable="attraction",id=form.idOfAttraction.data)
            .to(relationship_type="HAS_HASHTAG")
            .node(labels="Hashtag",variable="hashtag",id=form.idOfHashtag.data)
            .return_(results=["attraction","hashtag"])
            .execute()
        )
        listOfhasHashtag=list(hasHashtag)
        if not listOfhasHashtag:
            raise ValidationError('Attraction with specific id does not have hastag with specific id !')
        form.tupleForResult=(idOfAttraction,idOfHashtag)
          
class DeleteHasActivityForm(FlaskForm):
    idOfAttraction=StringField("Id of attraction",validators=[DataRequired()])
    idOfActivity=StringField("Id of activity",validators=[DataRequired()])

    def validate_idOfAttraction(form,nzm):
        attractions=(
            match()
            .node(labels="Attraction",variable="attraction")
            .where(item="attraction.id",operator=Operator.EQUAL,literal=form.idOfAttraction.data)
            .return_("attraction")
            .execute()    
        )
        listOfAttractions=list(attractions)
        if not listOfAttractions:
            raise ValidationError('Attraction with specific id does not exist!')
        attraction:Attraction =listOfAttractions[0]["attraction"]
       
        activities=(
            match()
            .node(labels="Activity",variable="activity")
            .where(item="activity.id",operator=Operator.EQUAL,literal=form.idOfActivity.data)
            .return_("activity")
            .execute()    
        )
        listOfactivities=list(activities)
        if not listOfactivities:
            raise ValidationError('Activity with specific id does not exist!')
        activity:Activity =listOfactivities[0]["activity"]
        
        
        hasActivity=(
            match()
            .node(labels="Attraction",variable="attraction",id=form.idOfAttraction.data)
            .to(relationship_type="HAS_ACTIVITY")
            .node(labels="Activity",variable="activity",id=form.idOfActivity.data)
            .return_(results=["attraction","activity"])
            .execute()
        )
        listOfhasActivity=list(hasActivity)
        if not listOfhasActivity:
            raise ValidationError('Attraction with specific id already does not have activity with specific id !')

class DeleteVisitedForm(FlaskForm):
    idOfAttraction=StringField("Id of attraction",validators=[DataRequired()])
    idOfUser=StringField("Id of user",validators=[DataRequired()])
    
    def validate_idOfAttraction(form,nzm):
        attractions=(
            match()
            .node(labels="Attraction",variable="attraction")
            .where(item="attraction.id",operator=Operator.EQUAL,literal=form.idOfAttraction.data)
            .return_("attraction")
            .execute()    
        )
        listOfAttractions=list(attractions)
        if not listOfAttractions:
            raise ValidationError('Attraction with specific id does not exist!')
        attraction:Attraction =listOfAttractions[0]["attraction"]
        idOfAttraction=attraction._id
       
        users=(
            match()
            .node(labels="User",variable="user")
            .where(item="user.id",operator=Operator.EQUAL,literal=form.idOfUser.data)
            .return_("user")
            .execute()    
        )
        listOfusers=list(users)
        if not listOfusers:
            raise ValidationError('User with specific id does not exist!')
        user:Hashtag =listOfusers[0]["user"]
        idOfUser=user._id
        
        
        visited=(
            match()
            .node(labels="User",variable="user",id=form.idOfUser.data)
            .to(relationship_type="VISITED")
            .node(labels="Attraction",variable="attraction",id=form.idOfAttraction.data)
            .return_(results=["user","attraction"])
            .execute()
        )
        listOfvisits=list(visited)
        if not listOfvisits:
            raise ValidationError('User with specific id already did not visit attraction with specific id !')
        
class DeleteHasAttractionForm(FlaskForm):
    idOfCity=StringField("Id of city",validators=[DataRequired()])
    idOfAttraction=StringField("Id of attraction",validators=[DataRequired()])
    submit = SubmitField('Delete')
    
    def validate_idOfCity(form,nzm):
        cities=(
            match()
            .node(labels="City",variable="city")
            .where(item="city.id",operator=Operator.EQUAL,literal=form.idOfCity.data)
            .return_("city")
            .execute()    
        )
        listOfCities=list(cities)
        if not listOfCities:
            raise ValidationError('City with specific id does not exist!')
       
        attractions=(
            match()
            .node(labels="Attraction",variable="attraction")
            .where(item="attraction.id",operator=Operator.EQUAL,literal=form.idOfAttraction.data)
            .return_("attraction")
            .execute()    
        )
        listOfattractions=list(attractions)
        if not listOfattractions:
            raise ValidationError('Attraction with specific id does not exist!')
        
        
        hasAttraction=(
            match()
            .node(labels="City",variable="city",id=form.idOfCity.data)
            .to(relationship_type="HAS_ATTRACTION")
            .node(labels="Attraction",variable="attraction",id=form.idOfAttraction.data)
            .return_(results=["city","attraction"])
            .execute()
        )
        listOfHasAttraction=list(hasAttraction)
        if not listOfHasAttraction:
            raise ValidationError('City with specific id does not have attraction with specific id !')
