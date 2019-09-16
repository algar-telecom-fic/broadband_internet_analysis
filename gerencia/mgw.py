import subprocess
import json
import utils
import sys
sys.path.append("/home/otsuka/Documents/Projects/doing/gerencia")
from my_sql import mySQL
from datetime import datetime, date, time


def main():
	fans  = []
	dirt  = '/home/otsuka/Documents/Projects/doing/gerencia/'
	mgw_files  = read_json(dirt + "files/mgw_config.json")
	date_files = read_json(dirt + "files/dates_config.json")
	subprocess.call(['rm', '-r', 'mgw'])
	subprocess.call(['unzip', 'mgw.zip', '-d', 'mgw'])
	dictf = read_json(dirt + 'files/mgw_elem.json')
	for filename in dictf:
		ans = []
		if filename.find('no config') == -1:
			ans = utils.build_result_commom (dirt + 'mgw/' + filename)
		else:
			ans = utils.build_result_final (dirt + 'mgw/' + filename)
		ans['Localidade'] = dictf[filename][0]
		ans['Estacao']    = dictf[filename][1]
		ans['Elemento']   = dictf[filename][2]
		fans.append(ans)
	filepath  = mgw_files ["database_credentials"]
	db_name   = mgw_files ["database_name"]
	mgw_name  = mgw_files ["table_name"]
	mgw_i     = mgw_files ["table_info"]
	date_name = date_files["table_name"]
	date_i    = date_files["table_info"]
	credentials = read_json(filepath)
	db = mySQL(credentials, db_name)
	mgw_i  = read_json(mgw_i)
	date_i = read_json(date_i)
	remove_info(db, mgw_name)
	db.insert_into(mgw_name, mgw_i, fans)
	dt = date.today()
	command = ('UPDATE ' + date_name + 
			  ' SET date = "' + str(dt) +
			  '" WHERE id = 2')
	db.cursor.execute(command) 
	db.connection.commit()


def open_file(filepath, fun_kappa):
	with open(filepath, "r", encoding='ISO-8859-1') as file:
		return fun_kappa(file)


def read_json(filepath):
	with open(filepath, 'r') as file:
		return json.loads(file.read(), encoding = 'utf-8')


def remove_info(db, table_name):
	command = "DELETE FROM " + table_name
	db.cursor.execute(command)
	db.connection.commit()
	command = "ALTER TABLE " + table_name + " AUTO_INCREMENT=1"
	db.cursor.execute(command)


main()