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
    
    owner_fname = StringField("Owner first name",
                        validators=[InputRequired(),
                                    Length(min=2, max=50)])

    owner_lname = StringField("Owner last name",
                              validators=[InputRequired(),
                                          Length(min=2, max=50)])

    website = StringField("Website adress",
                        validators=[InputRequired(),
                                    Length(min=2, max=100)])

    telephone_number = StringField("Telephone number",
                        validators=[InputRequired(),
                                    Length(min=5, max=20)])

    country = StringField("Telephone number",
                          validators=[InputRequired(),
                                      Length(min=5, max=20)])
                                      Password", 
                        validators=[InputRequired()])

    pwd_confirm = PasswordField("Confirm password", 
                        validators=[InputRequired(),
                                    EqualTo("pwd", message="Password must match!")])
