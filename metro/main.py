import sys
sys.path.append("/home/gardusi/github/sql_library")
from sql_json import mySQL
from openpyxl import load_workbook
import datetime
import json


def build_ans(filename):
	ans = []
	months = []
	wb = load_workbook(filename)
	ws = wb.get_sheet_names()[0]
	ws = wb.get_sheet_by_name(ws)
	for line, row in enumerate(list(ws.rows)):
		if line == 0:
			for cell in row:
				if(isinstance(cell.value, datetime.datetime)) :
					months.append(date_convert(cell.value))
					db_i[date_convert(cell.value)] = "FLOAT"
		else:
			data = {
				"Estado": row[0].value,
				"Cidade": row[1].value,
				"Anel": row[2].value,
				"Speed": float(row[3].value),
				"Informacao": row[4].value,
				"Traffic_100%": row[5].value,
				"Traffic_95%": row[6].value,
				"Traffic_Gbps": row[7].value,
				"TX": percent_to_float(str(row[8].value))	
			}
			for idx, m in enumerate(months):
				data[m] = row[idx+9].value
			ans.append(data)
	return ans


def date_convert(date):
	timestampStr = date.strftime("%b-%Y")
	return timestampStr


def db_inserction(filepath, db_name, tb_name, docs):
	global db_i
	credentials = read_json(filepath)
	db = mySQL(credentials, db_name)
	db.create_table(tb_name, db_i)
	db.insert_into(tb_name, db_i, docs)


def main():
	global db_i
	data = {}
	db_i = read_json("/home/otsuka/doing/metro/files/table_info.json")
	files = read_json("/home/otsuka/doing/metro/files/config.json")
	ans = build_ans(files["xlsx_filepath"])
	db_inserction(
		files["database_credentials"],
		files["database_name"],
		files["table_name"],
		ans
	)


def percent_to_float(string):
	for ch in string:
		if(ch == '%'):
			return float(string[:-1])/100
	return float(string)


def read_json(filepath):
	with open(filepath, 'r') as file:
		return json.load(file, encoding = 'utf-8')


if __name__ == '__main__':
	main()
