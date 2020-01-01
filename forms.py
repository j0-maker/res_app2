from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField
from wtforms.fields.html5 import DateField, EmailField, TelField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Length, Email

#date = DateField('Date:', validators=[DateRange(date(2000,1,1), date(2012,4,20))])

class RegisterForm(FlaskForm):
    username = StringField("Username",
                        render_kw={"placeholder": "Username"},
                        validators=[InputRequired(),
                                    Length(min=5, max=20)])

    restaurant_address = StringField("Restaurant address", 
                        render_kw={"placeholder": "Address"},
                        validators=[InputRequired(),
                                    Length(min=5, max=200)])

    restaurant_name = StringField("Restaurant name",
                        render_kw={"placeholder": "Restaurant name"},
                        validators=[InputRequired(),
                                    Length(min = 1, max = 200)])
    
    owner_fname = StringField("First name",
                        render_kw={"placeholder": "First name"},
                        validators=[InputRequired(),
                                    Length(min=2, max=50)])

    owner_lname = StringField("Last name",
                        render_kw={"placeholder": "Last name"},
                        validators=[InputRequired(),
                                    Length(min=2, max=50)])

    website = StringField("Website address",
                        render_kw={"placeholder": "Website"},
                        validators=[InputRequired(),
                                    Length(min=2, max=100)])

    email = EmailField("Email",
                        render_kw={"placeholder": "Email address"},
                        validators=[InputRequired(),
                                    Length(min=2, max=100),
                                    Email()])

    telephone_number = TelField("Telephone number",
                        render_kw={"placeholder": "Telephone number"},
                        validators=[InputRequired(),
                                    Length(min=5, max=20)])

    country = SelectField("Country",
                        choices=[("IT", "Italy"), ("FR", "France"), ("ES", "Spain"), ("DE", "Germany"), ("UK", "United Kingdom"), ("EE", "Estonia"), ("BR", "Brasil")])
                                      
    pwd = PasswordField("Password",
                        render_kw={"placeholder": "Password"}, 
                        validators=[InputRequired(),
                                    Length(min=8, max=30),
                                    EqualTo("pwd_confirm", message="Password must match!")])

    pwd_confirm = PasswordField("Confirm password", 
                        render_kw={"placeholder": "Confirm password"},
                        validators=[InputRequired()])


class LoginForm(FlaskForm):

    username = StringField("Username",
                        render_kw={"placeholder": "Username"},
                        validators=[InputRequired(),
                                    Length(min=5, max=100)])

    pwd = PasswordField("Password",
                        render_kw={"placeholder": "Password"}, 
                        validators=[InputRequired(),
                                    Length(min=2, max=30)])