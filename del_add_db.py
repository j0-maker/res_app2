from app import db, app
from models import *
import sys

def create(database):
    database.create_all()

def dropall(database):
    database.drop_all()

if sys.argv[1] == "c":
    create(db)
    time_array = ["19:00", "19:30", "20:00", "20:30","21:00", "21:30" ,"22:00" , "22:30", "23:00", "23:30"]
    for i in time_array:
        new_time = Time_range(t_time = i)
        db.session.add(new_time)
    db.session.commit()

elif sys.argv[1] == "d":
    dropall(db)

