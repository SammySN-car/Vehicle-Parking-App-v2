from Backend.utils.db import db
from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash,check_password_hash
import datetime
from flask_jwt_extended import create_access_token
from Backend.models.database import Users

class Register(Resource):
    def post(self):
        data=request.get_json()
        full_name=data.get('full_name')
        email_id=data.get('email_id')
        password=data.get('password')
        address=data.get('address')
        pincode=data.get('pincode')

        if not all([full_name,email_id,password,address,pincode]):
            return {'message':'Require all details'},400
        
        userd=Users.query.filter_by(email_id=email_id).first()
        if userd:
            return {"message":'User already exist'},409
        
        hashed_password=generate_password_hash(password)
        uses=Users(
            full_name=full_name,email_id=email_id,password=hashed_password,address=address,pincode=pincode
        )
        db.session.add(uses)
        db.session.commit()

        return {'message':'registered successfully'},201
    
class Login(Resource):
    def post(self):
        data=request.get_json()
        email_id=data.get('email_id')
        password=data.get('password')

        if not all([email_id,password]):
            return {'message':'require all details'},400
        
        user=Users.query.filter_by(email_id=email_id).first()
        if not user:
            return {"message":'wrong details'},401
        
        if not check_password_hash(user.password,password):
            return {"message":'wrong details'},401
        
        access_token=create_access_token(identity=str(user.id),expires_delta=datetime.timedelta(days=1))
        
        return {'message':'logged in','token':access_token,'role':user.role,'id':user.id},200
    
