from app import app
from flask import render_template, flash, request, redirect, url_for, send_from_directory
from app.controllers.utils import allowed_file, make_two_uploads
from werkzeug.utils import secure_filename
import os
import sys


@app.route("/vox_fixa/area_local/", methods=['GET', 'POST'])
def area_local():
    if request.method == 'POST':
        file1, file2 = make_two_uploads(request)
        sys.path.insert(0, app.config['PATH_VOZ_FIXA'])
        from read_vantive import processVantive
        #from read_vantive import testaVantive
        from read_anatel import processAnatel
        #from read_anatel import testaAnatel

        processAnatel(file1)
        processVantive(file2)

    return render_template('voz_fixa/area_local.html')
