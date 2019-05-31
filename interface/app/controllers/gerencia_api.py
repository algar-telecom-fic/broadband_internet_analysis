from app import app
from flask import render_template, flash, request, redirect, url_for, send_from_directory
from app.controllers.utils import allowed_file, make_two_uploads, make_one_upload, read_json
from werkzeug.utils import secure_filename
import os
import sys


@app.route("/gerencia", methods=['GET', 'POST'])
def gerencia():
    if request.method == 'POST':

        configs = read_json(os.path.abspath('../gerencia/files/config.json'))
        file1 = make_one_upload(request, configs['filepath'])
        sys.path.append(os.path.abspath('../gerencia'))
        import main
        main.main()
        sys.path.remove(os.path.abspath('../gerencia'))

    return render_template('gerencia.html')
