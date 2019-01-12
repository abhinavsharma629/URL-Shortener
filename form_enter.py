from flask_wtf import FlaskForm
import validators
from flask import flash
from wtforms import StringField, PasswordField ,SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL

class UrlShorten(FlaskForm):
	url=StringField('URL',validators=[DataRequired(),URL()])
	submit=SubmitField('Shorten URL')
