from app import app
from flask import render_template, flash, request, redirect, url_for, send_from_directory
from app.controllers.utils import allowed_file, make_two_uploads, make_one_upload, read_json
from werkzeug.utils import secure_filename
import os
import sys
import datetime

@app.route("/gpon/trafego", methods=['GET', 'POST'])
def gpon_trafego():
    if request.method == 'POST':
        configs = read_json(os.path.abspath('../gpon/traffic/config.json'))
        file1 = make_one_upload(request, configs["current_filepath"], 'file1')
        file2 = make_one_upload(request, configs["ports_filepath"], 'file2')
        file3 = make_one_upload(request, configs["ring_filepath"], 'file3')
        file4 = make_one_upload(request, configs["exceptions_filepath"], 'file4')

        print(configs["ports_filepath"])

        """
        sys.path.append(os.path.abspath('../gpon/traffic/'))
        import main
        main.main()
        sys.path.remove(os.path.abspath('../gpon/traffic/'))
        """


    return render_template('gpon/trafego.html')
