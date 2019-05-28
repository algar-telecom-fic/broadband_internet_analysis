from flask import render_template, flash, redirect, url_for, send_from_directory, request
from app.controllers.utils import allowed_file
from app import app
import os
from werkzeug.utils import secure_filename
from app.controllers.gpon_portas_api import gpon_portas
from app.controllers.trafego_api import teste

@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/gpon")
def gpon():
    return render_template('gpon/gpon.html')


@app.route("/tstdouble", methods=['GET', 'POST'])
def tstdouble():
    if request.method == 'POST':
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

        if file1 and allowed_file(file1.filename):
            filename = secure_filename(file1.filename)
            fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file1.save(fullpath)

        if file2 and allowed_file(file2.filename):

            filename = secure_filename(file2.filename)
            fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file2.save(fullpath)


    return render_template('infoPreencher.html')



#addres to download something you already uploaded
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
