from flask import flash
from app import app
from werkzeug.utils import secure_filename
import os
import json

def read_json(filepath):
	with open(filepath, 'r') as file:
		return json.loads(file.read(), encoding = 'utf-8')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def make_one_upload(request, desiredName = "", current_file = 'file1'):
    file1 = None
    if current_file not in request.files:
        flash('No '+ current_file)
        return None
    else:
        file1 = request.files[current_file]

    if file1.filename == '':
        flash('No file selected')
        return None

    if desiredName != "":
        fullpath1 = desiredName
        file1.save(fullpath1)

    elif file1 and allowed_file(file1.filename):
        filename = secure_filename(file1.filename)
        fullpath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file1.save(fullpath1)
        flash('successful upload')

    return fullpath1

def make_two_uploads(request):
    print(request.files)

    file1 = None
    file2 = None
    if 'file1' not in request.files:
        flash('No file1')
    else:
        file1 = request.files['file1']

    if 'file2' not in request.files:
        flash("No file2")
    else:
        file2 = request.files['file2']


    # if user does not select file, browser also
    # submit an empty part without filename
    if file1.filename == '':
        flash('No selected file1')
        #return redirect(request.url)
    if file2.filename == '':
        flash('No selected file2')
        #return redirect(request.url)

    fullpath1 = None
    fullpath2 = None

    if file1 and allowed_file(file1.filename):
        filename = secure_filename(file1.filename)
        fullpath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file1.save(fullpath1)

    if file2 and allowed_file(file2.filename):

        filename = secure_filename(file2.filename)
        fullpath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file2.save(fullpath2)

    return (fullpath1, fullpath2)
