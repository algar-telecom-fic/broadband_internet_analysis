import datetime
import pymongo
from math import ceil

class data:
  def __init__(self, regional, locale, station, total, available, occupied):
    self.regional = regional
    self.locale = locale
    self.station = station
    self.total = total
    self.available = available
    self.occupied = occupied
  def __lt__(self, other):
    if self.available != other.available:
      return self.available < other.available
    if self.regional != other.regional:
      return self.regional < other.regional
    if self.locale != other.locale:
      return self.locale < other.locale
    return self.station < other.station
  def __str__(self):
    return str(self.regional) + str(self.locale) + str(self.station) + str(self.self.total) + str(self.available) + str(self.occupied)

def add_port(filename, regional, locale, station, port):
  global database
  if regional not in database[filename]:
    database[filename][regional] = {}
  if locale not in database[filename][regional]:
    database[filename][regional][locale] = {}
  if station not in database[filename][regional][locale]:
    database[filename][regional][locale][station] = {
      'total': 0,
      'available': 0,
      'occupied': 0,
    }
  database[filename][regional][locale][station]['total'] += 1
  if port > 0:
    database[filename][regional][locale][station]['available'] += 1
  elif port < 0:
    database[filename][regional][locale][station]['occupied'] += 1

def build_database(current_file):
  global database
  v = []
  for regional in database[current_file]:
    for locale in database[current_file][regional]:
      for station in database[current_file][regional][locale]:
        v.append(
          data(
            regional,
            locale,
            station,
            database[current_file][regional][locale][station]['total'],
            database[current_file][regional][locale][station]['available'],
            database[current_file][regional][locale][station]['occupied'],
          )
        )
  v.sort()
  database[current_file] = v

def build_mongodb(current_file, previous_file, date_difference):
  global database
  documents = []
  date = datetime.datetime.now()
  today = str(date.day) + '/' + str(date.month) + '/' + str(date.year)
  for i in database[current_file]:
    try:
      before = database[previous_file][i.regional][i.locale][i.station]['occupied']
      median = (i.occupied - before) / (date_difference / 30)
      increasing = round(median, 1)
      if i.available == 0:
        prediction = 'Esgotado'
      elif median > 0:
        value = ceil(i.available / median)
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
      increasing = 'Esgotado' if i.available == 0 else 'Sem histórico'
      prediction = 'Esgotado' if i.available == 0 else 'Sem histórico'
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
  current_file, previous_file, date_difference = read_config_file('config.txt')
  read_file(current_file)
  read_file(previous_file)
  build_database(current_file)
  build_mongodb(current_file, previous_file, date_difference)

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
          add_port(filename, regional, locale, station, port)
  except Exception as e:
    print(e)
    print('Failed to read file: ' + filename)

main()