from flask import render_template, flash, redirect, url_for, send_from_directory
from app import app

from app.controllers.gpon_portas_api import gpon_portas
from app.controllers.trafego_api import teste

@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/gpon")
def gpon():
    return render_template('gpon/gpon.html')



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
