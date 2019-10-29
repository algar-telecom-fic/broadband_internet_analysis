from datetime import date
from DatabaseConnector import DatabaseConnector
from collections import defaultdict

def read_anatel(filename=None):
    recurso_total = defaultdict(int)
    recurso_comum = defaultdict(int)
    ddd = {}

    with open(filename, 'r', encoding='ISO-8859-1') as input_file:

        encountered_yet = False

        for line in input_file.readlines():
            attributes = line.split(';')
            nomePrestadora = attributes[0];

            if nomePrestadora == 'ALGAR TELECOM S/A':
                encountered_yet = True

                atual_ddd, prefixo, faixaInicial, faixaFinal, _, _, cidade = attributes[2:9]

                ddd[cidade] = atual_ddd

                diff = int(faixaFinal) - int(faixaInicial) + 1
                recurso_total[cidade]+=diff

                if prefixo != "4000" and prefixo != "4005":
                    recurso_comum[cidade]+=diff

            elif encountered_yet:
                break


    hoje = date.today()
    data_list = []
    for cidade in sorted(recurso_total):
        data_list.append(
            (
                cidade,
                ddd[cidade],
                recurso_total[cidade],
                recurso_comum[cidade],
                hoje,
            )
        )


    return data_list



def processAnatel(filename=None, dbconfigfile='/home/pediogo/broadband_internet_analysis/voz_fixa/area_local/dbconfigs.env'):
    if filename == None:
        return


    data = read_anatel(filename)

    query = "INSERT INTO faixa_stfc(cidade, ddd, total_recurso, total_comum, dia) VALUES (%s, %s, %s, %s, %s)"

    db = DatabaseConnector()
    db.configureDB(dbconfigfile)
    db.executaQuery(query, data)



def testaAnatel(filename):
    print('testouAnatel')
    if filename == '' or filename == None:
        return
    lista = read_anatel(filename)
    for item in lista:
        print(item)


if __name__ == '__main__':
    #filename = 'datasheets/faixa_minimizado.csv'
    filename = 'datasheets/FAIXA_STFC_20190406_2988_GERAL.txt'
    processAnatel(filename)
    #testaAnatel(filename)
    print('finished processing')
