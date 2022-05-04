from flask import Flask, render_template, request
import requests
# from app.forms import LoginForm 
from app.forms import PokemonForm
from app import app
from wtforms.validators import InputRequired, ValidationError


@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')
    

# @app.route('/login', methods=['GET','POST'])
# def login():
#     form = LoginForm()
#     if request.method=='POST' and form.validate_on_submit():
#         email = form.email.data.lower()
#         password = form.password.data
#         if email in app.config.get('REGISTERED_USERS') and password == app.config.get('REGISTERED_USERS').get(email).get('password'):
#             #Login success!!!!!!!!
#             return f"Login Succes Welcome {app.config.get('REGISTERED_USERS').get(email).get('name')}"
#         error_string = "Incorrect Email/Password Combo"
#         return render_template("login.html.j2", error=error_string, form=form)

#     return render_template("login.html.j2", form=form)

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    form = PokemonForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        pokemon1= form.pokemon1.data.lower()
        pokemon1 = request.form.get('pokemon1')
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon1}/"          
        response = requests.get(url)
       
        if not response.ok:
            error_string = 'ERROR, Sorry, choose an existing pokemon.'
            return render_template('pokemon.html.j2', error=error_string, form=form)
    
        if not response.json():
            error_string = "We had an error loading your data most likely because Pokemon not in database."
            return render_template('pokemon.html.j2', error=error_string)

        data = response.json()

        data={
            'name':data['forms'][0]['name'],
            'ability': data['abilities'][0]['ability']['name'],
            'base_expereince':data['base_experience'],
            'sprites':data['sprites']['front_shiny'],
            'stats_attack': data['stats'][1]['base_stat'],
            'stats_hp': data['stats'][0]['base_stat'],
            'stats_defense': data['stats'][2]['base_stat']
        }
        
        return render_template('pokemon.html.j2', form=form, poke=data)
    return render_template('pokemon.html.j2', form=form)

@app.route('/pokemon_image', methods=['GET', 'POST'])
def pokemon_image():      
    pass
