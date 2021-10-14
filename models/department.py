from db import db

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    