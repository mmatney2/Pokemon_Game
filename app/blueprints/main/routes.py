from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokemonForm
from .import bp as main
from flask_login import login_required, current_user
from ...models import Pokeman, User, Pokemanuser


@main.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')
    
@main.route('/pokemon/<string:poke_name>')
@login_required
def catch_a_poke(poke_name):
    poke_to_catch = Pokeman.query.filter_by(poke_name=poke_name).first()
    current_user.collect_poke(poke_to_catch)
    flash("Congrats you caught a pokemon!", 'primary')
    return redirect(url_for('main.pokemon'))

@main.route('/show_users')
@login_required
def show_users():
    users=User.query.filter(User.id != current_user.id).all()
    return render_template('show_users.html.j2',  users=users, view_all=True)


@main.route('/poke_team')
@login_required
def poke_team():
    pokemans = Pokeman.query.filter_by().all()
    users=User.query.filter(User.id != current_user.id).all()

    return render_template('poke_team.html.j2', users=users, pokemans=pokemans,  view_all=True)

@main.route('/attack/<int:id>')
@login_required
def attack_player(id):  
    
    user_to_attack=User.query.get(id) 
    ps = user_to_attack.pokeman
    cs = current_user.pokeman
    p_total = 0
    c_total = 0
    for p in ps:
        p_total += p.stats_hp
    for c in cs:
        c_total += c.stats_hp
    if p_total < c_total:
        print("you win")
    if p_total > c_total:
        print("you lose")
    return redirect(url_for('main.poke_team'))

@main.route('/pokemon/<int:id>')
@login_required
def delete_poke(id):
    poke_to_remove = Pokeman.query.filter(id)
    current_user.remove_poke(poke_to_remove)
    flash("You removed a Pokemon!", 'warning')
    return redirect(url_for('main.poke_team'))

@main.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokemonForm()

    if request.method == 'POST' and form.validate_on_submit():
        print("Checkpoint 1")
        #post the text in the form and display the data
        poke_name= form.poke_name.data.lower()
        
        poke_searched = Pokeman.query.filter_by(poke_name=poke_name).first()
        if not poke_searched:
            print("checkpoint 2")
            url = f"https://pokeapi.co/api/v2/pokemon/{poke_name}/"          
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
                'poke_name':data['forms'][0]['name'],
                'ability': data['abilities'][0]['ability']['name'],
                'base_experience':data['base_experience'],
                'sprites':data['sprites']['front_shiny'],
                'stats_attack': data['stats'][1]['base_stat'],
                'stats_hp': data['stats'][0]['base_stat'],
                'stats_defense': data['stats'][2]['base_stat']
            }
            
            poke_searched=Pokeman()
            poke_searched.from_dict(data) 
            poke_searched.save()
        # print(poke_searched)
        return render_template('pokemon.html.j2', poke_name=poke_searched, pokeman=poke_searched,  form=form)
    return render_template('pokemon.html.j2',  form=form )
    

