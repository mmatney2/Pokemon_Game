import os

class Config():
    SECRET_KEY = os.environ.get("SECRET_KEY")
    # REGISTERED_USERS = {
    #     'gilmore@happymadison.com: {"name" : "Happy", "password":"12345678"}',
    #     'coffee@lovescoffee.com:{"name": "coffee", "password":"love123"}',
    #     'carebear@carebearcousin.com:{"name": "Joel", "password": "darkheart"}'

    # }