import configparser
import mysql.connector
import os

class Database:
    def __init__(self):
        folder = "/".join( os.path.realpath(__file__).split('/')[:-1] )
        self.configureDB( folder + '/dbconfigs.env' )


    def configureDB(self, configFilename):
        self.config = configparser.ConfigParser()
        self.config.read(configFilename)
        self.config = self.config['DB']

    def executaQuery(self, query, args=[]):
        self.conectaBancodeDados()
        cursor = self.conn.cursor()
        if args == []:
            cursor.execute(query)
        else:
            cursor.executemany(query, args)

        try:
            results = cursor.fetchall()
            return results
        except:
            pass

        self.conn.commit()

    def conectaBancodeDados(self):
        self.conn = mysql.connector.connect(host     = self.config['DB_HOST'],
                                            database = self.config['DB_NAME'],
                                            user     = self.config['DB_USER'],
                                            password = self.config['DB_PSWD']
                                            )
