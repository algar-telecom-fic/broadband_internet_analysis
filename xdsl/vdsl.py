import math
import pymongo
import xdsl

class VDSL(xdsl.XDSL):
  database = {}
  available = [
    'disponivel ngn',
    'disponivel',
  ]
  table_info = {
    'available': 'INT',
    'cabinet': 'TINYTEXT',
    'date': 'DATETIME',
    'grand_station': 'TINYTEXT',
    'increasing': 'DOUBLE',
    'location': 'TINYTEXT',
    'occupied': 'INT',
    'prediction': 'TINYTEXT',
    'regional': 'TINYTEXT',
    'total': 'INT',
  }
  occupied = [
    'auditoria',
    'ocupado',
    'reservado ngn',
  ]
  table_name = 'vdsl'
  technologies = [
    'huawei vdsl',
    'keymile vdsl',
  ]

  def add_port(self, v):
    technology = str(v[18]).strip().lower()
    if technology not in self.technologies:
      return
    status = str(v[4]).strip()
    regional = str(v[5]).strip()
    locale = str(v[6]).strip()
    station = str(v[7]).strip()
    cabinet = self.get_cabinet(v)
    if regional not in self.database:
      self.database[regional] = {}
    if locale not in self.database[regional]:
      self.database[regional][locale] = {}
    if station not in self.database[regional][locale]:
      self.database[regional][locale][station] = {}
    if cabinet not in self.database[regional][locale][station]:
      self.database[regional][locale][station][cabinet] = {
        'available': 0,
        'occupied': 0,
        'total': 0,
      }
    self.database[regional][locale][station][cabinet]['total'] += 1
    if status in self.available:
      self.database[regional][locale][station][cabinet]['available'] += 1
    elif status in self.occupied:
      self.database[regional][locale][station][cabinet]['occupied'] += 1

  def build_documents(self, previous, date_difference):
    self.documents = []
    for regional in self.database:
      for locale in self.database[regional]:
        for station in self.database[regional][locale]:
          for cabinet in self.database[regional][locale][station]:
            available = self.database[regional][locale][station][cabinet]['available']
            occupied = self.database[regional][locale][station][cabinet]['occupied']
            total = self.database[regional][locale][station][cabinet]['total']
            try:
              occupied_before = previous.database[regional][locale][station][cabinet]['occupied']
              median = (occupied - occupied_before) / (date_difference / 30)
              increasing = round(median, 1)
              if available == 0:
                prediction = 'Esgotado'
              elif median > 0:
                value = ceil(available / median)
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
              increasing = 'Sem histórico'
              prediction = 'Esgotado' if i.available == 0 else 'Sem histórico'
            documents.append({
              'available': available,
              'cabinet': cabinet,
              'date': self.date,
              'grand_station': station,
              'increasing': increasing,
              'location': locale,
              'occupied': occupied,
              'prediction': prediction,
              'regional': regional,
              'total': total,
            })

  def get_cabinet(self, v):
    if len(v[ord('U') - ord('A')]) == 0:
      return v[ord('H') - ord('A')] + ' ARD RR'
    if v[ord('U') - ord('A')].find('ARD ') == -1:
      return v[ord('U') - ord('A')] + ' ARD ' + v[ord('V') - ord('A')]
    return v[ord('U') - ord('A')]