import abc
import datetime
import sys
sys.path.append('/home/gardusi/github/sql_library/')
from sql_json import mySQL

class XDSL(abc.ABC):
  date = datetime.datetime.now()

  @abc.abstractmethod
  def add_port(self):
    pass

  @abc.abstractmethod
  def build_documents(self):
    pass

  def insert_documents(
    self, 
    database_credentials, 
    database_name, 
    table_info,
    table_name,
  ):
    db = mySQL(
      database_credentials = database_credentials,
      database_name = database_name,
    )
    db.create_table(
      table_info = table_info,
      table_name = table_name,
    )
    self.db.insert_into(
      table_name = table_name,
      table_info = table_info,
      values = self.documents,
    )