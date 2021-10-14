from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField , DateTimeField,RadioField ,FileField
from wtforms.validators import Length,DataRequired
from models.candidate import Candidate
class RegistrationForm(FlaskForm):

    full_name = StringField(label='User Name:',validators=[Length(min=2,max=30),DataRequired()])
    date_of_birth = DateTimeField(label='Date of birth:',format='%Y-%m-%d', validators=[DataRequired()])
    department_id= RadioField(label='department:', choices=[(0,'IT'),(1,'Finance'),(2,'HR')])
    resume = FileField(label="resume")
    submit = SubmitField(label='Submit')
