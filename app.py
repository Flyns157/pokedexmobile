#=============================== IMPORTS ZONE ===============================
from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField
import requests
# personnal modules
import search_engine
search_engine.ECO = True
import debug_sys


#=============================== INIT ZONE ===============================
API_URL = "https://api-pokemon-fr.vercel.app/api/v1/pokemon"
API_HEADER = {
    "User-Agent": "RobotPokemon",
    "From": "adresse[at]domaine[dot]com",
    'Content-type': 'application/json'
}
MAX_SUGGESTION = 6

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')

app.secret_key = "MSI c kro bien !"

class SearchForm(FlaskForm):
    recherche = StringField('nom du pokemon', validators=[DataRequired()])

if __name__ == '__main__':
    app.run(debug=True)


#=============================== MAIN ZONE ===============================
@app.route('/')
def index():
    return redirect(url_for('fr'))

@app.route('/fr', methods=['GET', 'POST'])
def fr():
    poke_name_form = SearchForm()
    if poke_name_form.validate_on_submit():
        search_result = search_engine.search(poke_name_form.recherche.data,'fr')[0]
        debug_sys.log('SEARCH',f'''{poke_name_form.recherche.data} => {search_result}''')
        return redirect(url_for('pokemon_view', id = search_result))
    return render_template('index.html', form = poke_name_form)

@app.route('/fr/<id>')
def pokemon_view(id):
    poke_name_form = SearchForm()
    poke_infos = search_engine.infos_on(id)
    debug_sys.log('INFO',str(poke_infos))
    try:
        if poke_infos['status'] == 404:
            debug_sys.log('404',f'''{poke_infos['message']} : "/{id}"''')
        return f'''404 : {poke_infos['message']}"'''
    except:
        pass
    return render_template('pokemon_view.html', form = poke_name_form, poke_infos = poke_infos)


#=============================== TEST ZONE ===============================
from flask import request, jsonify

@app.route('/search_test', methods=['GET'])
def search_test():
    poke_name_form = SearchForm()
    return render_template('test_page.html', form = poke_name_form)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    suggestions = []
    for id in search_engine.search(query,'fr')[:MAX_SUGGESTION]:
        information = search_engine.infos_on(id)
        suggestions.append((information['name']['fr'],id,information['sprites']['regular']))
    debug_sys.log('SUGGEST', f'query={query} : ' + str(suggestions))
    return jsonify(suggestions)