from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo,ValidationError
from app.models import User



#form section
class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



class PokemonForm(FlaskForm):
    pokemon1 = StringField('Pokemon1', validators=[DataRequired()])
    submit = SubmitField('Submit')
    def validate_pokemon1(form,field):
        if len(field.data) > 15:
            raise ValidationError('Name must be less than 15 characters.')
        # elif field.data != DataRequired:
        #     return ("please enter a valid pokemon")
        # else:
        #     return("please enter a valid pokemon")

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()]) 
    password = StringField('Password', validators=[DataRequired()]) 
    confirm_password = StringField('Confirm Password', 
            validators=[DataRequired(), EqualTo('password', message='Password Must Match')])
    submit = SubmitField('Register')
    def validate_email(form, field):
        same_email_user = User.query.filter_by(email = field.data).first()
        if same_email_user:
            raise ValidationError('Email is Already in use')