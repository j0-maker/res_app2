#libraries-----------------------
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#initializing flask app--------------------------
app = Flask(__name__)
heroku = False

#load config file--------------------------------
if heroku == True:
    app.config.from_pyfile('config.py')
else:
    app.config.from_pyfile('config2.py')

#set db------------------------------------------
db = SQLAlchemy(app)

#import views(module)----------------------------
from views import *

if __name__ == "__main__":
    app.run()
