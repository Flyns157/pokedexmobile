#=============================== IMPORTS ZONE ===============================
import Route
from app.app import app
from unidecode import unidecode
from app.Models.Model import db
from flask import redirect,url_for
from app.Controllers import PokemonController
from app.Controllers import EmployeeController


#================================ INIT ZONE ================================
# @app.before_first_request
# def create_table(): 
with app.app_context():db.create_all()

@app.template_filter('basic_format')
def basic_format(input_str : str):return unidecode(input_str.lower())


#================================ MAIN ZONE ================================
# --------------------------------------------------------------------------
#  Web Routes
# --------------------------------------------------------------------------
# Here is where you can register web routes for your application. These
# routes are loaded by the RouteServiceProvider and all of them will
# be assigned to the "web" middleware group. Make something great!
@app.route('/')
def home():return redirect(url_for('fr'))
@app.route('/suggest', methods=['POST'])
def suggest():PokemonController.suggest()
@app.route('/search', methods=['POST'])
def search():PokemonController.search()


Route.resource('/fr',PokemonController)
# Route.resource('/data',EmployeeController)


app.run(host='localhost', port=5000)