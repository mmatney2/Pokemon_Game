from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokemonForm
from .import bp as main
from flask_login import login_required, current_user
from ...models import Pokeman, User


@main.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')
    
@main.route('/pokemon/<string:poke_name>')
@login_required
def catch_a_poke(poke_name):
    poke_to_catch = Pokeman.query.filter_by(poke_name=poke_name).first()
    current_user.collect_poke(poke_to_catch)
    print(poke_to_catch)
    flash("Congrats you caught a pokemon!", 'primary')
    return redirect(url_for('main.pokemon'))

@main.route('/show_users')
def show_users():
    poke1 = Pokeman.query.filter().all()
    users=User.query.filter(User.id != current_user.id).all()
    
    return render_template('show_users.html.j2',  users=users,  poke1=poke1, view_all=True)

#attack
@main.route('/attack/<int:id>')
def attack_player(id):
    # print(id)
    attack_poke = User.query.filter(pokemen==id).all()
    # print(attack_poke)
    for poke in attack_poke:
        print(poke)

        return render_template('results.html.j2', attack_poke=attack_poke, view_all=True)


    # current_user.attack_a_poke(attack_poke)

    # count_wins=User.query.filter_by(wins=wins)
    # current_user.wins(count_wins)


# #put att func here/calc who wins and update database who won, update win count
#     if current_user.stats_hp < User.stats_hp:
#         current_user.save()
#         flash(f"You lost against {user.first_name} {user.last_name} ", "danger")
#         return render_template('results.html.j2', user=user)
#     flash(f"YOU WON against {user.first_name} {user.last_name} ", "success")
#     return render_template('results.html.j2', user=user)
    
@main.route('/delete_poke/<int:id>')
def delete_poke(id):
    pokemans = Pokeman.query.filter.get(id)
    current_user.delete(pokemans)




#results of battle/winner/loser/displyed on results page
@main.route('/results')
@login_required
def results(id):
    user = Pokeman.query.get(id)
    if current_user['stats_hp'] <= user['stats_hp']:
        data=Pokeman()
        print(data)
        data.save
        return render_template('show_users.html.j2', user=user, view_all=True)    

    
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
    

