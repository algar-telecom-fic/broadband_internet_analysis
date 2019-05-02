from datetime import date
from DatabaseConnector import DatabaseConnector

def read_anatel(filename=None):
    database = {}

    with open(filename, 'r', encoding='ISO-8859-1') as input_file:

        encountered_yet = False

        for line in input_file.readlines():
            attributes = line.split(';')
            nomePrestadora = attributes[0];

            if nomePrestadora == 'ALGAR TELECOM S/A':
                encountered_yet = True

                ddd          = attributes[2]
                prefixo      = attributes[3]
                faixaInicial = attributes[4]
                faixaFinal   = attributes[5]
                cidade       = attributes[8]

                if cidade not in database:
                    database[cidade] = (ddd,0,0) #(total recurso, total comum)

                diff = int(faixaFinal) - int(faixaInicial) + 1

                if prefixo == "4000" or prefixo == "4005":
                    t = (ddd, database[cidade][1] + diff, database[cidade][2])
                else:
                    t = (ddd, database[cidade][1] + diff, database[cidade][2] + diff)

                database[cidade] = t

            elif encountered_yet:
                break


    hoje = date.today()
    cidade_list = []
    for cidade in sorted(database):
        cidade_list.append((cidade,)+ database[cidade] + (hoje,))


    return cidade_list



def processAnatel(filename=None):
    data = read_anatel(filename)

    query = "INSERT INTO faixa_stfc(cidade, ddd, total_recurso, total_comum, dia) VALUES (%s, %s, %s, %s, %s)"

    db = DatabaseConnector()
    db.configureDB('dbconfigs.env')
    db.executaQuery(query, data)



if __name__ == '__main__':
    #filename = 'datasheets/faixa_minimizado.csv'
    filename = 'datasheets/FAIXA_STFC_20190406_2988_GERAL.txt'
    processAnatel(filename)
    print('finished processing')
