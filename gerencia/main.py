import subprocess
import json
import utils
import sys
import os
sys.path.append("/home/otsuka/doing/gerencia/piloto_mgw")
from my_sql import mySQL
import datetime


def find_old(estacao, old_cities):
	lo = 0
	hi = len(old_cities) - 1
	while(lo <= hi):
		me = int((lo + hi)/2)
		if old_cities[me][0] == estacao:
			return old_cities[me]
		elif old_cities[me][0] > estacao:
			hi = me-1
		else:
			lo = me+1
	return -1


def main(tod):

	dirt = os.getcwd()
	mgw_files = read_json(dirt + "/files/mgw_config.json")
	filepath = mgw_files ["database_credentials"]
	credentials = read_json(filepath)

	db_name = mgw_files ["database_name"]
	table_name = mgw_files ["table_name"]
	table_info = mgw_files ["table_info"]

	db = mySQL(credentials, db_name)
	mgw_info = read_json(table_info)

	DD = datetime.timedelta(days=180)
	aux_day = tod - DD
	aux_time = datetime.datetime.min.time()
	aux_day = datetime.datetime.combine(aux_day, aux_time)

	query1 = "select distinct Dia from mgw"
	dates = db.executaQuery(query1)
	query_date = tod #default
	for d in reversed(dates):
		if (d[0] <= aux_day):
			query_date = str(d[0]).split()[0]
			break

	query2 = f"select Estacao, Ocupado, Dia from mgw where dia = '{query_date}';"
	old_cities = db.executaQuery(query2)
	old_cities.sort()

	delta = tod - query_date
	delta = delta.days

	fans  = []
	subprocess.call(['rm', '-r', 'mgw'])
	subprocess.call(['unzip', 'mgw.zip', '-d', 'mgw'])
	dictf = read_json(dirt + '/files/mgw_elem.json')
	for filename in dictf:
		old = find_old(dictf[filename][1], old_cities)
		ans = []
		if filename.find('no config') == -1:
			ans = utils.build_result_commom (dirt + '/mgw/' + filename)
		else:
			ans = utils.build_result_final (dirt + '/mgw/' + filename)
		ans['Localidade']    = dictf[filename][0]
		ans['Estacao']       = dictf[filename][1]
		ans['Elemento']      = dictf[filename][2]
		ans['Dia']           = tod
		ans['Crescimento']   = round ( ( ans['Ocupado'] - old[1] ) / delta * 30 )
		ans['Esgotamento_M'] = ""
		try:
			ans['Esgotamento'] = ans['Disponivel'] / ans['Crescimento']
		except ZeroDivisionError:
			ans['Esgotamento'] = 0
		ans['Taxa_Ocupacao'] = ( ans['Capacidade'] - ans['Disponivel'] ) / ans['Capacidade']

		fans.append(ans)

	db.insert_into(table_name, mgw_info, fans)


def read_json(filepath):
	with open(filepath, 'r') as file:
		return json.loads(file.read(), encoding = 'utf-8')


if __name__ == "__main__":
	main(datetime.date(2019, 10, 11))
