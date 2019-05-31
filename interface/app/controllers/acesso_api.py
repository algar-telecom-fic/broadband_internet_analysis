from app import app
from flask import render_template, flash, request, redirect, url_for, send_from_directory
from app.controllers.utils import allowed_file, make_two_uploads, make_one_upload, read_json
from werkzeug.utils import secure_filename
import os
import sys


@app.route("/voz_fixa/acesso", methods=['GET', 'POST'])
def acesso():
    if request.method == 'POST':



        configs = read_json(os.path.abspath('../voz_fixa/acesso/files/config.json'))
        file1 = make_one_upload(request, configs["actual_filepath"])
        file2 = make_one_upload(request, configs["base_filepath"])
        file3 = make_one_upload(request, configs["regional_filepath"])



        sys.path.append(os.path.abspath('../voz_fixa/acesso'))
        import main
        main.main(request.form.get('DateAtual'), request.form.get('DateAntiga'))
        sys.path.remove(os.path.abspath('../voz_fixa/acesso'))



    return render_template('voz_fixa/acesso.html')
