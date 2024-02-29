from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Email

#This is the name that will bbe displayed above your input fields

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    subject = StringField('Subject ', validators=[InputRequired()])
    message = TextAreaField('Message', validators=[InputRequired()])