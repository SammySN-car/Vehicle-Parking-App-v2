from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity
from Backend.utils.db import db
from Backend.models.database import Users
from werkzeug.security import generate_password_hash,check_password_hash

class EditProfile(Resource):
    @jwt_required()
    def put(self,role):
        user_id=get_jwt_identity()
        data=request.get_json()
        password=data.get('password')
        full_name=data.get('full_name')
        address=data.get('address')
        pincode=data.get('pincode')

        if not all([full_name,password,address,pincode]):
            return {'message':'Fill all details'},400
        
        hashed_password=generate_password_hash(password)

        userd=Users.query.get(user_id)
        userd.full_name=full_name
        userd.address=address
        userd.pincode=pincode
        userd.password=hashed_password
        db.session.commit()

        return {'message':'details have been updated'},200
    
    @jwt_required()
    def get(self,role):
        user_id=get_jwt_identity()

        userd=Users.query.get(user_id)
        user_details={'full_name':userd.full_name,'address':userd.address,'pincode':userd.pincode}

        return{"message":"here are the details",'user_details':user_details},200