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
  filepath = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
  )

  def __init__(self):
    self.capacity_exceptions = self.read_json(
      self.filepath + '/' + 'capacity_exceptions.json'
    )
    self.config = self.read_json(
      self.filepath + '/' + 'config.json'
    )
    self.ring_info = self.read_json(
      self.filepath + '/' + 'ring_info.json'
    )
    self.table_info = self.read_json(
      self.filepath + '/' + 'table_info.json'
    )
    self.database_credentials = self.read_json(
      self.config['database_credentials_filepath']
    )
    self.db = mySQL(
      database_credentials = self.database_credentials,
      database_name = self.config['database_name'],
    )

  def build_documents(self):
    self.documents = []
    for ip in self.database:
      if ip in self.capacity_exceptions:
        self.database[ip]['Capacidade'] = self.capacity_exceptions[ip]
      if ip in self.ring_info:
        self.database[ip]['ANEL METRO'] = self.ring_info[ip]
      self.database[ip]['__qtd__'] = max(1, self.database[ip]['__qtd__'])
      self.database[ip]['Utilização'] = (
        self.database[ip]['__sum__'] / self.database[ip]['__qtd__']
      )
      self.database[ip]['Utilização gbps'] = (
        self.database[ip]['Utilização'] * self.database[ip]['Capacidade']
      ) / 100.0
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
    self.db.create_table(
      table_info = self.table_info,
      table_name = self.config['table_name'],
    )
    self.db.insert_into(
      table_name = self.config['table_name'],
      table_info = self.table_info,
      values = self.documents,
    )

  def read_json(self, filepath):
    with open(filepath, 'rb') as file:
      return json.load(file, encoding = 'utf-8')

  def read_traffic(self):
    with open(
      self.config['current_filepath'], 'r', encoding = 'latin-1'
    ) as input_file:
      for line in input_file.readlines():
        v = line.split(';')
        ip = self.get_ip(v[ord('G') - ord('A')])
        if ip in self.database:
          self.database[ip]['Switch'] = v[ord('E') - ord('A')]
          self.database[ip]['Capacidade'] += float(
            v[ord('H') - ord('A')].strip()
          )
          value = float(v[ord('I') - ord('A')].strip())
          if value > 0:
            self.database[ip]['__sum__'] += value
            self.database[ip]['__qtd__'] += 1

  def read_ports(self):
    with open(
      self.config['ports_filepath'], 'r', encoding = 'latin-1'
    ) as input_file:
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