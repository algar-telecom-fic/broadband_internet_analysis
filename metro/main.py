import csv
import json
import sys
sys.path.append("/home/gardusi/github/sql_library")
from sql_json import mySQL


def build_result(file):
	csv_reader = csv.reader(file, delimiter=',')
	line_count = 0
	result = []
	months = []
	for row in csv_reader:
		data = {}
		if line_count == 0:
			months = row[9:]
			for month in months:
				db_i[month] = 'TINYTEXT'
		else:
			data = {
				"Estado": row[0],
				"Cidade": row[1],
				"Anel": row[2],
				"Speed": row[3],
				"Informacao": row[4],
				"Traffic_100%": row[5],
				"Traffic_95%": row[6],
				"Traffic_Gbps": row[7],
				"TX": row[8]
			}
			for idx, m in enumerate(months):
				data[m] = row[idx+9]
			result.append(data)
		line_count += 1
	return result


def db_inserction(filepath, db_name, tb_name, docs):
	credentials = read_json(filepath)
	db = mySQL(credentials, db_name)
	print(db_i)
	db.create_table(tb_name, db_i)
	db.insert_into(tb_name, db_i, docs)


def main():
	files = read_json("/home/otsuka/doing/metro/files/config.json")
	items = open_file(files["csv_filepath"], build_result)
	db_inserction(
		files["database_credentials"],
		files["database_name"],
		files["table_name"],
		items
	)


def open_file(file_path, fun_kappa):
	with open(file_path, "r", encoding='ISO-8859-1') as file:
		return fun_kappa(file)


def read_json(filepath):
	with open(filepath, 'rb') as file:
		return json.load(file, encoding = 'utf-8')


db_i = read_json("/home/otsuka/doing/metro/files/table_info.json")
main()