from flask import Flask, render_template, request

from flask import Flask
from flask import render_template


app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


database = {'Alexandra': 'Vallet'}

@app.route('/Login')
def login():
    return render_template('login.html')

@app.route('/form_login', methods=['POST', 'GET'])
def returnLogin():
    name1 = request.form['username']
    pwd = request.form['password']
    if name1 not in database or database[name1] != pwd:
        return render_template('login.html',
                                  info='Invalid User Or Password !')
    else:
        return render_template('form_login.html')


if __name__ == '__main__':
    app.run()
