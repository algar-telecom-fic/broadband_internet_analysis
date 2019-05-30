import mysql.connector

class mySQL:

  # USE 'database';
  def __init__(self, database_credentials: dict, database_name: str) -> None:
    self.connection = mysql.connector.connect(
      host = database_credentials['ip'],
      user = database_credentials['username'],
      passwd = database_credentials['password'],
      database = database_name,
    )
    self.cursor = self.connection.cursor()

  # CREATE TABLE IF NOT EXISTS 'table_name' ('key_0' 'value_0', 'key_1' 'value_1', ...);
  def create_table(self, table_name: str, table_info: dict) -> None:
    command = (
      'CREATE TABLE IF NOT EXISTS'
      + ' ' + table_name + '('
      + ', '.join([('`' + key + '`' + ' ' + value) for key, value in table_info.items()])
      + ', ' + 'PRIMARY KEY (id)' + ')'
    )
    self.cursor.execute(command)

  # INSERT INTO 'table_name' ("keys") VALUES ("values_0"), ("values_1"), ... ;
  def insert_into(self, table_name: str, table_info: dict, values: list) -> None:
    columns = table_info
    columns.pop('id', None)
    documents = []
    for idx in range(len(values)):
      document = []
      for key in list(columns.keys()):
        document.append('\'' + str(values[idx][key]) + '\'')
      documents.append('(' + ', '.join(list(map(str, document))) + ')')
    command = (
      'INSERT INTO'
      + ' ' + table_name + ' ('
      + ', '.join([('`' + i + '`') for i in list(columns.keys())])
      + ') ' + 'VALUES' + ' ' + ', '.join(documents)
    )
    self.cursor.execute(command)