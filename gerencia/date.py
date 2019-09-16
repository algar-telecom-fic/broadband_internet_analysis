import subprocess
import json
import utils
import sys
sys.path.append("/home/otsuka/Documents/Projects/doing/gerencia")
from my_sql import mySQL
from datetime import datetime, date, time


def main():
	fans  = []
	ans = {}
	dirt  = '/home/otsuka/Documents/Projects/doing/gerencia/'
	dt = datetime.strptime("11/12/2018", "%d/%m/%Y")
	config = read_json(dirt + "files/dates_config.json")
	ans["options"] = "Base"
	ans["date"] = dt
	fans.append(ans)
	ans = {}
	ans["options"] = "Current"
	ans["date"] = date.today()
	fans.append(ans)
	db_inserction(
		config["database_credentials"],
		config["database_name"],
		config["table_name"],
		config["table_info"],
		fans
	)


def open_file(filepath, fun_kappa):
	with open(filepath, "r", encoding='ISO-8859-1') as file:
		return fun_kappa(file)


def read_json(filepath):
	with open(filepath, 'r') as file:
		return json.loads(file.read(), encoding = 'utf-8')

def db_inserction(filepath, db_name, tb_name, db_i, docs):
	credentials = read_json(filepath)
	db = mySQL(credentials, db_name)
	db.drop_table(tb_name)
	db_i = read_json(db_i)
	db.create_table(tb_name, db_i)
	db.insert_into(tb_name, db_i, docs)


main()