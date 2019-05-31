from app import app
from flask import render_template, flash, request, redirect, url_for, send_from_directory
from app.controllers.utils import allowed_file, make_two_uploads, make_one_upload, read_json
from werkzeug.utils import secure_filename
import os
import sys


@app.route("/metro", methods=['GET', 'POST'])
def metro():
    if request.method == 'POST':
        configs = read_json(os.path.abspath('../metro/files/config.json'))
        file1 = make_one_upload(request, configs['csv_filepath'])
        sys.path.append(os.path.abspath('../metro'))
        import main
        main.main()
        sys.path.remove(os.path.abspath('../metro'))


    return render_template('metro.html')
