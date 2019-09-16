import json
import sys
sys.path.append("/home/otsuka/Documents/Projects/doing/gerencia")
from my_sql import mySQL


def main():
	fans = []
	dirt  = '/home/otsuka/Documents/Projects/doing/gerencia/files/'
	files = read_json(dirt + "base_config.json")
	dictf = read_json(dirt + 'base_elem.json')
	for elem in dictf:
		ans = {}
		ans["Elemento"] = elem
		ans["Ocupado"] = dictf[elem]
		fans.append(ans)
	db_inserction(
		files["database_credentials"],
		files["database_name"],
		files["table_name"],
		files["table_info"],
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
	db_i = read_json(db_i)
	remove_info(db, tb_name)
	db.insert_into(tb_name, db_i, docs)


def remove_info(db, table_name):
	command = "DELETE FROM " + table_name
	db.cursor.execute(command)
	db.connection.commit()
	command = "ALTER TABLE " + table_name + " AUTO_INCREMENT=1"
	db.cursor.execute(command)


main()