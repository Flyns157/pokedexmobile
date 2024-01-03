from app.app import app
from app.Models.Model import db
from app.Controllers import EmployeeController
from Route import resource


# @app.before_first_request
# def create_table(): 
with app.app_context():
    db.create_all()


resource('/data',EmployeeController)


app.run(host='localhost', port=5000)
