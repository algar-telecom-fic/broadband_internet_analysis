import datetime
import os
import re
import sys
sys.path.append('/home/gardusi/github/sql_library/')
import mysql_json

class GPON:
  convert_status = {
    'OCUPADO': 'Portas Ocupdas',
    'VAGO': 'Portas Livres',
  }
  database = {}
  ip_exceptions = {
    '172.30.16.49': 10,
    '172.30.20.93': 2,
    '172.30.20.187': 2,
    '172.24.6.135': 2,
    '172.17.16.1': 2,
    '172.24.29.50': 2,
    '172.30.20.132': 2,
    '172.17.18.2': 1,
    '172.17.18.209': 1,
    '172.17.12.1': 2,
    '172.24.158.146': 2,
    '172.17.10.3': 2,
    '172.17.22.6': 2,
    '172.30.13.125': 2,
    '172.30.10.64': 1,
    '172.17.18.129': 1,
    '172.24.6.135': 2,
  }
  database_name = 'kappacidade'
  date = datetime.datetime.now()
  host = '0.0.0.0'
  passwd = 'pe'
  primary_key = 'id'
  user = 'peduardo'
  table_name = 'gpon_traffic'
  table_info = {
    'id': 'INT AUTO_INCREMENT',
    'ANEL METRO_': 'TINYTEXT',
    'Capacidade': 'INT',
    'Capacidade_': 'TINYTEXT',
    'Data': 'DATETIME',
    'Estação': 'TINYTEXT',
    'IP OLT': 'TINYTEXT',
    'Localidade': 'TINYTEXT',
    'Modelo': 'TINYTEXT',
    'OLT': 'TINYTEXT',
    'Portas Livres': 'INT',
    'Portas Ocupdas': 'INT',
    'Total Instalado': 'INT',
    'Utilização 12/11': 'TINYTEXT',
    'Utilização': 'DOUBLE',
    'Utilização_': 'TINYTEXT',
    'VLAN': 'TINYTEXT',
    'Switch': 'TINYTEXT',
    'Utilização passada': 'DOUBLE',
    'Utilização gbps': 'DOUBLE',
    'Crescimento MB / mês': 'DOUBLE',
    'Esgotamento dias': 'DOUBLE',
    'Esgotamento': 'DATETIME',
  }

  def __init__(self, filepath):
    with open(filepath, 'r', encoding = 'ISO-8859-1') as config_file:
      v = config_file.readlines()
      self.filepath_ports = v[0].split('=')[1].strip().split('"')[1].strip()
      self.filepath_current = v[1].split('=')[1].strip().split('"')[1].strip()
      self.filepath_previous = v[2].split('=')[1].strip().split('"')[1].strip()
      self.date_difference = v[3].split('=')[1].strip().split('"')[1].strip()

  def build_documents(self):
    self.documents = []
    for i in self.database:
      self.database[i]['Utilização gbps'] = self.database[i]['Utilização'] * self.database[i]['Capacidade']
      self.database[i]['Crescimento MB / mês'] = (self.database[i]['Utilização gbps'] - self.database[i]['Utilização gbps']) / float(self.date_difference)
      self.database[i]['Esgotamento dias'] = max(0, (self.database[i]['Capacidade'] - self.database[i]['Utilização gbps']) / max(1, self.database[i]['Crescimento MB / mês']))
      self.database[i]['Esgotamento'] = self.date + datetime.timedelta(days = self.database[i]['Esgotamento dias'])
      if i in self.ip_exceptions:
        self.database[i]['Capacidade'] = self.ip_exceptions[i]
      self.documents.append(self.database[i])

  def get_ip(self, s):
    try:
      return re.findall(r'[0-9]+(?:\.[0-9]+){3}', s)[0]
    except Exception:
      return None

  def insert_documents(self):
    db = mysql_json.mySQL(
      database = self.database_name,
      host = self.host,
      passwd = self.passwd,
      user = self.user,
    )
    db.create_table(
      primary_key = self.primary_key,
      table_info = self.table_info,
      table_name = self.table_name,
    )
    db.insert_into(
      self.table_name,
      self.table_info,
      self.documents,
    )

  def read_current_traffic(self):
    with open(self.filepath_current, 'r', encoding = 'ISO-8859-1') as input_file:
      for line in input_file.readlines():
        v = line.split(';')
        ip = self.get_ip(v[ord('G') - ord('A')])
        if ip in self.database:
          self.database[ip]['Capacidade'] += float(v[ord('H') - ord('A')].strip())
          self.database[ip]['Utilização'] += float(v[ord('I') - ord('A')].strip())
          self.database[ip]['Switch'] = v[ord('E') - ord('A')]

  def read_previous_traffic(self):
    with open(self.filepath_previous, 'r', encoding = 'ISO-8859-1') as input_file:
      for line in input_file.readlines():
        v = line.split(';')
        ip = self.get_ip(v[ord('G') - ord('A')])
        if ip in self.database:
          self.database[ip]['Utilização passada'] = float(v[ord('I') - ord('A')])

  def read_traffic(self):
    self.read_current_traffic()
    self.read_previous_traffic()

  def read_ports(self):
    with open(self.filepath_ports, 'r', encoding = 'ISO-8859-1') as input_file:
      for line in input_file.readlines():
        v = line.split(';')
        ip = v[ord('X') - ord('A')].strip()
        status = v[ord('N') - ord('A')].strip()
        if ip not in self.database:
          self.database[ip] = {
            'ANEL METRO_': '?',
            'Capacidade': 0,
            'Capacidade_': '?',
            'Data': self.date,
            'Estação': v[ord('P') - ord('A')].strip(),
            'IP OLT': ip,
            'Localidade': v[ord('O') - ord('A')].strip(),
            'Modelo': v[ord('S') - ord('A')].strip(),
            'OLT': v[ord('V') - ord('A')].strip(),
            'Portas Livres': 0,
            'Portas Ocupdas': 0,
            'Total Instalado': 0,
            'Utilização 12/11': '?',
            'Utilização': 0,
            'Utilização_': '?',
            'VLAN': v[ord('Y') - ord('A')].strip(),
          }
        self.database[ip]['Total Instalado'] += 1
        if status in self.convert_status:
          self.database[ip][self.convert_status[status]] += 1

def main():
  gpon = GPON(os.path.dirname(os.path.abspath(__file__)) + '/' + 'config.txt')
  gpon.read_ports()
  gpon.read_traffic()
  gpon.build_documents()
  gpon.insert_documents()

main()