import mysql.connector

class mySQL:

  # use 'database'
  def __init__(self, host: str, user: str, passwd: str, database: str) -> None:
    self.connection = mysql.connector.connect(
      host = host,
      user = user,
      passwd = passwd,
      database = database
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
    command += 'PRIMARY KEY' + '(' + primary_key + '))'
    print(command)
    self.cursor.execute(command)

  # INSERT INTO 'table_name' ("keys") VALUES ("values_0"), ("values_1"), ... ;
  def insert(self, table_name: str, table_info: dict, values: list) -> None:
    command = (
      'INSERT INTO'
      + ' ' + table_name + ' ('
      + ', '.join(list(table_info.keys()))
      + ') ' + 'VALUES' + ' '
    )
    print(command)