from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,BooleanField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo


class SearchForm(FlaskForm):
    ig_username =StringField('ig_username',validators=[DataRequired()])
    submit = SubmitField("Go")

class RegistrationForm(FlaskForm):
    # add email field here:
    email = StringField("Email", validators=[DataRequired(), Email()])
    # add password fields here:
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

