from flask import flash
from app import app
from werkzeug.utils import secure_filename
import os


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def make_one_upload(request):
    file1 = None
    if 'file1' not in request.files:
        flash('No file1')
        return None
    else:
        file1 = request.files['file1']

    if file1.filename == '':
        flash('No file1 selected')
        return None

    if file1 and allowed_file(file1.filename):
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
