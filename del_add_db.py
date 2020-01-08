from app import db, app
from models import *
import sys

def create(database):
    database.create_all()

def dropall(database):
    database.drop_all()

if sys.argv[1] == "c":
    create(db)
    #("16:00 e 23:59 usati solamente per tenere l'ultima fascia oraria - non selezionabili come orari apertura/chiusura")
    #indici utili: 0-11:00 1 2-12:00 3 4 5-13:30 6 7 8 9-15:30     sera 11-19:00 14-20:30 18:22:30   max 21 min 0
    time_array = ["11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "19:00", "19:30", "20:00", "20:30","21:00", "21:30" ,"22:00" , "22:30", "23:00", "23:30", "23:59"]
    for i in time_array:
        new_time = Time_range(t_time = i)
        db.session.add(new_time)
    db.session.commit()

elif sys.argv[1] == "d":
    dropall(db)

