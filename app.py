from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, IntegerField
import requests

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')

app.secret_key = "MSI c kro bien !"

class PokeNameForm(FlaskForm):
    pokemon = StringField('nom du pokemon', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    poke_name_form = PokeNameForm()
    if poke_name_form.validate_on_submit():
        headers = {
            "User-Agent": "RobotPokemon",
            "From": "adresse[at]domaine[dot]com",
            'Content-type': 'application/json'
        }
        print('pas flop')
        return str(requests.get(f"https://api-pokemon-fr.vercel.app/api/v1/pokemon/{poke_name_form.pokemon.data}",headers).json())
    print('flop')
    return render_template('index.html', form = poke_name_form)


if __name__ == '__main__':
    app.run()