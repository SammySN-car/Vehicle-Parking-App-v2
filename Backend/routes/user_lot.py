from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity
from Backend.utils.db import db
from Backend.utils.jwt_utils import user_required
from Backend.models.database import ParkingLot,ParkingSpot,ReserveParkingSpot
from datetime import datetime

class UserLotBook(Resource):
    @jwt_required()
    @user_required
    def post(self,lot_id):
        user_id=get_jwt_identity()
        data=request.get_json()
        spot_id=data.get('id')
        vehicle_number=data.get('vehicle_number')
        if not all([vehicle_number,spot_id]):
            return {"message": "details required"}, 400
        parking_timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reserve=ReserveParkingSpot(
            lot_id=lot_id,
            spot_id=spot_id,
            user_id=user_id,
            vehicle_number=vehicle_number,
            parking_timestamp=parking_timestamp
        )
        db.session.add(reserve)
        spot=ParkingSpot.query.get(spot_id)
        spot.status='O'
        db.session.commit()
        return {'message':'Slot has been booked'},201
    
    @jwt_required()
    @user_required
    def get(self,lot_id):
        spots=ParkingSpot.query.filter_by(lot_id=lot_id,status='A').first()
        if spots:
            spot = {
                'id': spots.id,
                'lot_id': spots.lot_id,
                'status': spots.status
            }
            return {'message':"spot can be booked now",'spot':spot},200
        else:
            return {'message':'no free spot available'},409

class UserReleaseBook(Resource):
    @jwt_required()
    @user_required
    def post(self,reservation_id):
        data=request.get_json()
        now = datetime.now()
        leaving_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        #leaving_timestamp=data.get('leaving_timestamp')
        reserve=ReserveParkingSpot.query.get(reservation_id)
        hours = max(1, int((now - datetime.strptime(reserve.parking_timestamp, "%Y-%m-%d %H:%M:%S")).total_seconds() // 3600))
        lott=ParkingLot.query.get(reserve.lot_id)
        lot=lott.price
        parking_cost=hours*lot
        #parking_cost=data.get('parking_cost')
        #reserve=ReserveParkingSpot.query.get(reservation_id)
        reserve.parking_cost=parking_cost
        reserve.leaving_timestamp=leaving_timestamp
        spot=ParkingSpot.query.get(reserve.spot_id)
        spot.status='A'
        db.session.commit()
        return {"message": "Spot released successfully"}, 200

    @jwt_required() 
    @user_required
    def get(self,reservation_id):

        reservation=ReserveParkingSpot.query.get(reservation_id)
        if not reservation:
            return {'message': 'Reservation not found'}, 404

        now = datetime.now()
        leaving_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        start_time = datetime.strptime(reservation.parking_timestamp, "%Y-%m-%d %H:%M:%S")
        hours = max(1, int((now - start_time).total_seconds() // 3600))
        lott=ParkingLot.query.get(reservation.lot_id)
        lot=lott.price
        parking_cost=hours*lot
        return {'message':'reservation details','reservation': {
            'id': reservation.id,
            'user_id': reservation.user_id,
            'spot_id': reservation.spot_id,
            'lot_id': reservation.lot_id,
            'parking_timestamp': reservation.parking_timestamp,
            'vehicle_number': reservation.vehicle_number,
            'leaving_timestamp':reservation.leaving_timestamp,
            'parking_cost':reservation.parking_cost
        },'leaving_timestamp':leaving_timestamp,'parking_cost':parking_cost},200