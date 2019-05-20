import adsl
import os
import vdsl

def main():
  filepath = os.path.dirname(os.path.abspath(__file__)) + '/'
  config = read_json(filepath + 'config.txt')
  current_adsl, current_vdsl = read_file(config['current_filepath'])
  previous_adsl, previous_vdsl = read_file(config['previous_filepath'])
  current_adsl.build_documents(previous_adsl, config['date_difference'])
  current_vdsl.build_documents(previous_vdsl, config['date_difference'])
  current_adsl.insert_documents()
  current_vdsl.insert_documents()

def read_file(filepath):
  technologies = (adsl.ADSL(), vdsl.VDSL())
  with open(filepath, 'r', encoding = 'ISO-8859-1') as input_file:
    for line in input_file.readlines():
      v = line.split(';')
      for technology in technologies:
        technology.add_port(v)
  return technologies

def read_json(self, filepath):
  with open(filepath, 'rb') as file:
    return json.load(file, encoding = 'utf-8')

main()