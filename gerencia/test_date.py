import json
import refresh_base
from datetime import datetime, date, time
import sys
sys.path.append("/home/otsuka/Documents/Projects/doing/gerencia")
from my_sql import mySQL

def main():
	ans = []
	dirt  = '/home/otsuka/Documents/Projects/doing/gerencia/files/'
	date_db = read_json(dirt + "dates_config.json")
	credentials = read_json(dirt + 'credentials.json')
	db = mySQL(credentials, date_db["database_name"])
	teste = db.select_from(date_db["table_name"], ["date"])
	print(teste)
	for i in teste:
		for j in i:
			ans.append(j)
	print(ans)
	diff = ans[1] - ans[0]
	print(diff.days)


def read_json(filepath):
	with open(filepath, 'r') as file:
		return json.loads(file.read(), encoding = 'utf-8')


main()