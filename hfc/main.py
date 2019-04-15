import datetime
import math
import sys
sys.path.append('/home/gardusi/github/sql_library/')
import mysql_json

date = datetime.datetime.now()
database_name = 'kappacidade'
host = '0.0.0.0'
passwd = 'pe'
primary_key = 'id'
user = 'peduardo'
table_name = 'hfc'
table_info = {
  'id': 'INT AUTO_INCREMENT',
  'Capacidade (Mbps)': 'INT',
  'CMTS': 'TINYTEXT',
  'Crescimento mensal (%)': 'DOUBLE',
  'Crescimento mensal (Mbps)': 'INT',
  'Data': 'DATETIME',
  'Node': 'TINYTEXT',
  'Previsão de congestionamento (Mês)': 'DOUBLE',
  'Previsão de congestionamento': 'TINYTEXT',
  'Projeto': 'TINYTEXT',
  'Quantidade de clientes': 'TINYTEXT',
  'Utilização média entre as portadoras (%)': 'DOUBLE',
  'Utilização média entre as portadoras (Mbps)': 'DOUBLE',
}

def build_documents(current_file, previous_file, date_difference):
  global database
  documents = []
  for node_name in database[current_file]:
    try:
      before = database[previous_file][node_name]['usage']
      current = database[current_file][node_name]['usage']
      median = (current - before) / (date_difference / 30)
      increasing_percentage = median / 100.0
      increasing_mbps = round(median * database[current_file][node_name]['capacity'] / 100.0, 2);
      if increasing_mbps == 0:
        prediction_num = 'Estável'
        prediction = 'Estável'
      else:
        kappa = database[current_file][node_name]['capacity']
        keepo = round(database[current_file][node_name]['capacity'] * database[current_file][node_name]['usage'] / 100.0, 2)
        prediction_num = math.ceil((kappa - keepo) / increasing_mbps)
        if value < 0:
          prediction = 'Decrescimento'
        else:
          if value == 1:
            prediction = 'Esgota em até 1 mês'
          elif value > 10:
            prediction = 'Esgota em mais de 10 meses'
          else:
            prediction = 'Esgota em até ' + str(value) + ' meses'
    except Exception as e:
      print(e)
      for j in range(7, 11):
        sheet.cell(row = current_row, column = j).value = 'Sem histórico'

    documents.append({
      'Capacidade (Mbps)': database[current_file][node_name]['capacity'],
      'CMTS': '?',
      'Crescimento mensal (%)': increasing_percentage,
      'Crescimento mensal (Mbps)': increasing_mbps,
      'Data': date,
      'Node': node_name,
      'Previsão de congestionamento (Mês)': prediction_num,
      'Previsão de congestionamento': prediction,
      'Projeto': '?',
      'Quantidade de clientes': '?',
      'Utilização média entre as portadoras (%)': database[current_file][node_name]['usage'] / 100.0,
      'Utilização média entre as portadoras (Mbps)': round(database[current_file][node_name]['capacity'] * database[current_file][node_name]['usage'] / 100.0, 2),
    })
  return documents

def insert_documents(documents):
  db = mysql_json.mySQL(
    database = database_name,
    host = host,
    passwd = passwd,
    user = user,
  )
  db.create_table(
    primary_key = primary_key,
    table_info = table_info,
    table_name = table_name,
  )
  db.insert_into(
    table_name,
    table_info,
    documents,
  )

def main():
  import os
  filepath = os.path.dirname(os.path.abspath(__file__)) + '/' + 'config.txt'
  current_file, previous_file, date_difference = read_config_file(filepath)
  read_file(current_file)
  read_file(previous_file)
  documents = build_documents(current_file, previous_file, date_difference)
  insert_documents(documents)

def read_config_file(filename):
  global database
  database = {}
  try:
    with open(filename, 'r') as config_file:
      v = config_file.readlines()
      current_file = v[0].split('=')[1].strip().split('"')[1].strip()
      previous_file = v[1].split('=')[1].strip().split('"')[1].strip()
      date_difference = int(v[2].split('=')[1].strip().split('"')[1].strip())
      return (current_file, previous_file, date_difference)
  except Exception as e:
    print(e)
    print('Failed to read file: ' + filename)

def read_file(filename):
  global database
  database[filename] = {}
  try:
    with open(filename, 'r', encoding = 'ISO-8859-1') as input_file:
      lines = input_file.readlines()
      for i in range(len(lines)):
        lines[i] = lines[i].strip()
      idx = -1
      while idx + 1 < len(lines):
        idx += 1
        if len(lines[idx]) == 0:
          continue
        node_name = lines[idx]
        qtd_interfaces = 0
        total_capacity = 0
        total_usage = 0
        idx += 2
        while idx + 1 < len(lines):
          idx += 1
          if len(lines[idx]) == 0:
            break
          qtd_interfaces += 1
          v = lines[idx].split(';')
          total_capacity += int(v[2])
          total_usage += float(v[6])
        median_usage = total_usage / qtd_interfaces
        database[filename][node_name] = {
          'capacity': total_capacity,
          'usage': median_usage
        }
  except Exception as e:
    print(e)
    print('Failed to read file: ' + filename)

main()