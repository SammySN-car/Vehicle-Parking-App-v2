from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from Backend.utils.db import db
from Backend.models.database import ParkingLot,ParkingSpot
from Backend.utils.jwt_utils import admin_required
from sqlalchemy import text

class AddLot(Resource):
    @jwt_required()
    @admin_required 
    def post(self):
        data=request.get_json()
        prime_location_name=data.get('prime_location_name')
        price=data.get('price')
        address=data.get('address')
        pincode=data.get('pincode')
        maximum_number_of_spots=data.get('maximum_number_of_spots')

        if not all([prime_location_name,price,address,pincode,maximum_number_of_spots]):
            return {'message':'require all details'},400
        
        lot=ParkingLot(
            prime_location_name=prime_location_name,
            price=price,
            address=address,
            pincode=pincode,
            maximum_number_of_spots=maximum_number_of_spots
        )
        db.session.add(lot)
        db.session.flush()

        for _ in range(maximum_number_of_spots):
            spot=ParkingSpot(
                lot_id=lot.id
            )
            db.session.add(spot)
        
        db.session.commit()

        return {'message':'lot added successfully'},201
    
class EditLot(Resource):
    @jwt_required()
    @admin_required
    def put(self,lot_id):
        data=request.get_json()
        prime_location_name=data.get('prime_location_name')
        price=data.get('price')
        address=data.get('address')
        pincode=data.get('pincode')
        maximum_number_of_spots=data.get('maximum_number_of_spots')

        if not all([prime_location_name,price,address,pincode,maximum_number_of_spots]):
            return {'message':'require all details'},400
        

        lot=ParkingLot.query.get(lot_id)
        lots=lot.maximum_number_of_spots
        lot.prime_location_name=prime_location_name
        lot.price=price
        lot.address=address
        lot.pincode=pincode
        lot.maximum_number_of_spots=maximum_number_of_spots

        if maximum_number_of_spots > lots:
            for _ in range(maximum_number_of_spots - lots):
                spot=ParkingSpot(lot_id=lot.id)
                db.session.add(spot)
        elif maximum_number_of_spots<lots:
            fot=ParkingSpot.query.filter_by(lot_id=lot_id,status='A').count()
            star=lots-maximum_number_of_spots
            if star<=fot:
                spoto=ParkingSpot.query.filter_by(lot_id=lot_id,status='A').limit(star).all()
                for spo in spoto:
                    db.session.delete(spo)
            else:
                return {'message':'Free up spot first to delete'},409
        db.session.commit()
        return {'message':'changes have been made successfully'},200
    
    @jwt_required()
    @admin_required
    def get(self,lot_id):
        lot=ParkingLot.query.get(lot_id)
        lot_details={'prime_location_name':lot.prime_location_name,'price':lot.price,'address':lot.address,'pincode':lot.pincode,'maximum_number_of_spots':lot.maximum_number_of_spots}
        return {'message':"here are the details",'lot_details':lot_details},200
    
class DeleteLot(Resource):
    @jwt_required()
    @admin_required
    def delete(self,lot_id):
        
        count=ParkingSpot.query.filter_by(lot_id=lot_id,status='O').count()
        if count>0:
            return {'message':'Cannot delete because all spots are not available'},409
        obj=ParkingLot.query.filter_by(id=lot_id).first()
        db.session.delete(obj)
        db.session.commit()
        return {'message':'lot deleted successfully'},200

class ViewLots(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        sql = text("""
                    SELECT pl.*,
                        (SELECT COUNT(*) FROM Parking_spot ps WHERE ps.lot_id = pl.id AND ps.status = 'A') AS Available,
                        (SELECT COUNT(*) FROM Parking_spot ps WHERE ps.lot_id = pl.id AND ps.status = 'O') AS Occupied
                    FROM Parking_lot pl
                """)
        result = db.session.execute(sql)
        lots = [dict(row._mapping) for row in result]
        full_lots=[]
        for lot in lots:
            spo=ParkingSpot.query.filter_by(lot_id=lot['id']).all()
            spots=[{'id':l.id,'lot_id':l.lot_id,'status':l.status} for l in spo]
            lott=dict(lot)
            lott['spots'] = [dict(spot) for spot in spots]
            full_lots.append(lott)
        return {'message':"Here are the details",'all_lot':full_lots},200
        