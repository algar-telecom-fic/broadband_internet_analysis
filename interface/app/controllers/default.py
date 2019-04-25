from flask import render_template, request, flash, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from app import app

@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/gpon")
def gpon():
    return render_template('gpon/gpon.html')

@app.route("/gpon/portas/", defaults={'choice':None}, methods=['GET', 'POST'])
@app.route("/gpon/portas/<choice>", methods=['GET', 'POST'])
def gpon_portas(choice):
    if request.method == 'POST' and choice != None:
    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fullpath)

            import sys
            sys.path.insert(0, app.config['PATH_GPON_PORTAS'])
            from main import Main
            if choice == 'cidades':
                Main(fullpath, "")
            elif choice == 'dados':
                Main("", fullpath)

            flash("Atualizacao feita.")


    return render_template('gpon/portas.html')


ALLOWED_EXTENSIONS = ['csv', 'xlsx']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', defaults = {'var': 'tchau'})
@app.route('/teste/<var>')
def teste(var):
    if var == 'oi':
        return "kkkkkk"
    elif var == 'tchau':
        return ":((("

    return "oops"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
