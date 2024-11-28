# =============================== IMPORTS ZONE ===============================
import sqlite3

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, InputRequired, ValidationError
from wtforms import StringField, SubmitField
from unidecode import unidecode
# personnal modulespython3 -m pip uninstall flask-wtf wtforms flask jinja2 click werkzeug markupsafe itsdangerouspip install Flask-WTF
import pokedexmobile.utils.search_engine as search_engine

search_engine.ECO = True
from debug_sys import Logger
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# =============================== INIT ZONE ===============================
debug_sys = Logger()
API_URL = "https://api-pokemon-fr.vercel.app/api/v1/pokemon"
API_HEADER = {
    "User-Agent": "RobotPokemon",
    "From": "adresse[at]domaine[dot]com",
    'Content-type': 'application/json'
}
MAX_SUGGESTION = 6

app = Flask(__name__, static_url_path='',
            static_folder='assets',
            template_folder='views')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'MSI c kro bien !'
app.app_context().push()
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class SearchForm(FlaskForm):
    recherche = StringField('nom du pokemon', validators=[DataRequired()])


database = {'Alexandra': 'Vallet'}

@app.route('/favoris', methods=["GET", "POST"])
@login_required
def favoris():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    poke = cur.execute("SELECT * FROM avoris WHERE id_user="+current_user.get_id()).fetchall()
    conn.commit()
    pokemons = []
    for pokemon in poke :
        pokemons.append(search_engine.infos_on(pokemon[2]))
    cur.close()
    conn.close()
    return render_template('favoris.html',pokemons=pokemons)



@app.route('/addFavoris/<id>',methods=["GET", "POST"])
@login_required
def addFavoris(id):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO avoris(id_user,id_pokemon) VALUES ("+current_user.get_id()+","+id+")")
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('pokemon_view',id=id))


@app.route('/Login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    flash("Tu as été déconnecté !")
    return redirect(url_for('login'))

@app.route('/form_login', methods=['POST', 'GET'])
def returnLogin():
    name1 = request.form['username']
    pwd = request.form['password']
    if name1 not in database or database[name1] != pwd:
        return render_template('login.html',
                               info='Invalid User Or Password !')
    else:
        return render_template('form_login.html')


@app.route('/Register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/form_register', methods=['POST', 'GET'])
def returnRegister():
    name = request.form['username']
    pwd = request.form['password']
    email = request.form['email']
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)


@app.template_filter('basic_format')
def basic_format(input_str: str):
    return unidecode(input_str.lower())


# =============================== MAIN ZONE ===============================
@app.route('/')
def index():
    return redirect(url_for('fr'))


@app.route('/fr', methods=['GET', 'POST'])
def fr():
    poke_name_form = SearchForm()
    if poke_name_form.validate_on_submit():
        search_result = search_engine.search(poke_name_form.recherche.data, 'fr')[0]
        debug_sys.log('SEARCH', f'''{poke_name_form.recherche.data} => {search_result}''')
        return redirect(url_for('pokemon_view', id=search_result))
    return render_template('index.html', form=poke_name_form)


@app.route('/fr/<id>')
def pokemon_view(id):
    poke_name_form = SearchForm()
    poke_infos = search_engine.infos_on(id)
    debug_sys.log('INFO', str(poke_infos))
    try:
        if poke_infos['status'] == 404:
            debug_sys.log('404', f'''{poke_infos['message']} : "/{id}"''')
        return f'''404 : {poke_infos['message']}"'''
    except:
        pass
    intitule = ['Vie', 'Attaque', 'Deffense', 'Attaque spéciale', 'Deffense spéciale', 'Vitesse']
    stats = [{'intitule': i, 'stat': s, 'value': v} for i, s, v in
             zip(intitule, poke_infos['stats'].keys(), poke_infos['stats'].values())]
    return render_template('pokemon_view.html', form=poke_name_form, poke_infos=poke_infos, stats=stats)


# =============================== TEST ZONE ===============================
from flask import request, jsonify


@app.route('/test/<id>', methods=['GET'])
def search_test(id):
    poke_name_form = SearchForm()
    poke_infos = search_engine.infos_on(id)
    debug_sys.log('INFO', str(poke_infos))
    try:
        if poke_infos['status'] == 404:
            debug_sys.log('404', f'''{poke_infos['message']} : "/{id}"''')
        return f'''404 : {poke_infos['message']}"'''
    except:
        pass
    return render_template('test_page.html', form=poke_name_form, poke_infos=poke_infos)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    suggestions = []
    for id in search_engine.search(query, 'fr')[:MAX_SUGGESTION]:
        information = search_engine.infos_on(id)
        suggestions.append((information['name']['fr'], id, information['sprites']['regular']))
    debug_sys.log('SUGGEST', f'query={query} : ' + str(suggestions))
    return jsonify(suggestions)


# AUTHENTIFICATION

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})
    password = StringField('password', validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("That username already exists. Please choose a different one.")


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})
    password = StringField('password', validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
