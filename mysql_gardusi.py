import mysql.connector

class mySQL:

  # use 'database'
  def __init__(self, host: str, user: str, passwd: str, database: str) -> None:
    self.connection = mysql.connector.connect(
      host = host[0],
      user = user[0],
      passwd = passwd[0],
      database = database[0],
    )
    self.cursor = self.connection.cursor()

  # CREATE TABLE IF NOT EXISTS 'table_name' ('key_0' 'value_0', 'key_1' 'value_1', ..., )
  def create_table(self, table_name: str, table_info: dict, primary_key: str) -> None:
    command = (
      'CREATE TABLE IF NOT EXISTS'
      + ' ' + table_name + '('
    )
    for key, value in table_info.items():
      command += key + ' ' + value + ', '
    command += 'PRIMARY KEY' + '(' + primary_key[0] + '))'
    self.cursor.execute(command)

  # INSERT INTO 'table_name' ("keys") VALUES ("values_0"), ("values_1"), ... ;
  def insert_into(self, table_name: str, table_info: dict, values: list) -> None:
    eoq = table_info
    eoq.pop('id', None)
    command = (
      'INSERT INTO'
      + ' ' + table_name + ' ('
      + ', '.join(list(eoq.keys()))
      + ') ' + 'VALUES' + ' '
    )
    kappa = []
    for i in range(len(values)):
      keepo = []
      for key in list(table_info.keys()):
        if key in values[i]:
          keepo.append(values[i][key])
      keepo = ', '.join(keepo)
      print(keepo)
    print(command)