from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,BooleanField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo


class SearchForm(FlaskForm):
    ig_username =StringField('ig_username',validators=[DataRequired()])
    submit = SubmitField("Go")



