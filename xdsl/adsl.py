import math
import pymongo
import xdsl

import sys
sys.path.append('/home/gardusi/github/broadband_internet_analysis/')
import mysql_gardusi

class ADSL(xdsl.XDSL):
  database = {}
  available = [
    'disponivel ngn',
    'disponivel',
  ]
  mysql_table_info = {
    'available': 'INT',
    'date': 'DATETIME',
    'grand_station': 'TINYTEXT',
    'id': 'INT AUTO_INCREMENT',
    'increasing': 'DOUBLE',
    'location': 'TINYTEXT',
    'occupied': 'INT',
    'prediction': 'TINYTEXT',
    'regional': 'TINYTEXT',
    'station': 'TINYTEXT',
    'total': 'INT',
  }
  occupied = [
    'auditoria',
    'ocupado',
    'reservado ngn',
  ]
  technologies = [
    'huawei ngn',
    'huawei',
    'keymile adsl',
    'keymile',
    'zte',
  ]

  def start_db(self):
    db = mysql_gardusi.mySQL(
      host = '0.0.0.0',
      user = 'peduardo',
      passwd = 'pe',
      database = 'kappacidade'
    )
    db.create_table(
      table_name = 'adsl',
      items = self.table_info,
      primary_key = 'id'
    )
    db.show_tables()

  def add_port(self, v):
    technology = str(v[18]).strip().lower()
    if technology not in self.technologies:
      return
    status = str(v[4]).strip()
    regional = str(v[5]).strip()
    locale = str(v[6]).strip()
    station = str(v[7]).strip()
    if regional not in self.database:
      self.database[regional] = {}
    if locale not in self.database[regional]:
      self.database[regional][locale] = {}
    if station not in self.database[regional][locale]:
      self.database[regional][locale][station] = {
        'available': 0,
        'occupied': 0,
        'total': 0,
      }
    self.database[regional][locale][station]['total'] += 1
    if status in self.available:
      self.database[regional][locale][station]['available'] += 1
    elif status in self.occupied:
      self.database[regional][locale][station]['occupied'] += 1

  def build_mongodb(self, previous, date_difference):
    documents = []
    for regional in self.database:
      for locale in self.database[regional]:
        for station in self.database[regional][locale]:
          available = self.database[regional][locale][station]['available']
          occupied = self.database[regional][locale][station]['occupied']
          total = self.database[regional][locale][station]['total']
          try:
            occupied_before = previous.database[regional][locale][station]['occupied']
            median = (occupied - occupied_before) / (date_difference / 30)
            increasing = round(median, 1)
            if available == 0:
              prediction = 'Esgotado'
            elif median > 0:
              value = math.ceil(available / median)
              if value == 1:
                prediction = 'Esgota em até 1 mês'
              elif value > 10:
                prediction = 'Esgota em mais de 10 meses'
              else:
                prediction = 'Esgota em até ' + str(value) + ' meses'
            elif median < 0:
              prediction = 'Decrescimento'
            else:
              prediction = 'Estável'
          except Exception as e:
            print(e)
            error = 'Esgotado' if available == 0 else 'Sem histórico'
            increasing = error
            prediction = error
          documents.append({
            'Crescimento': increasing,
            'Data': self.date,
            'Estação mãe': ' '.join(station.split(' ')[: -1]),
            'Estação': station,
            'Localidade': locale,
            'Portas disponíveis': available,
            'Portas ocupadas': occupied,
            'Previsão de esgotamento': prediction,
            'Regional': regional,
            'Total de portas': total,
          })
    with pymongo.MongoClient() as client:
      database = client['capacidade']
      collection = database['adsl']
      collection.insert(documents)