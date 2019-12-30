from wtforms import  Form, StringField, PasswordField, validators, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length
from flask_wtf import Form

class RegisterForm(Form):
    username = StringField("Username", [validators.Length(min=2, max=50)])

    restaurant_address = StringField("Restaurant address", 
                        validators=[InputRequired(),
                                    Length(min=5, max=200)])

    restaurant_name = StringField("Restaurant name",
                        validators=[InputRequired(),
                                    Length(min = 1, max = 200)])
    
    owner_name = StringField("Owner name",
                        validators=[InputRequired(),
                                    Length(min=2, max=50)])

    pwd = PasswordField("Password", 
                        validators=[InputRequired()])

    pwd_confirm = PasswordField("Confirm password", 
                        validators=[InputRequired(),
                                    EqualTo("pwd", message="Password must match!")])
