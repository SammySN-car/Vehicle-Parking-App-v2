from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from Backend.utils.db import db
from Backend.utils.jwt_utils import admin_required
from sqlalchemy import func
from Backend.models.database import ParkingLot,ParkingSpot,ReserveParkingSpot
from Backend.utils.redis_client import cache
import json

class AdminSummary(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        cache_k='admin_summary'
        cached_d=cache.get(cache_k)
        if cached_d:
            return {'message':'from cache','summary':json.loads(cached_d)}
        parking_lots=ParkingLot.query.all()
        summary_data=[]
        total_occupied=0
        total_available=0
        total_revenue=0
        for lot in parking_lots:
            lot_id=lot.id
            occupied=ParkingSpot.query.filter_by(lot_id=lot_id,status='O').count()
            available=ParkingSpot.query.filter_by(lot_id=lot_id,status='A').count()
            result = (db.session.query(func.sum(ReserveParkingSpot.parking_cost).label('price')).join(ParkingSpot,ParkingSpot.id==ReserveParkingSpot.spot_id).filter(ParkingSpot.lot_id==lot_id,ReserveParkingSpot.leaving_timestamp.isnot(None)).scalar())
            revenue = result or 0

            total_available+=available
            total_occupied+=occupied
            total_revenue+=revenue
            summary_data.append({
                'lot_id':lot.id,
                'available':available,
                'occupied':occupied,
                'revenue':revenue
            })
        if summary_data:
            loty=[]
            revenuety=[]
            occupiedty=[]
            availablety=[]
            for data in summary_data:
                loty.append(data['lot_id'])
                revenuety.append(data['revenue'])
                occupiedty.append(data['occupied'])
                availablety.append(data['available'])
        summary={'loty':loty,'revenuety':revenuety,'occupiedity':occupiedty,'availablety':availablety}
        cache.setex(cache_k,300,json.dumps(summary))
        return {'message':'here are the details','summary':summary},200