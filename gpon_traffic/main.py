import datetime
import os
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

  def read_ports(self):
    with open(self.filepath_ports, 'r', encoding = 'ISO-8859-1') as input_file:
      for line in input_file.readlines():
        v = line.split(';')
        ip = v[ord('Z') - ord('A')].strip()
        status = v[ord('P') - ord('A')].strip()
        print(v)
        print(ip)
        print(status)
        if ip not in self.database:
          self.database[ip] = {
            'ANEL METRO': '?',
            'Capacidade_': '?',
            'Estação': v[ord('R') - ord('A')].strip(),
            'IP OLT': ip,
            'Localidade': v[ord('Q') - ord('A')].strip(),
            'Modelo': v[ord('U') - ord('A')].strip(),
            'OLT': v[ord('X') - ord('A')].strip(),
            'Portas Livres': 0,
            'Portas Ocupdas': 0,
            'Total Instalado': 0,
            'Utilização 12/11': '?',
            'Utilização': '?',
            'VLAN': v[1 + ord('Z') - ord('A')].strip(),
          }
        self.database[ip]['Total Instalado'] += 1
        if status in self.convert_status:
          self.database[ip][convert_status[status]] += 1

def main():
  gpon = GPON(os.path.dirname(os.path.abspath(__file__)) + '/' + 'config.txt')
  gpon.read_ports()
  for i in gpon.database:
    print(i)

main()