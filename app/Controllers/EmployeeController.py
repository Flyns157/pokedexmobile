from flask import render_template,request,redirect,abort,Request
from app.Models.Employee import db, Employee


# Display a listing of the resource.
def index():
    employees = Employee.query.all()
    return render_template('datalist.html', employees=employees)


# Show the form for creating a new resource.
def create():
    if request.method == 'GET':return render_template('createpage.html')
    if request.method == 'POST':store(request)


# Store a newly created resource in storage.
def store(request : Request):
    employee_id = request.form['employee_id']
    name = request.form['name']
    age = request.form['age']
    position = request.form['position']
    employee = Employee(employee_id, name, age, position)
    db.session.add(employee)
    db.session.commit()
    return redirect('/data')


# Display the specified resource.
def show(id):
    employee = Employee.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee=employee)
    return f"Employee with id ={id} Does not exist"


# Show the form for editing the specified resource.
def edit(id):pass


# Update the specified resource in storage.
def update(id):
    employee = Employee.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            employee = Employee(
                employee_id=id, name=name, age=age, position=position)
            db.session.add(employee)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} Does not exist !"

    return render_template('update.html', employee=employee)

# Remove the specified resource from storage.
def destroy(id):
    employee = Employee.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect('/data')
        abort(404)
    return render_template('delete.html')