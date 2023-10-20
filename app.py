import requests
from flask import Flask
from flask import render_template

import sqlite3

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

@app.route('/test')
def test():
    response = requests.get('https://api-pokemon-fr.vercel.app/api/v1/pokemon')
    return response.json()


### Base de données ###

try:
    con = sqlite3.connect('pokedex.db', check_same_thread=False)
    cur = con.cursor()
    cur.execute("CREATE TABLE USER (id INTEGER, login TEXT NOT NULL, mdp TEXT NOT NULL)")
    con.commit()
except sqlite3.OperationalError:
    con = sqlite3.connect('pokedex.db', check_same_thread=False)
    con.close()

try:
    con = sqlite3.connect('pokedex.db', check_same_thread=False)
    cur = con.cursor()
    cur.execute("CREATE TABLE POKEMON (id INTEGER, nameFR TEXT, nameEN TEXT, types TEXT, generation INT)")
    con.commit()
except sqlite3.OperationalError:
    con = sqlite3.connect('pokedex.db', check_same_thread=False)
    con.close()

try:
    con = sqlite3.connect('pokedex.db', check_same_thread=False)
    cur = con.cursor()
    cur.execute("CREATE TABLE FAVORI (id_user INTEGER, id_pokemon INTEGER, FOREIGN KEY (id_user) REFERENCES USER (id), FOREIGN KEY (id_pokemon) REFERENCES POKEMON(id))")
    con.commit()
except sqlite3.OperationalError:
    con = sqlite3.connect('pokedex.db', check_same_thread=False)
    con.close()

#Remplissage de la table POKEMON