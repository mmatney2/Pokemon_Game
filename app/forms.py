from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


#form section
# class LoginForm(FlaskForm):
#     email = StringField('Email Address', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired(), Email()])
#     submit = SubmitField('Login')



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
        