from Backend.utils.db import db
from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash,check_password_hash
from Backend.models.database import Users

class ForgetPass(Resource):
    def post(self):
        data=request.get_json()
        email_id=data.get('email_id')
        full_name=data.get('full_name')
        current_email=Users.query.filter_by(email_id=email_id,full_name=full_name).first()
        if not current_email:
            return {"message":'Provided Email is Wrong'},404
        return {"message":'Provided email is correct','email_id':email_id,'hashpass':current_email.password},200
    
class NewPass(Resource):
    def put(self,email_id,hashpass):
        data=request.get_json()
        newpassword=data.get('newpassword')
        newhash=generate_password_hash(newpassword)
        current_email=Users.query.filter_by(email_id=email_id).first()
        if not current_email or current_email.password!=hashpass:
            return {"message":'Please visit this url after passing forget password details'},401
        current_email.password=newhash
        db.session.commit()
        return {'message':'Your Password has been successfully reseted'},201