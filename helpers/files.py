from os import path
from flask import current_app, send_from_directory
from app import app
from helpers.admin import admin_required
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docs'}

def save_resume(file, filename):
    file.save(
        path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)))

def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

def file_type_validator(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS