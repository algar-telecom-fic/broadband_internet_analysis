from CTO import CTO
from UI import UIManager
from Cidades import Cidades
from Database import Database
from datetime import datetime

class Main:

    def __init__(self):
        cidade_filename, dados_filename = UIManager().get_filenames()

        self.cidades = Cidades(cidade_filename)
        self.processaCSV(dados_filename)
        self.recuperaDados()
        self.insereDados()

    def processaCSV(self, filename):
        with open(filename, 'r', encoding='ISO-8859-1') as input_file:

            self.concessao = {}
            self.expansao  = {}
            for line in input_file.readlines():
                attributes = line.split(';')

                localidade = str(attributes[14])
                estacao    = str(attributes[15])
                cto        = str(attributes[1])
                status     = str(attributes[13])

                if localidade in self.cidades.concessao:
                    if cto in self.concessao:
                        self.concessao[cto].addLeitura(status)
                    else:
                        self.concessao[cto] = CTO(localidade, estacao, cto)
                        self.concessao[cto].addLeitura(status)

                elif localidade in self.cidades.expansao:
                    if cto in self.expansao:
                        self.expansao[cto].addLeitura(status)
                    else:
                        self.expansao[cto] = CTO(localidade, estacao, cto)
                        self.expansao[cto].addLeitura(status)


    def insereDados(self):
        hoje = datetime.utcnow()


        argsCn = []
        for nome, cto in self.concessao.items():
            nomeCto = cto.dict['CTO']
            try:
                antigoOcupado = self.antigoConcessao[nomeCto][8]
                antigoData    = self.antigoConcessao[nomeCto][1]

                ocupadoAtual  = int(cto.dict['OCUPADO'])
                vagoAtual = int(cto.dict['VAGO'])
                numDias = (hoje - self.antigoConcessao[nomeCto][1]).days

                taxa_crescimento = (ocupadoAtual - antigoOcupado) / numDias
                previsao = vagoAtual / taxa_crescimento
            except Exception as e:
                previsao = -1
            argsCn.append(
                (hoje,) + cto.as_a_tuple() + (previsao,)
            )

        argsEx = []
        for nome, cto in self.expansao.items():
            nomeCto = cto.dict['CTO']
            try:
                antigoOcupado = self.antigoExpansao[nomeCto][8]
                antigoData    = self.antigoExpansao[nomeCto][1]

                ocupadoAtual  = int(cto.dict['OCUPADO'])
                vagoAtual = int(cto.dict['VAGO'])
                numDias = (hoje - self.antigoExpansao[nomeCto][1]).days

                taxa_crescimento = (ocupadoAtual - antigoOcupado) / numDias
                previsao = vagoAtual / taxa_crescimento
            except Exception as e:
                previsao = -1
            argsEx.append(
                (hoje,) + cto.as_a_tuple() + (previsao,)
            )

        db = Database('dbconfigs.env')

        query = """INSERT INTO concessao (dia, local, estacao, cto, defeito, designado, reservado, ocupado, vago, total, previsao_esgotamento)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        db.executaQuery(query, argsCn)

        query = """INSERT INTO expansao (dia, local, estacao, cto, defeito, designado, reservado, ocupado, vago, total, previsao_esgotamento)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        db.executaQuery(query, argsEx)


    def recuperaDados(self):
        db = Database('dbconfigs.env')
        self.antigoConcessao = {}
        self.antigoExpansao = {}
        for registro in db.executaQuery('SELECT * from concessao where dia = (select Max(dia) from concessao)'):
            self.antigoConcessao[registro[4]] = registro

        for registro in db.executaQuery('SELECT * from expansao where dia = (select Max(dia) from expansao)'):
            self.antigoExpansao[registro[4]] = registro



if __name__ == '__main__':
    Main()
