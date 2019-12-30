from app import db, app
import models
import sys

def create(database):
    database.create_all()

def dropall(database):
    database.drop_all()

if sys.argv[1] == "c":
    create(db)
elif sys.argv[1] == "d":
    dropall(db)

