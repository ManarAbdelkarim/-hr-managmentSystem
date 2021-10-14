from flask_restful import Api
from flask import Flask , current_app,request
from os import environ,path
from resourses.routes import Application
from models.department import Department
import sqlite3
import mariadb
from app import app
DATABASE_CONFIG={
  "USER":environ.get("USER"),
  "PASSWORD":environ.get("PASSWORD"),
  "DATABASE_PORT":environ.get("DATABASE_PORT"),
  "HOST":environ.get("HOST"),
  "DATABASE_NAME":environ.get("DATABASE")
}
user,password,port,host,name = DATABASE_CONFIG.values()

UPLOAD_FOLDER = 'static/uploads'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['BUNDLE ERRORS'] = True
app.secret_key = environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()
    seed_department()
@app.context_processor
def context_processor():
    return dict(app=app)
api.add_resource(Application, '/application',
                 '/application/<int:application_id>')

@app.route('/department', methods=['POST'])
def department():

    request_data = request.get_json()
    name = request_data['name']
    department = Department(name=name)
    db.session.add(department)
    db.session.commit()
    return {"message": "good job"} 
def seed_department():
    departments_names = ['IT','HR','Finance']
    for department_name in departments_names:
        department=Department(name=department_name)
        db.session.add(department)
    db.session.commit()

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=environ.get("PORT"),debug=environ.get("DEBUG"))

