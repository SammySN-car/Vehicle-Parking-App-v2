from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from Backend.utils.db import db
from Backend.utils.jwt_utils import admin_required
from Backend.models.database import ParkingLot,ParkingSpot,Users


class AdminSearch(Resource):
    @jwt_required()
    @admin_required
    def post(self):
        data=request.get_json()
        search_by=data.get('search_by')
        search_term=data.get('search_term')

        if search_by=='user_id':
            try:
                user_id = int(search_term)
            except (ValueError, TypeError):
                return {'message': 'Invalid user ID'}, 400
            user=Users.query.get(user_id)
            if user:
                results=[{'id':user.id,'full_name':user.full_name,'email_id':user.email_id,'address':user.address,'pincode':user.pincode}]
                return {"message":'These are the details','results':results}, 200
            else:
                return {'message':'user not found'},404
        elif search_by=='prime_location_name':
            lots=ParkingLot.query.filter(ParkingLot.prime_location_name.ilike(f"%{search_term}%")).all()
            if lots:
                results=[]
                for lot in lots:
                    occupied=ParkingSpot.query.filter_by(lot_id=lot.id,status='O').count()
                    available=ParkingSpot.query.filter_by(lot_id=lot.id,status='A').count()
                    lott = {
                        'id': lot.id,
                        'prime_location_name': lot.prime_location_name,
                        'address': lot.address,
                        'pincode': lot.pincode,
                        'price': lot.price,
                        'occupied': occupied,
                        'available': available
                    }
                    results.append(lott)

                return {'message':"here are the details",'results':results,'search_by':search_by},200
            else:
                return {'message':'location not found'},404
        else:
            return {'message':'wrong input'},400
