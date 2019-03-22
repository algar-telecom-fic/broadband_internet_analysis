import abc
from math import ceil
import datetime
import pymongo

class Technology(abc.ABC):
  database = {}

  @abc.abstractmethod
  def add_port(self):
    pass

  @abc.abstractmethod
  def build_mongodb(self):
    pass

class ADSL(Technology):

  def __init__(filename):
    try:
      with open(filename, 'r', encoding = 'ISO-8859-1') as input_file:
        technologies = [
          'huawei',
          'huawei ngn',
          'keymile',
          'keymile adsl',
          'zte',
        ]
        occupied = [
          'auditoria',
          'ocupado',
          'reservado ngn',
        ]
        available = [
          'disponivel',
          'disponivel ngn',
        ]
        for line in input_file.readlines():
          v = line.split(';')
          technology = str(v[18]).strip().lower()
          if technology in technologies:
            status = str(v[4]).strip()
            regional = str(v[5]).strip()
            locale = str(v[6]).strip()
            station = str(v[7]).strip()
            port = +1 if status in available else (-1 if status in occupied else 0)
            add_port(regional, locale, station, port)
    except Exception as e:
      print(e)
      print('Failed to read file: ' + filename)

  def add_port(self, regional, locale, station, port):
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
    if port > 0:
      self.database[regional][locale][station]['available'] += 1
    elif port < 0:
      self.database[regional][locale][station]['occupied'] += 1

  def build_mongodb(self, previous, diff):
    documents = []
    date = datetime.datetime.now()
    today = str(date.day) + '/' + str(date.month) + '/' + str(date.year)
    for regional in self.database:
      for locale in self.database[regional]:
        for station in self.database[regional][locale]:
          total = self.database[regional][locale][station]['total']
          available = self.database[regional][locale][station]['available']
          occupied = self.database[regional][locale][station]['occupied']
          try:
            occupied_before = previous.database[regional][locale][station]['occupied']
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
            error = 'Esgotado' if available == 0 else 'Sem histórico'
            increasing = error
            prediction = error
          documents.append({
            'Regional': i.regional,
            'Localidade': i.locale,
            'Estação mãe': ' '.join(i.station.split(' ')[:-1]),
            'Estação': i.station,
            'Total de portas': i.total,
            'Portas disponíveis': i.available,
            'Portas ocupadas': i.occupied,
            'Crescimento': increasing,
            'Previsão de esgotamento': prediction,
            'Data': today,
          })
    with pymongo.MongoClient() as client:
      database = client.capacidade
      collection = database.adsl_jaum_data
      collection.insert(documents)

def main():
  current_filepath, previous_filepath, date_difference = read_config_file('config.txt')
  current_file = ADSL(current_filepath)
  previous_file = ADSL(previous_filepath)
  current_file.build_mongodb(previous_file, date_difference)

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

main()