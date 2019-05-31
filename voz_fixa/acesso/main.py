import csv
import json
import math
import sys
from datetime import date
sys.path.append("/home/usrCapacity/broadband_internet_analysis/voz_fixa/acesso/sql_library")
from sql_json import mySQL


def build_dict(station, base, actual, days):
	total = actual[station]["TOTAL"]
	oc = actual[station]["T OCUPADO"]
	disp = actual[station]["T DISPONIVEL"]
	if station not in base:
		cr = "Sem Historico"
		pre_pm = 0
	else:
		cr = ((actual[station]["T OCUPADO"]-base[station]["T OCUPADO"])/days)*30
		if cr != 0:
			pre_pm = disp/cr
		else:
			pre_pm = 0
	if pre_pm < 0:
		pre = "Decrescimento"
	elif pre_pm == 0:
		pre = "Esgotado"
	else:
		aux = math.ceil(pre_pm)
		pre = "Esgota em ate {} meses.".format(aux)
	result = {
		"Estacao": station,
		"Regional": actual[station]["REGIONAL"],
		"Localidade": actual[station]["LOCALIDADE"],
		"Sigla": actual[station]["SIGLA"],
		"Total": total,
		"Ocupados": oc,
		"Disponiveis": disp,
		"Crescimento": cr,
		"Prev_esg_m": pre_pm,
		"Prev_esg": pre
	}
	return result


def build_reg(filepath):
	result = {}
	csv_reader = csv.reader(filepath, delimiter=';')
	line_count = 0
	for row in csv_reader:
		if line_count!=0:
			if row[0] not in result:
				result[row[0]] = [row[1]]
			else:
				if row[1] not in result[row[0]]:
					result[row[0]].append(row[1])
		line_count += 1
	return result


def create(file):
	files = read_json("/home/usrCapacity/broadband_internet_analysis/voz_fixa/acesso/files/config.json")
	reg_dict = open_file(files["regional_filepath"], build_reg)
	csv_reader = csv.reader(file, delimiter=';')
	line_count = 0
	count = 0
	index_loc = 0
	index_sigla = 0
	ports = {}
	for row in csv_reader:
		if line_count == 0:
			for i in row:
				if i == 'Localidade':
					index_loc = count
				elif i == 'Sigla da Estação' or i == "Sigla da Estacao":
					index_sigla = count
				count += 1
		else:
			for city in reg_dict.keys():
				if row[index_loc] in reg_dict[city]:
					region = city
					break
			if row[0] not in ports.keys():
				status = {
					"LOCALIDADE": row[index_loc],
					"SIGLA": row[index_sigla],
					"REGIONAL": region,
					"CONGELADO": 0,
					"DEFEITO": 0,
					"DISPONIVEL": 0,
					"INTERCEPTADO": 0,
					"OCUPADO": 0,
					"OCUPADO FIXA DADOS": 0,
					"OCUPADO RUBI": 0,
					"RESERVA MC": 0,
					"RESERVADO": 0,
					"VAGO": 0,
					"VAGO TP": 0,
					"TOTAL": 0,
					"T OCUPADO": 0,
					"T DISPONIVEL": 0
				}
				status[row[1]] += 1
				ports[row[0]]	= status
			else:
				ports[row[0]][row[1]] += 1
			if (
				row[1] == "INTERCEPTADO" or
				row[1] == "OCUPADO" or
				row[1] == "OCUPADO FIXA DADOS" or
				row[1] == "OCUPADO RUBI"
			):
				ports[row[0]]["T OCUPADO"] += 1
			if row[1] == "VAGO":
				ports[row[0]]["T DISPONIVEL"] += 1
			ports[row[0]]["TOTAL"] += 1
		line_count += 1
	return ports


def date_dif_file(file):
	dates = []
	date_format = "%d/%m/%Y"
	for d in file.readlines():
		for e in d.split():
			dates.append(e)
	datea = dates[2]
	dateb = dates[5]
	dates = []
	datez = []
	for i in datea.split("/"):
		dates.append(int(i))
	for i in dateb.split("/"):
		datez.append(int(i))
	d1 = date(dates[2],dates[1],dates[0])
	d2 = date(datez[2],datez[1],datez[0])
	r = abs(d2-d1).days
	return r



def date_dif_arg(d1,d2):
	dates = []
	datez = []
	for i in d1.split("/"):
		dates.append(int(i))
	for i in d2.split("/"):
		datez.append(int(i))
	d1 = date(dates[2],dates[1],dates[0])
	d2 = date(datez[2],datez[1],datez[0])
	return abs(d2-d1).days


def db_insertion(filepath, db_name, tb_name, db_info, docs):
	credentials = read_json(filepath)
	db_i = read_json(db_info)
	db = mySQL(credentials, db_name)
	db.create_table(tb_name, db_i)
	db.insert_into(tb_name, db_i, docs)


def open_file(file_path, fun_kappa):
	with open(file_path, "r", encoding='ISO-8859-1') as file:
		return fun_kappa(file)


def read_json(filepath):
	with open(filepath, 'rb') as file:
		return json.load(file, encoding = 'utf-8')


def main(d1 = None, d2 = None):
	base_dict = {}
	actual_dict = {}
	reg_dict = {}
	result = {}
	files = read_json("/home/usrCapacity/broadband_internet_analysis/voz_fixa/acesso/files/config.json")
	base_dict = open_file(files["base_filepath"], create)
	actual_dict = open_file(files["actual_filepath"], create)
	if d1 == None or d2 == None:
		days = open_file(files["dates_filepath"], date_dif_file)
	else:
		days = date_dif_arg(d1, d2)
	for key in actual_dict:
		result[key] = build_dict(key, base_dict, actual_dict, days)
	items = []
	for i in result.keys():
		items.append(result[i])
	db_insertion(
		files["database_credentials"],
		files["database_name"],
		files["table_name"],
		files["table_info"],
		items
	)


if __name__ == "__main__":
	main()
