from flask import Flask
from flask import render_template
import requests

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')

@app.route('/<twa>')
def poke_info(twa = None):
    headers = {
        "User-Agent": "RobotPokemon",
        "From": "adresse[at]domaine[dot]com",
        'Content-type': 'application/json'
    }
    poke_infos = requests.get(f"https://api-pokemon-fr.vercel.app/api/v1/pokemon/{twa}",headers).json()
    return render_template('pokemon_view.html', poke_infos = poke_infos)

if __name__ == '__main__':
    app.run()
