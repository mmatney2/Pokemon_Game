from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')
    
@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    if request.method == 'POST':
        pokemon1 = request.form.get('pokemon1')
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon1}/"          
        response = requests.get(url)
        if not response.ok:
            error_string = 'ERROR, Sorry, choose an existing pokemon.'
            return render_template('pokemon.html.j2', error=error_string)
    
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
        
        return render_template('pokemon.html.j2', poke=data)
    return render_template('pokemon.html.j2')

# @app.route('/pokemon_image', methods=['GET', 'POST'])
# def pokemon_image():      
        

        

 