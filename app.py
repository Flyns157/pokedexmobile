import requests
from flask import Flask
from flask import render_template

import sqlite3

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

@app.route('/test')
def test():
    response = requests.get('https://api-pokemon-fr.vercel.app/api/v1/pokemon')
    return "<h1>"+str(response.json()[730]["name"]["fr"])+"</h1>"+"<br>"+"<img src="+str(response.json()[730]["sprites"]["regular"])+">"