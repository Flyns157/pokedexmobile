#=============================== IMPORTS ZONE ===============================
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField
import requests
# personnal modules
import search_engine
import debug_sys


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

class SearchForm(FlaskForm):
    recherche = StringField('nom du pokemon', validators=[DataRequired()])

if __name__ == '__main__':
    app.run()


#=============================== MAIN ZONE ===============================
@app.route('/', methods=['GET', 'POST'])
def index():
    poke_name_form = SearchForm()
    if poke_name_form.validate_on_submit():
        search_result = search_engine.search_result(search_engine.search_engine(poke_name_form.pokemon.data))[0][0]
        debug_sys.log('SEARCH',f'''{poke_name_form.recherche.data} => {search_result}''')
        return redirect(url_for('pokemon_view', id = search_result))
    return render_template('index.html', form = poke_name_form)

@app.route('/<id>')
def pokemon_view(id):
    poke_name_form = SearchForm()
    poke_infos = requests.get(f"{API_URL}/{id}",API_HEADER).json()
    debug_sys.log('INFO',str(poke_infos)[:100])
    try:
        if poke_infos['status'] == 404:
            debug_sys.log('404',f'''{poke_infos['message']} : "/{id}"''')
        return f'''404 : {poke_infos['message']}"'''
    except:
        pass
    return render_template('pokemon_view.html', form = poke_name_form, poke_infos = poke_infos)