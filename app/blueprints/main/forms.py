from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import User

# from .forms import PokemonForm

class PokemonForm(FlaskForm):
    poke_name = StringField('Pokemon1', validators=[DataRequired()])
    submit = SubmitField('Submit')
    def validate_pokemon1(form,field):
        if len(field.data) > 30:
            raise ValidationError('Name must be less than 30 characters.')

    
    ## MUST BE LIKE THIS!!  VALIDATE_FIELDNAME
    def validate_email(form, field):
        same_email_user = User.query.filter_by(email = field.data).first()
                        # SELECT * FROM user WHERE email = ???
        if same_email_user:
            raise ValidationError('Email is Already in Use')

        ## MUST BE LIKE THIS!!  VALIDATE_FIELDNAME
   