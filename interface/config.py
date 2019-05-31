import os

DEBUG = True
HOME = os.environ.get('HOME', '')
UPLOAD_FOLDER = HOME + '/pastaDosUploads'
PATH_GPON_PORTAS = HOME + '/broadband_internet_analysis/gpon/ports'
PATH_VOZ_FIXA = HOME + '/broadband_internet_analysis/voz_fixa/area_local'
ALLOWED_EXTENSIONS = ['csv', 'xlsx', 'png', 'txt']
SECRET_KEY = os.urandom(16)
