import mysql.connector

class SQL:

  def __init__(self, host: str, user: str, passwd: str, database: str) -> None:
    self.connection = mysql.connector.connect(
      host = host,
      user = user,
      passwd = passwd,
      database = database
    )
    self.cursor = self.connection.cursor()

  def create_table(self, table_name, items, primary_key):
    command = (
      'CREATE TABLE IF NOT EXISTS'
      + ' ' + table_name + ' ('
    )
    for item in items:
      command += item + ', '
    command += ', ' + primary_key + ')'
    print(command)
    self.__execute(command)

  def __execute(self, command):
    self.cursor.execute(command)

  def show_tables(self):
    pass

def main():
  sql = SQL(
    host = '0.0.0.0',
    user = 'peduardo',
    passwd = 'pe',
    database = 'kappacidade'
  )
  sql.create_table(
    table_name = 'xdsl',
    items = [
      'id INT AUTO_INCREMENT'
    ],
    primary_key = 'id'
  )

main()