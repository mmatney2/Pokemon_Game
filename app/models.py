from app import db, login
from flask_login import UserMixin # IS ONLY FOR THE USER MODEL!!!!
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash




class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name =  db.Column(db.String)
    email =  db.Column(db.String, unique=True, index=True)
    password =  db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.Integer)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    pokeman = db.relationship('Pokeman', 
                    secondary = 'pokemanuser', #or pokemen
                    backref = 'users',
                    lazy='dynamic')
    
    # def collect_poke(self, poke):
    #     self.pokemen.append(poke)
    #     db.session.commit()

    
    # should return a unique identifing string
    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'

    # Human readbale ver of rpr
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    #salts and hashes our password to make it hard to steal
    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    # compares the user password to the password provided in the login form
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email=data['email']
        self.password = self.hash_password(data['password'])
        self.icon = data['icon']

    # save the user to the database
    def save(self):
        db.session.add(self) #adds the user to the db session
        db.session.commit() #save everythig in the session to the db

    def edit(self, new_pokeman):
        self.poke_name = new_pokeman

    
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def collect_poke(self, pok):
        self.pokeman.append(pok)
        db.session.commit()

    def remove_poke(self, pok):
        self.pokeman.remove(pok)
        db.session.commit()
    


    def get_icon_url(self):
        return f'https://avatars.dicebear.com/api/adventurer/{self.icon}.svg'
    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    # SELECT * FROM user WHERE id = ???

class Pokemanuser(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    poke_id = db.Column(db.Integer, db.ForeignKey('pokeman.poke_id'))
    id= db.Column(db.Integer, db.ForeignKey('user.id'))

class Pokeman(db.Model):
    poke_id = db.Column(db.Integer, primary_key=True)
    poke_name = db.Column(db.String)
    stats_hp = db.Column(db.Integer)
    ability = db.Column(db.String)
    base_experience = db.Column(db.Integer)
    sprites = db.Column(db.String)
    stats_attack=  db.Column(db.Integer)
    stats_defense = db.Column(db.Integer)    

    
    

    def __repr__(self):
        return f'<Pokeman: {self.poke_name} | {self.poke_id} | {self.stats_hp} | {self.ability} | {self.sprites} | {self.stats_attack} | {self.stats_defense}>'

    def edit(self, new_pokeman):
        self.poke_name = new_pokeman

    def save(self):
        db.session.add(self) #adds the post to the db session
        db.session.commit() #save everything in the session to the db
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def collect_poke(self, pok):
        self.pokeman.append(pok)
        db.session.commit()

    def remove_poke(self, pok):
        self.pokeman.remove(pok)
        db.session.commit()
        
    
   
        

    
    def from_dict(self, data):
        self.poke_name=data['poke_name']
        self.ability = data['ability']
        self.base_experience=data['base_experience']
        self.sprites=data['sprites']
        self.stats_attack=data['stats_attack']
        self.stats_hp=data['stats_hp']
        self.stats_defense=data['stats_defense']

    