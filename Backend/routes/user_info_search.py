from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity
from Backend.utils.db import db
from Backend.models.database import ReserveParkingSpot,ParkingLot,ParkingSpot
from Backend.utils.jwt_utils import user_required
from sqlalchemy import func,cast,String

class UserInfoSearch(Resource):
    @jwt_required()
    @user_required
    def get(self):
        user_id=get_jwt_identity()
        
        release=(db.session.query(ReserveParkingSpot.id,ParkingLot.prime_location_name,ReserveParkingSpot.vehicle_number,ReserveParkingSpot.leaving_timestamp).join(ParkingSpot,ParkingSpot.id==ReserveParkingSpot.spot_id).join(ParkingLot,ParkingLot.id==ParkingSpot.lot_id).filter(ReserveParkingSpot.user_id==user_id,ReserveParkingSpot.leaving_timestamp.isnot(None)).all())
        
        book=(db.session.query(ReserveParkingSpot.id,ParkingLot.prime_location_name,ReserveParkingSpot.vehicle_number).join(ParkingSpot,ParkingSpot.id==ReserveParkingSpot.spot_id).join(ParkingLot,ParkingLot.id==ParkingSpot.lot_id).filter(ReserveParkingSpot.user_id==user_id,ReserveParkingSpot.leaving_timestamp.is_(None)).all())
        released = [{'id':id,'prime_location_name':prime_location_name,'vehicle_number':vehicle_number,'leaving_timestamp':leaving_timestamp} for id,prime_location_name,vehicle_number,leaving_timestamp in release]
        booked = [{'id':id,'prime_location_name':prime_location_name,'vehicle_number':vehicle_number} for id,prime_location_name,vehicle_number in book]
        detail=(db.session.query(ParkingLot.id,ParkingLot.prime_location_name,ParkingLot.address,ParkingLot.price,ParkingLot.pincode,func.count(ParkingSpot.id).label('available')).join(ParkingSpot,ParkingSpot.lot_id==ParkingLot.id).filter(ParkingSpot.status=='A').group_by(ParkingLot.id).all())
        details=[{'id':id,'prime_location_name':prime_location_name,'available':available,'address':address,'price':price,'pincode':pincode} for id,prime_location_name,address,price,pincode,available in detail]
        return {'released':released,'booked':booked,'details':details},200
    
    @jwt_required()
    def post(self):
        data=request.get_json()
        search_term=data.get('search_term')
        if search_term:
            lotts=(db.session.query(ParkingLot.id,ParkingLot.prime_location_name,func.count().label('available')).join(ParkingSpot,ParkingLot.id==ParkingSpot.lot_id).filter((ParkingLot.prime_location_name.ilike(f"%{search_term}%"))|(func.cast(ParkingLot.pincode,String).ilike(f"%{search_term}%")),ParkingSpot.status=='A').group_by(ParkingLot.id,ParkingLot.prime_location_name).all())
            lots = [{'id':id,'prime_location_name':prime_location_name,'available':available} for id,prime_location_name,available in lotts]
            return {'lots':lots,'search_term':search_term},200
        else:
            return {'message':'wrong input'},400