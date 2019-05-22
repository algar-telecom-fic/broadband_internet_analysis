from app import app
from flask import render_template, flash, request, redirect, url_for, send_from_directory
from app.controllers.utils import allowed_file
from werkzeug.utils import secure_filename
import os


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
