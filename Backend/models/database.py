from Backend.utils.db import db

class Users(db.Model):
    __tablename__='USERS'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    full_name=db.Column(db.String,unique=True,nullable=False)
    email_id=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    address=db.Column(db.String,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    role=db.Column(db.String,db.CheckConstraint("role in ('admin','user')"),nullable=False,default='user')

    reservations=db.relationship('ReserveParkingSpot',backref='user',cascade='all,delete')

class ParkingLot(db.Model):
    __tablename__='Parking_lot'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    prime_location_name=db.Column(db.String,nullable=False)
    price=db.Column(db.Integer,nullable=False)
    address=db.Column(db.String,nullable=False)
    pincode=db.Column(db.Integer,nullable=False)
    maximum_number_of_spots=db.Column(db.Integer,nullable=False)

    spots=db.relationship('ParkingSpot',backref='lot',cascade='all,delete')
    reservations=db.relationship('ReserveParkingSpot',backref='lot',cascade='all,delete')

class ParkingSpot(db.Model):
    __tablename__='Parking_spot'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    lot_id=db.Column(db.Integer,db.ForeignKey('Parking_lot.id',ondelete='CASCADE'),nullable=False)
    status=db.Column(db.String,db.CheckConstraint("status in ('A','O')"),nullable=False,default='A')
    
    reservations=db.relationship('ReserveParkingSpot',backref='spot',cascade='all,delete')

class ReserveParkingSpot(db.Model):
    __tablename__='Reserve_parking_spot'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('USERS.id',ondelete='CASCADE'),nullable=False)
    spot_id=db.Column(db.Integer,db.ForeignKey('Parking_spot.id',ondelete='CASCADE'),nullable=False)
    lot_id=db.Column(db.Integer,db.ForeignKey('Parking_lot.id',ondelete='CASCADE'),nullable=False)
    parking_timestamp=db.Column(db.String,nullable=False)
    leaving_timestamp=db.Column(db.String)
    parking_cost=db.Column(db.Integer)
    vehicle_number=db.Column(db.String)
