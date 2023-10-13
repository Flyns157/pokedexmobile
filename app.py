import sqlite3
from random import random
import requests as requests
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField
from flask import Flask, request, redirect, url_for, render_template

# Init
try:
    DEFAULT_KEY_SIZE = 30
    DEFAULT_PAGE = 0
    DEFAULT_PAGE_SIZE = 1
    DEFAULT_BD = 'users.db'
    con = sqlite3.connect(DEFAULT_BD, check_same_thread=False)

    app = Flask(__name__)
    app.secret_key = "POKEDEX.mobile"
except (RuntimeError, TypeError, NameError):
    raise Exception(f'''/!\ Can't init the website ...\nRuntimeError : {RuntimeError}\nTypeError : {TypeError}\nNameError : {NameError})''')

try:
    cur = con.cursor()
        # Create table users
    cur.execute('''CREATE TABLE users
                (id INTEGER PRIMARY KEY AUTOINCREMENT, pseudo text, name text, surname text, mail text, age real, password text, last_key text)''')
        # Insert a row of data to create the admin acount
    cur.execute("INSERT INTO users VALUES (0,'admin','admin','admin','matteo.cuisset@gmail.com',19,'1234','')")
        # Save (commit) the changes
    con.commit()
except :
    #raise Exception('Erreur lors de la création de la BD ...')
    pass


class PageForm(FlaskForm):
    numero = StringField('numero', validators=[DataRequired()])
    size = IntegerField('size', validators=[DataRequired()])

class UserForm(FlaskForm):
    pseudo = StringField('pseudo', validators=[DataRequired()])
    key = IntegerField('key', validators=[DataRequired()])

@app.route("/", methods=['GET', 'POST'])
def index():
    page_form = PageForm()
    if page_form.validate_on_submit():
        location = int(page_form.numero.data)
        nb_pokemon_by_page = int(page_form.size.data)
    else :
        location = DEFAULT_PAGE
        nb_pokemon_by_page = DEFAULT_PAGE_SIZE
    pokemons = requests.get(f'https://pokeapi.co/api/v2/pokemon/?limit={nb_pokemon_by_page}&offset={location}')
    return render_template('index.html', pekemons = pokemons.json())


def gen_key(size : int = DEFAULT_KEY_SIZE)-> str :
    return str(int(random()*10**size))

@app.route('/login', methods=['POST'])
def login():
    # Vérifiez les informations d'identification ici
    cur = con.cursor()
    cur.execute('''SELECT id FROM users WHERE pseudo = ? and password = ?''',(request.form.get('pseudo'),request.form.get('password')))
    exist = cur.fetchone()
    if exist :
        cur.execute('''UPDATE users SET last_key = ? WHERE id = ?''',(gen_key(),exist[0]))
        con.commit()
        return f'connected !!'
    con.commit()
    return redirect('/')
