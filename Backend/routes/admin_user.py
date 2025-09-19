from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from Backend.utils.db import db
from Backend.utils.jwt_utils import admin_required
from Backend.models.database import Users

class AdminUser(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        us=(db.session.query(Users.id,Users.email_id,Users.full_name,Users.address,Users.pincode).filter(Users.role!='admin').all())
        users = [{'id':user.id,'email_id':user.email_id,'full_name':user.full_name,'address':user.address,'pincode':user.pincode} for user in us]
        print(us,users)
        return {"message":"Here are the details","users":users},200