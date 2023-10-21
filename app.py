#=============================== IMPORTS ZONE ===============================
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField
import requests
from datetime import datetime
import search_engine_v1 as search_engine


#=============================== INIT ZONE ===============================
API_URL = "https://api-pokemon-fr.vercel.app/api/v1/pokemon"
API_HEADER = {
    "User-Agent": "RobotPokemon",
    "From": "adresse[at]domaine[dot]com",
    'Content-type': 'application/json'
}

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')

app.secret_key = "MSI c kro bien !"

class PokeNameForm(FlaskForm):
    pokemon = StringField('nom du pokemon', validators=[DataRequired()])

if __name__ == '__main__':
    app.run()


#=============================== MAIN ZONE ===============================
@app.route('/', methods=['GET', 'POST'])
def index():
    poke_name_form = PokeNameForm()
    if poke_name_form.validate_on_submit():
        return redirect(url_for('pokemon', name=poke_name_form.pokemon.data))
    return render_template('index.html', form = poke_name_form)

@app.route('/<name>')
def pokemon_view(name):
    poke_name_form = PokeNameForm()
    search_result = search_engine.search_result(search_engine.search_engine(name))[0][0]
    poke_infos = requests.get(f"{API_URL}/{search_result}",API_HEADER).json()
    if poke_infos['status'] == 404:
        log(f'''404 : {poke_infos['message']} : "/{search_result}"''')
        return f'''404 : {poke_infos['message']}"'''
    log('')
    return render_template('pokemon_view.html', form = poke_name_form, poke_infos = poke_infos)


#=============================== DEBUG ZONE ===============================

# suppression des logs
tmp = open('gaza.log', 'w')
tmp.write('')
tmp.close()

# gestion des logs
num_log = 0
def log(content : str)-> None:
    global num_log
    num_log += 1
    with open('gaza.log', 'a') as file:
        file.write(f'({num_log}) : {datetime.now()} : {content}\n')