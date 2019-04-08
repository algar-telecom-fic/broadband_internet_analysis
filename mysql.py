import mysql.connector

class mySQL:

  def __init__(self, host: str, user: str, passwd: str, database: str) -> None:
    self.connection = mysql.connector.connect(
      host = host,
      user = user,
      passwd = passwd,
      database = database
    )
    self.cursor = self.connection.cursor()

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

  def show_tables(self) -> None:
    self.cursor.execute('SHOW TABLES')
    for i in self.cursor:
      print(i)

# db = mySQL(
#   host = '0.0.0.0',
#   user = 'username',
#   passwd = 'password',
#   database = 'database_name'
# )

# db.create_table(
#   table_name = 'xdsl',
#   items = [
#     'id INT AUTO_INCREMENT'
#   ],
#   primary_key = 'id'
# )

# sql.show_tables()