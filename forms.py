from wtforms import  Form, TextField, PasswordField, validators, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired

class BookForm(Form):
    name = IntegerField("Name", validators=[DataRequired()])
    res_date = DateField("Date", validators=[DataRequired()])
