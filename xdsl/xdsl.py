import abc
import datetime

class XDSL(abc.ABC):
  database = 'kappacidade'
  date = datetime.datetime.utcnow(),
  host = '0.0.0.0',
  passwd = 'pe',
  user = 'peduardo',

  @abc.abstractmethod
  def add_port(self):
    pass

  @abc.abstractmethod
  def build_documents(self):
    pass

  def insert_documents(self):
    with mysql_gardusi.mySQL(
      database = self.database,
      host = self.host,
      passwd = self.passwd,
      user = self.user,
    ) as db:
      db.create_table(
        primary_key = 'id',
        table_info = self.table_info,
        table_name = self.table_name,
      )