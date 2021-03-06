import adsl
import os
import json
import vdsl

def main(date_difference=0):
  filepath = os.path.dirname(os.path.abspath(__file__)) + '/'
  config = read_json(filepath + 'config.json')
  if date_difference!=0:
      config['date_difference'] = date_difference
  current_adsl, current_vdsl = read_file(config['current_filepath'])
  previous_adsl, previous_vdsl = read_file(config['previous_filepath'])
  current_adsl.build_documents(previous_adsl, config['date_difference'])
  current_vdsl.build_documents(previous_vdsl, config['date_difference'])
  database_credentials = read_json(config['database_credentials_filepath'])
  current_adsl.insert_documents(
    database_credentials = database_credentials,
    database_name = config['database_name'],
    table_info = read_json(filepath + 'adsl_table_info.json'),
    table_name = config['adsl_table_name'],
  )
  current_vdsl.insert_documents(
    database_credentials = database_credentials,
    database_name = config['database_name'],
    table_info = read_json(filepath + 'vdsl_table_info.json'),
    table_name = config['vdsl_table_name'],
  )

def read_file(filepath):
  technologies = (adsl.ADSL(), vdsl.VDSL())
  with open(filepath, 'r', encoding = 'ISO-8859-1') as input_file:
    for line in input_file.readlines():
      v = line.split(';')
      for technology in technologies:
        technology.add_port(v)
  return technologies

def read_json(filepath):
  with open(filepath, 'rb') as file:
    return json.load(file, encoding = 'utf-8')

if __name__ == "__main__":
    main()
