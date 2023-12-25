from flask import Flask, render_template, request, redirect
from app.Models.Employee import db, Employee


@app.route('/data/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = Employee(
            employee_id=employee_id, name=name, age=age, position=position)
        db.session.add(employee)
        db.session.commit()
        return redirect('/data')


@app.route('/data')
def RetrieveList():
    employees = Employee.query.all()
    return render_template('datalist.html', employees=employees)


@app.route('/data/<int:id>')
def RetrieveEmployee(id):
    employee = Employee.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee=employee)
    return f"Employee with id ={id} Doenst exist"


@app.route('/data/<int:id>/update', methods=['GET', 'POST'])
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
        return f"Employee with id = {id} Does nit exist"

    return render_template('update.html', employee=employee)


@app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    employee = Employee.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect('/data')
        abort(404)

    return render_template('delete.html')