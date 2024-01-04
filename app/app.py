#=============================== IMPORTS ZONE ===============================
from flask import Flask
from random import random
from .Models.Model import db
from flask_wtf import FlaskForm
from wtforms import StringField
import myLibs.debug_sys as debug_sys
from wtforms.validators import DataRequired


#=============================== INIT ZONE ===============================
API_URL = "https://api-pokemon-fr.vercel.app/api/v1/pokemon"
API_HEADER = {
    "User-Agent": "RobotPokemon",
    "From": "adresse[at]domaine[dot]com",
    'Content-type': 'application/json'
}
MAX_SUGGESTION = 6

app = Flask(__name__, static_url_path='',
            static_folder='public',
            template_folder='resources/view')

app.secret_key = "".join(chr(int(random()*100))for _ in range(20))
print(app.secret_key)
debug_sys.log('INFO',f'''!!! Important !!! => $env:FLASK_APP.secret_key = "{app.secret_key}"''')


class SearchForm(FlaskForm):recherche = StringField('nom du pokemon', validators=[DataRequired()])


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# DEBUG
# import os
# print("app ::: ",os.getcwd())