import abc
import datetime
import math
import os
import pymongo

class Technology(abc.ABC):
  database = {}
  date = datetime.datetime.utcnow()
  today = str(date.day) + '/' + str(date.month) + '/' + str(date.year)

  @abc.abstractmethod
  def add_port(self):
    pass

  @abc.abstractmethod
  def build_mongodb(self):
    pass

class ADSL(Technology):
  available = [
    'disponivel',
    'disponivel ngn',
  ]
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
        'total': 0,
        'available': 0,
        'occupied': 0,
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
            'Data': self.today,
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
      collection = database['xdsl_adsl']
      collection.insert(documents)

class VDSL(Technology):
  available = [
    'disponivel',
    'disponivel ngn',
  ]
  occupied = [
    'auditoria',
    'ocupado',
    'reservado ngn',
  ]
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

  def build_mongodb(self, previous, date_difference):
    documents = []
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
              'Armário': i.cabinet,
              'Crescimento': increasing,
              'Data': self.today,
              'Estação mãe': i.station,
              'Localidade': i.locale,
              'Portas disponíveis': i.available,
              'Portas ocupadas': i.occupied,
              'Previsão de esgotamento': prediction,
              'Regional': i.regional,
              'Total de portas': i.total,
            })
    with pymongo.MongoClient() as client:
      database = client.capacidade
      collection = database.vdsl
      collection.insert(documents)

  def get_cabinet(self, v):
    if len(v[ord('U') - ord('A')]) == 0:
      return v[ord('H') - ord('A')] + ' ARD RR'
    if v[ord('U') - ord('A')].find('ARD ') == -1:
      return v[ord('U') - ord('A')] + ' ARD ' + v[ord('V') - ord('A')]
    return v[ord('U') - ord('A')]

def main():
  filepath = os.path.dirname(os.path.abspath(__file__))
  current_filepath, previous_filepath, date_difference = read_config_file(filepath + '/config.txt')
  current_adsl, current_vdsl = read_file(current_filepath)
  previous_adsl, previous_vdsl = read_file(previous_filepath)
  current_adsl.build_mongodb(previous_adsl, date_difference)
  current_vdsl.build_mongodb(previous_vdsl, date_difference)

def read_config_file(filepath):
  with open(filepath, 'r', encoding = 'ISO-8859-1') as config_file:
    v = config_file.readlines()
    current_file = v[0].split('=')[1].strip().split('"')[1].strip()
    previous_file = v[1].split('=')[1].strip().split('"')[1].strip()
    date_difference = int(v[2].split('=')[1].strip().split('"')[1].strip())
    return (current_file, previous_file, date_difference)

def read_file(filepath):
  technologies = (ADSL(), VDSL())
  for i in technologies:
    print(i)
  # technologies = (ADSL())
  # technologies = (VDSL())
  # with open(filepath, 'r', encoding = 'ISO-8859-1') as input_file:
  #   for line in input_file.readlines():
  #     v = line.split(';')
  #     print(v)
  #     for technology in technologies:
  #       technology.add_port(v)

main()