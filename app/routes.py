from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import LoginForm, RegisterForm
from app import app
from .models import User
from flask_login import current_user, logout_user, login_user, login_required
from app.forms import LoginForm, PokemonForm

@app.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')
    

@app.route('/pokemon', methods=['GET', 'POST'])
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


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        u=User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash('Welcome to Pokemon Showdown!', 'success')
            return redirect(url_for("index"))
        flash('Incorrect Email Password Combo', 'danger')
        return render_template('login.html.j2', form=form)
    return render_template("login.html.j2", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name": form.first_name.data.title(), 
                "last_name": form.last_name.data.title(), 
                "email": form.email.data.lower(), 
                "password": form.password.data
                }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
            new_user_object.save()
        except:
            flash("There was an unexpected error creating your account. Please try again later", 'danger')
            return render_template('register.html.j2', form=form)
        flash('You have successfully registered', 'success')
        return redirect(url_for('login'))
    return render_template('register.html.j2', form=form)

@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash("you have logged out", 'warning')
        return redirect(url_for('login'))