from celery import Celery
from celery.schedules import crontab
def make_celery():
    return Celery('parking_app',broker="redis://localhost:6379/0",backend='redis://localhost:6379/1',include=['Backend.tasks.user_task'])

celery=make_celery()
celery.conf.timezone='Asia/Kolkata'
celery.conf.beat_schedule={
    'daily-reminders-task':{
        'task':'tasks.user_task.daily_reminders',
        'schedule': crontab(hour=19,minute=5)
    },'monthly-summary-task':{
        'task':'tasks.user_task.monthly_reminders',
        'schedule': crontab(minute=0,hour=9,day_of_month=1)
    }       
}


