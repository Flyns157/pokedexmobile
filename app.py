from random import random
import requests as requests
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField
from flask import Flask, redirect, url_for, render_template

# Init
try:
    DEFAULT_KEY_SIZE = 30
    DEFAULT_PAGE = 0
    DEFAULT_PAGE_SIZE = 1

    app = Flask(__name__)
    app.secret_key = "POKEDEX.mobile"
except (RuntimeError, TypeError, NameError):
    raise Exception(f'''/!\ Can't init the website ...\nRuntimeError : {RuntimeError}\nTypeError : {TypeError}\nNameError : {NameError})''')

class PageForm(FlaskForm):
    numero = StringField('numero', validators=[DataRequired()])
    size = IntegerField('size', validators=[DataRequired()])

@app.route("/catalogue", methods=['GET', 'POST'])
def index():
    page_form = PageForm()
    if page_form.validate_on_submit():
        location = int(page_form.numero.data)
        nb_pokemon_by_page = int(page_form.size.data)
    else :
        location = DEFAULT_PAGE
        nb_pokemon_by_page = DEFAULT_PAGE_SIZE
    pokemons = requests.get(f'https://pokeapi.co/api/v2/pokemon/?limit={nb_pokemon_by_page}&offset={location}')
    return render_template('cataloge.html', pekemons = pokemons.json())
