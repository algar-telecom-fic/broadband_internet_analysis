import datetime
import json
import os
import re
import sys
sys.path.append('/home/gardusi/github/sql_library/')
from sql_json import mySQL

class GPON:
  convert_status = {
    'OCUPADO': 'Portas Ocupdas',
    'VAGO': 'Portas Livres',
  }
  database = {}
  date = datetime.datetime.now()
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
    '172.30.10.64': 1,
    '172.17.18.129': 1,
    '172.24.6.135': 2,
  }

  def __init__(self):
    filepath = os.path.realpath(
      os.path.join(os.getcwd(), os.path.dirname(__file__))
    )
    filepath += '/' + 'config.json'
    print(filepath)
    with open(filepath, 'r', encoding = 'ISO-8859-1') as config_file:
      self.config = json.load(config_file)
    print(self.config)

  def build_documents(self):
    self.documents = []
    for ip in self.database:
      if ip in self.ip_exceptions:
        self.database[ip]['Capacidade'] = self.ip_exceptions[ip]
      self.database[ip]['__qtd__'] = max(1, self.database[ip]['__qtd__'])
      self.database[ip]['Utilização'] = self.database[ip]['__sum__'] / self.database[ip]['__qtd__']
      self.database[ip]['Utilização gbps'] = (self.database[ip]['Utilização'] * self.database[ip]['Capacidade']) / 100.0
      self.database[ip].pop('__sum__', None)
      self.database[ip].pop('__qtd__', None)
      valid = True
      for key in self.table_info.keys():
        if key != 'id' and key not in self.database[ip]:
          valid = False
      if valid == True:
        self.documents.append(self.database[ip])

  def get_ip(self, s):
    try:
      return re.findall(r'[0-9]+(?:\.[0-9]+){3}', s)[0]
    except Exception:
      return None

  def insert_documents(self):
    db = mySQL(
      filepath = self.config[database_filepath],
      database_name = 'kappacidade',
    )
    db.create_table(
      table_info = self.table_info,
      table_name = 'gpon_traffic',
    )
    db.insert_into(
      self.table_name,
      self.table_info,
      self.documents,
    )

  def read_traffic(self):
    with open(self.filepath_current, 'r', encoding = 'ISO-8859-1') as input_file:
      for line in input_file.readlines():
        v = line.split(';')
        ip = self.get_ip(v[ord('G') - ord('A')])
        if ip in self.database:
          self.database[ip]['Switch'] = v[ord('E') - ord('A')]
          self.database[ip]['Capacidade'] += float(v[ord('H') - ord('A')].strip())
          value = float(v[ord('I') - ord('A')].strip())
          if value > 0:
            self.database[ip]['__sum__'] += value
            self.database[ip]['__qtd__'] += 1

  def read_ports(self):
    with open(self.filepath_ports, 'r', encoding = 'ISO-8859-1') as input_file:
      for line in input_file.readlines():
        v = line.split(';')
        ip = v[ord('X') - ord('A')].strip()
        status = v[ord('N') - ord('A')].strip()
        if ip not in self.database:
          self.database[ip] = {
            'ANEL METRO': '?',
            'Capacidade Anel': '?',
            'Utilização Anel': '?',
            'Capacidade': 0,
            'Data': self.date,
            'Estação': v[ord('P') - ord('A')].strip(),
            'IP OLT': ip,
            'Localidade': v[ord('O') - ord('A')].strip(),
            'Modelo': v[ord('S') - ord('A')].strip(),
            'OLT': v[ord('V') - ord('A')].strip(),
            'Portas Livres': 0,
            'Portas Ocupdas': 0,
            'Total Instalado': 0,
            'VLAN': v[ord('Y') - ord('A')].strip(),
            '__sum__': 0,
            '__qtd__': 0,
          }
        self.database[ip]['Total Instalado'] += 1
        if status in self.convert_status:
          self.database[ip][self.convert_status[status]] += 1