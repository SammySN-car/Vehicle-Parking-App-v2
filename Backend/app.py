from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from Backend.utils.db import db
import os
from werkzeug.security import generate_password_hash


app=Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='[Your Email_id]'
app.config['MAIL_PASSWORD']='[Your Password]'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

mail=Mail(app)

app.config['JWT_SECRET_KEY']='this-is-my-secret-key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
jwt=JWTManager(app)

db_path = os.path.join(os.path.dirname(__file__), 'data', 'parking.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)  # ensure the folder exists

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Backend/data/parking.db'
db.init_app(app)

from Backend.models.database import Users,ParkingLot,ParkingSpot,ReserveParkingSpot

with app.app_context():
    db.create_all()
    print("✅ DB created")
    if not Users.query.filter_by(role='admin').first():
        passwor='admin'
        adm=Users(
            full_name='ADMIN',
            email_id="ADMIN@gmail.com",
            password=generate_password_hash(passwor),
            address="ADMINS HOME",
            pincode='000000',
            role='admin'
        )
        db.session.add(adm)
        db.session.commit()
        print("✅ Admin user created")
from Backend.routes.auth import Register,Login
from Backend.routes.admin_lot import AddLot,EditLot,DeleteLot,ViewLots
from Backend.routes.admin_search import AdminSearch
from Backend.routes.admin_user import AdminUser
from Backend.routes.edit_profile import EditProfile
from Backend.routes.admin_spot import AdminSpot
from Backend.routes.admin_summary import AdminSummary
from Backend.routes.user_info_search import UserInfoSearch
from Backend.routes.user_lot import UserLotBook,UserReleaseBook
from Backend.routes.user_summary import UserSummary
from Backend.routes.csv_export import CSVExport,CSVDownload

api=Api(app)

api.add_resource(Register,'/register')
api.add_resource(Login,'/')
api.add_resource(AddLot,'/admin/add_lot')
api.add_resource(EditLot,'/admin/edit_lot/<int:lot_id>')
api.add_resource(DeleteLot,'/admin/delete_lot/<int:lot_id>')
api.add_resource(ViewLots,'/admin/home')
api.add_resource(AdminSearch,'/admin/search')
api.add_resource(AdminUser,'/admin/users')
api.add_resource(EditProfile,'/<string:role>/edit_profile')
api.add_resource(AdminSpot,'/admin/spot/<int:spot_id>')
api.add_resource(AdminSummary,'/admin/summary')
api.add_resource(UserInfoSearch,'/user/home')
api.add_resource(UserSummary,'/user/summary')
api.add_resource(UserLotBook,'/user/book/<int:lot_id>')
api.add_resource(UserReleaseBook,'/user/release/<int:reservation_id>')
api.add_resource(CSVExport,'/user/export_csv')
api.add_resource(CSVDownload,'/user/export_csv/<string:file_name>')

if __name__=='__main__':
    app.run(debug=True,port=5000)

