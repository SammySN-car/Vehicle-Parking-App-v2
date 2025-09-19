from flask_restful import Resource
from flask import request
from sqlalchemy import func
from flask_jwt_extended import jwt_required,get_jwt_identity
from Backend.utils.db import db
from Backend.utils.jwt_utils import user_required
from Backend.utils.redis_client import cache
from Backend.models.database import ParkingLot, ParkingSpot, ReserveParkingSpot
import json

class UserSummary(Resource):
    @jwt_required()
    @user_required
    def get(self):
        cache_k='user_summary'
        cached_d=cache.get(cache_k)
        if cached_d:
            return {'message':'from cache','summary':json.loads(cached_d)}
        user_id=get_jwt_identity()
        details=(db.session.query(ParkingLot.id,func.count().label('used')).join(ParkingSpot,ParkingSpot.lot_id==ParkingLot.id).join(ReserveParkingSpot,ReserveParkingSpot.spot_id==ParkingSpot.id).filter(ReserveParkingSpot.user_id==user_id,ReserveParkingSpot.leaving_timestamp.isnot(None)).group_by(ParkingLot.id).all())
        summary=[{'lot_id':lot_id,'used':used} for lot_id,used in details]
        if not summary:
            return {'message':'no data to use','summary':[]},200
        cache.setex(cache_k,300,json.dumps(summary))
        return {'message': 'Success', 'summary': summary}, 200