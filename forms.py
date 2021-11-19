from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField
from wtforms.validators import DataRequired, NumberRange


class SearchForm(FlaskForm):
    ig_username =StringField('ig_username',validators=[DataRequired()])
    submit = SubmitField("Go")