from app import app
from flask import render_template, flash, request, redirect, url_for, send_from_directory
from app.controllers.utils import allowed_file, make_two_uploads, make_one_upload
from werkzeug.utils import secure_filename
import os
import sys


@app.route("/gerencia", methods=['GET', 'POST'])
def gerencia():
    if request.method == 'POST':
        file1 = make_one_upload(request)

        """
        sys.path.insert(0, app.config['PATH_VOZ_FIXA'])
        from read_vantive import processVantive
        #from read_vantive import testaVantive
        from read_anatel import processAnatel
        #from read_anatel import testaAnatel

        processAnatel(file1)
        processVantive(file2)
        """

    return render_template('gerencia.html')
