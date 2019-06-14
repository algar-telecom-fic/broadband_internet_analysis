from app import app
from flask import render_template, flash, request, redirect, url_for, send_from_directory
from app.controllers.utils import allowed_file, make_two_uploads, make_one_upload, read_json
from werkzeug.utils import secure_filename
import os
import sys
import datetime

@app.route("/xdsl/", methods=['GET', 'POST'])
def xdsl():
    if request.method == 'POST':
        configs = read_json(os.path.abspath('../xdsl/config.json'))
        file1 = make_one_upload(request, configs["current_filepath"], 'file1')
        file2 = make_one_upload(request, configs["previous_filepath"], 'file2')

        diaAtual  = request.form.get('DateAtual')
        diaAtual  = datetime.datetime.strptime(diaAtual, '%d/%m/%Y')
        diaAntiga = request.form.get('DateAntiga')
        diaAntiga = datetime.datetime.strptime(diaAntiga, '%d/%m/%Y')

        date_difference = abs( (diaAtual - diaAntiga).days)
        sys.path.append(os.path.abspath('../xdsl/'))
        import main
        main.main(date_difference)
        sys.path.remove(os.path.abspath('../xdsl/'))


    return render_template('xdsl/xdsl.html')
