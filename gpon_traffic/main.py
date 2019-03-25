import datetime
import os
import re
import pymongo

class GPON:
  convert_status = {
    'OCUPADO': 'Portas Ocupdas',
    'VAGO': 'Portas Livres',
  }
  database = {}
  date = datetime.datetime.utcnow()

  def __init__(self, filepath):
    with open(filepath, 'r', encoding = 'ISO-8859-1') as config_file:
      v = config_file.readlines()
      self.filepath_ports = v[0].split('=')[1].strip().split('"')[1].strip()
      self.filepath_current = v[1].split('=')[1].strip().split('"')[1].strip()
      self.filepath_previous = v[2].split('=')[1].strip().split('"')[1].strip()
      self.date_difference = v[3].split('=')[1].strip().split('"')[1].strip()

  def get_ip(self, s):
    return re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', s)

  def read_current_traffic(self):
    with open(self.filepath_current, 'r', encoding = 'ISO-8859-1') as input_file:
      for line in input_file.readlines():
        v = line.split(';')
        ip = self.get_ip(v[ord('G') - ord('A')])
        if ip == None:
          continue
        print(v)
        print(ip)
        self.database[ip]['Capacidade'] += int(v[ord('H') - ord('A')].strip())
        self.database[ip]['sum'] += float(v[ord('I') - ord('A')])
        self.database[ip]['qtd'] += 1
        self.database[ip]['Switch'] = v[ord('E') - ord('A')]

  def read_previous_traffic(self):
    with open(self.filepath_current, 'r', encoding = 'ISO-8859-1') as input_file:
      for line in input_file.readlines():
        v = line.split(';')
        ip = self.get_ip(v[ord('G') - ord('A')])
        self.database[ip]['Utilização passada'] = int(v[ord('H') - ord('A')])

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
            'Estação': v[ord('P') - ord('A')].strip(),
            'IP OLT': ip,
            'Localidade': v[ord('O') - ord('A')].strip(),
            'Modelo': v[ord('S') - ord('A')].strip(),
            'OLT': v[ord('V') - ord('A')].strip(),
            'Portas Livres': 0,
            'Portas Ocupdas': 0,
            'qtd': 0,
            'sum': 0,
            'Total Instalado': 0,
            'Utilização 12/11': '?',
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
  for i in gpon.database:
    print(gpon.database[i])

main()