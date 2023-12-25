from flask import Flask
from app.Models.Model import db
from app.Controllers import EmployeeController
import Route

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table(): db.create_all()


Route.resource('/data',EmployeeController)


app.run(host='localhost', port=5000)
