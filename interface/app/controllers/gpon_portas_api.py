from app import app
from flask import render_template, flash, request, redirect, url_for, send_from_directory, send_file
from app.controllers.utils import allowed_file, make_two_uploads, make_one_upload, read_json
from werkzeug.utils import secure_filename
import os
import sys
from datetime import datetime



@app.route("/gpon/portas/", methods=['GET', 'POST'])
def gpon_portas():
    if request.method == 'POST':
        hoje = request.form.get('DateAtual')
        d, m, y = hoje.split('/')
        hoje = datetime(int(y), int(m), int(d))

        configs = app.config
        filepath = configs['PATH_GPON_PORTAS'] + 'data/current_circuito.csv'
        file1 = make_one_upload(request, filepath, 'file1')

        sys.path.append(os.path.abspath('../gpon/ports/piloto/'))
        from main import main

        main(filepath, hoje)
        sys.path.remove(os.path.abspath('../gpon/ports/piloto/'))


        filename1 = "Portas_CTO_" + hoje.strftime("%d-%m-%Y") + ".csv"
        filename2 = "Taxa_crescimento_" + hoje.strftime("%d-%m-%Y") + ".csv"

        return redirect(url_for('download_gpon_portas', filename1=filename1, filename2=filename2))
    return render_template('gpon/portas.html')

@app.route("/gpon/portas/download_files/<filename1>&<filename2>", methods=['GET', 'POST'])
def download_gpon_portas(filename1, filename2):
    #print(f"chegeui aqui pelo menos\npath: {os.path.abspath('../gpon/ports/piloto/data/') }\nfilename:{filename1}")
    return render_template('gpon/portas_download.html', filename1=filename1, filename2=filename2)


@app.route('/download/<filename>', methods=['GET', 'POST'])
def downloadFile(filename):
    return send_from_directory(os.path.abspath("../gpon/ports/piloto/data/"), filename)
