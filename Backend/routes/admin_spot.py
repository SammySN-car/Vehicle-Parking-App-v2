from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from Backend.utils.db import db
from Backend.utils.jwt_utils import admin_required
from Backend.models.database import ParkingLot,ParkingSpot,ReserveParkingSpot

class AdminSpot(Resource):
    @jwt_required()
    @admin_required
    def get(self,spot_id):
        spot=ParkingSpot.query.get(spot_id)
        if not spot:
            return {'message':'this spot does not exist'},404
        occupied=None
        if spot.status=='O':
            occupied=ReserveParkingSpot.query.filter_by(spot_id=spot_id).first()
            occupied={'spot_id':occupied.spot_id,'user_id':occupied.user_id,'vehicle_number':occupied.vehicle_number,'parking_timestamp':occupied.parking_timestamp,'parking_cost':occupied.parking_cost}
        spots={'id':spot.id,'status':spot.status,'lot_id':spot.lot_id}
        if occupied:
            spots['occupied']=occupied
        else:
            spots['occupied']=None
        return {'message':'here are the details','spots':spots},200
    
    @jwt_required()
    @admin_required
    def delete(self,spot_id):

        spot=ParkingSpot.query.get(spot_id)
        if not spot:
            return {'message':'this spot does not exist'},404
        if spot.status=='A':
            ParkingSpot.query.filter_by(id=spot_id).delete()
            db.session.commit()
            return {'message':'spot deleted successfully'},200
        else:
            return {'message':'spot is occupied'},409
        