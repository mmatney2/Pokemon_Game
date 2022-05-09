from flask import render_template, request, flash
import requests
from .forms import PokemonForm
from .import bp as main
from flask_login import login_required


@main.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')
    

@main.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokemonForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        pokemon1= form.pokemon1.data.lower()
        pokemon1 = request.form.get('pokemon1')
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon1}/"          
        response = requests.get(url)
       
        if not response.ok:
            error_string = 'ERROR, Sorry, choose an existing pokemon.'
            flash('Please enter an existing pokemon', 'danger')
            return render_template('pokemon.html.j2', error=error_string, form=form)
    
        if not response.json():
            error_string = "We had an error loading your data most likely because Pokemon not in database."
            
            return render_template('pokemon.html.j2', error=error_string, form=form)

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
        
        return render_template('pokemon.html.j2', poke=data, form=form)
    return render_template('pokemon.html.j2', form=form)