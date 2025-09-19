from Backend.celery_work import celery
from Backend.utils.db import db
from Backend.models.database import ParkingLot,ParkingSpot,ReserveParkingSpot,Users
import csv,os
from datetime import datetime,date,timedelta
from flask_mail import Message
from sqlalchemy import func,not_,distinct

@celery.task(name="tasks.user_task.daily_reminders")
def daily_reminders():
    from Backend.app import app, mail
    with app.app_context():
        
        if ParkingLot.query.count()==0:
            return "First add a parking lot to start reminders"
        today=date.today().isoformat()
        use = db.session.query(Users.id, Users.email_id, Users.full_name).filter(not_(Users.id.in_(db.session.query(distinct(ReserveParkingSpot.user_id)).filter(func.date(ReserveParkingSpot.parking_timestamp) == today)))).all()

        users=[{'id':id,'email_id':email_id,'full_name':full_name} for id,email_id,full_name in use]


        for user in users:
            email=user['email_id']
            name=user['full_name']
            msg=Message(
                subject="Daily Parking Reminder",
                sender=app.config['MAIL_USERNAME'],
                recipients=[email],
                body=f"Hi {name},\n\nYou haven't booked a parking slot today.Please book if needed.\n\nParking app team"
            )
            try:
                mail.send(msg)
                print(f'mail sent to {email}')
            except Exception as e:
                print(f'Failed to send email to {email} : {e}')
        return {'status':"Daily reminders sent","count":len(users)}

@celery.task(name="tasks.user_task.monthly_reminders")
def monthly_reminders():
    from Backend.app import app, mail
    with app.app_context():
        first_day=datetime.today().replace(day=1)
        last_day=first_day-timedelta(days=1)
        previous_month=last_day.strftime('%Y-%m')
        use=(db.session.query(ReserveParkingSpot.user_id,Users.email_id,Users.full_name).join(Users,ReserveParkingSpot.user_id==Users.id).filter(func.strftime('%Y-%m', ReserveParkingSpot.parking_timestamp) == previous_month).distinct(ReserveParkingSpot.user_id).all())
        user_list=[{'user_id':user_id,'email_id':email_id,'full_name':full_name} for user_id,email_id,full_name in use]
        if not user_list:
            return 'no reservation last month'
        for user in user_list:
            lott=(db.session.query(ReserveParkingSpot.lot_id,ParkingLot.prime_location_name,ParkingLot.address,func.count().label('total')).join(ParkingLot,ReserveParkingSpot.lot_id==ParkingLot.id).filter(func.strftime('%Y-%m', ReserveParkingSpot.parking_timestamp) == previous_month,ReserveParkingSpot.user_id==user['user_id']).group_by(ReserveParkingSpot.lot_id).first())
            lot={'lot_id':lott[0],'prime_location_name':lott[1],'address':lott[2],'total':lott[3]}
            count=ReserveParkingSpot.query.filter(ReserveParkingSpot.user_id==user['user_id'],func.strftime('%Y-%m', ReserveParkingSpot.parking_timestamp) == previous_month).count()
            cost=db.session.query(func.coalesce(func.sum(ReserveParkingSpot.parking_cost),0)).filter(ReserveParkingSpot.user_id==user['user_id'],func.strftime('%Y-%m', ReserveParkingSpot.parking_timestamp) == previous_month).scalar()
            msg=Message(
                    subject="Monthly Parking Report",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[user['email_id']],
                    html=f"""
                    <html>
                        <body>
                            <h2 style="color:#2c3e50;">Monthly Parking Report - {previous_month}</h2>
                            <p>Hi <strong>{user['full_name']}</strong>,</p>
                            <p>Here is a summary of your parking activity last month:</p>
                            <ul>
                                <li><strong>Total Reservations:</strong> {count}</li>
                                <li><strong>Total Cost:</strong> ₹{cost}</li>
                                <li><strong>Most Visited Lot:</strong> {lot['prime_location_name']} {lot['address']}</li>
                                <li><strong>Times Visited:</strong> {lot['total']}</li>
                            </ul>
                            <p style="margin-top:20px;">Thank you for using the Parking App.</p>
                            <p style="color:gray;">- Parking App Team</p>
                        </body>
                    </html>
                """
                )
            try:
                mail.send(msg)
                print(f"monthly report mail sent to {user['email_id']}")
            except Exception as e:
                print(f"Failed to send monthly report email to {user['email_id']}")
        return {'status': "Monthly reports sent", "count": len(user_list)}
    
@celery.task
def export_csv(user_id):
    from ..app import app
    with app.app_context():
        reserve=(db.session.query(ReserveParkingSpot.id,ReserveParkingSpot.spot_id,ReserveParkingSpot.lot_id,ReserveParkingSpot.parking_timestamp,ReserveParkingSpot.leaving_timestamp,ReserveParkingSpot.parking_cost,ReserveParkingSpot.vehicle_number).filter(ReserveParkingSpot.user_id==user_id).all())
        reservations=[{'id':id,'spot_id':spot_id,'lot_id':lot_id,'parking_timestamp':parking_timestamp,'leaving_timestamp':leaving_timestamp,'parking_cost':parking_cost,'vehicle_number':vehicle_number} for id,spot_id,lot_id,parking_timestamp,leaving_timestamp,parking_cost,vehicle_number in reserve]
        export_csv_id = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../exports'))
        os.makedirs(export_csv_id,exist_ok=True)

        file_name=f"user_{user_id}_export.csv"
        csv_file=os.path.join(export_csv_id,file_name)

        with open(csv_file,"w",newline='') as files:
            wri=csv.writer(files)
            wri.writerow(['Reservation ID','Spot ID','Lot ID','Parking Timestamp','Leaving Timestamp','Cost','Vehicle Number'])
            for row in reservations:
                wri.writerow([row['id'],row['spot_id'],row['lot_id'],row['parking_timestamp'],row['leaving_timestamp'],row['parking_cost'],row['vehicle_number']])
        print(f'CSV written in {csv_file}')
        return {'status':'completed','file_name':file_name}
