from datetime import datetime
from sqlalchemy import desc
from db import db
from models.department import Department

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    full_name = db.Column(db.String(80), nullable=False, unique=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey(
        'department.id'), nullable=False)
    department = db.relationship('Department', backref='candidate', lazy=True)
    resume = db.Column(db.String(20), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,full_name, date_of_birth, department_id, resume):
        self.full_name = full_name
        self.date_of_birth = date_of_birth
        self.department_id = department_id
        self.resume = resume


    @classmethod
    def retrieve_candidates(cls):
        return cls.query.order_by(desc(cls.registration_date)).all()

    def json(self):
        departmnent = Department.query.filter(self.department_id == Department.id).first_or_404()
        return {
        "full name":self.full_name,
        "date_of_birth":self.prettier_date_of_birth,
        "department_id":departmnent.name,
        "registration_date":self.prettier_registration_date
        }
    @property
    def prettier_date_of_birth(self):
        return datetime.strftime( self.date_of_birth,'%Y-%m-%d')
    @property
    def prettier_registration_date(self):
        return datetime.strftime( self.registration_date ,'%d/%m/%Y %H:%M:%S')

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
 