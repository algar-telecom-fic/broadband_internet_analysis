import abc
import datetime
import sys
sys.path.append('/home/gardusi/github/broadband_internet_analysis/')
import mysql_gardusi

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

  def insert_documents(self, database, host, passwd, user, primary_key, table_info, table_name):
    db = mysql_gardusi.mySQL(
      database = database,
      host = host,
      passwd = passwd,
      user = user,
    )
    db.create_table(
      primary_key = primary_key,
      table_info = table_info,
      table_name = table_name,
    )