
from flask import request
# from . security import authenticate, identity
from os import environ
from flask_restful import  Resource, reqparse
from models.candidate import Candidate
from helpers.files import *
from helpers.admin import admin_required
from forms.registeration_form import RegistrationForm
import uuid 

@admin_required
@app.route('/uploads/<int:candidateID>' ,methods=['POST','GET'])
def download_file_by_candidate(candidateID):
    candidate = Candidate.query.filter(Candidate.id == candidateID).first_or_404()
    return download_file(candidate.resume)

class Application(Resource):

    # parser = reqparse.RequestParser()
    # parser.add_argument(
    #         'full_name', type=type(str), required=True, help="this feild connot be empty", location=['form'])
    # parser.add_argument(
    #         'date_of_birth', type=type(date), required=True, help="this feild connot be empty")
    # parser.add_argument(
    #         'department_id', type=type(int), required=True, help="this feild connot be empty")
    # parser.add_argument(
    #         'resume', type=type(str), required=True, help="this feild connot be empty", location=['form','files','values','json'])
    
    def post(self):
        try:
            form = RegistrationForm()
            if not request.form.get('full_name'):
                return {'message': 'No data has been received'}, 400
            file = request.files['resume']
            filename = '{}.{}'.format(uuid.uuid4(), file.filename.split('.')[-1])
            if not file_type_validator(filename):
                return {"message":"allowed file types are only 'txt', 'pdf', 'docs'"}, 403
            candidate = Candidate(
                full_name=form.full_name.data, 
                date_of_birth=form.date_of_birth.data, 
                resume=filename,
                department_id=form.department_id.data
            )
            # data = Application.parser.parse_args()
            # candidate = Candidate(data)
            candidate.save_to_db()
            save_resume(file,filename)

            return {"message":"Your Aplication has been send succesully"}, 201
        except:
            return {"message":"An Error happened while saveing data"}, 500
    def get(self):
        pass

    @admin_required
    def get(self, application_id=None):
        if application_id:
            applicant = next(
                filter(lambda x: x.id == application_id, Candidate), None)
            return {'applicant': applicant}, 200 if applicant else 404
        
        candidates_list = Candidate.retrieve_candidates()
        return {'candidates':list(map(lambda candidate:candidate.json() ,candidates_list))}
              





