import json
import sys
sys.path.append("/home/otsuka/Documents/Projects/doing/gerencia")
from my_sql import mySQL
from datetime import datetime, date, time


def main():
	dirt  = '/home/otsuka/Documents/Projects/doing/gerencia/files/'
	mgw_db = read_json(dirt + "mgw_config.json")
	base_db = read_json(dirt + "base_config.json")
	date_db = read_json(dirt + "dates_config.json")
	credentials = read_json(dirt + 'credentials.json')
	db = mySQL(credentials, mgw_db["database_name"])
	ans = db.select_from("mgw", ["Elemento", "Ocupado"])
	fans = []
	for row in ans:
		fool = {}
		fool["Elemento"] = row[0]
		fool["Ocupado"] = row[1]
		fans.append(fool)
	remove_info(db, base_db["table_name"])
	db_i = read_json(base_db["table_info"])
	db.insert_into(base_db["table_name"], db_i, fans)

	date_name = date_db["table_name"]
	dt = date.today()
	command = ('UPDATE ' + date_name + 
			  ' SET date = "' + str(dt) +
			  '" WHERE id = 1')
	db.cursor.execute(command) 
	db.connection.commit()



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