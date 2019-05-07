from datetime import date
from DatabaseConnector import DatabaseConnector
from mydict import InfiniteDict


def read_vantive(filename=None):
    database = InfiniteDict()
    possible_status = set()

    with open(filename, 'r', encoding='ISO-8859-1') as input_file:
        next(input_file)

        for line in input_file.readlines():
            attributes = line.strip().split(';')
            quantidade, areaLocal, localidade, status, tecnologia = attributes

            possible_status.add(status)

            database[areaLocal][localidade][tecnologia][status] = database[areaLocal][localidade][tecnologia].get(status, 0) + int(quantidade)

    possible_status = sorted(possible_status)

    hoje = date.today()

    lista_vantive = []
    for areaLocal, dados in database.items():
        for localidade, dados in dados.items():
            for tecnologia in dados:
                data = [areaLocal, localidade, tecnologia]
                for status in possible_status:
                    data.append( database[areaLocal][localidade][tecnologia].get(status, 0) )
                data.append(hoje)
                lista_vantive.append(tuple(data))

    return (possible_status, lista_vantive)
    

def processVantive(filename=None, dbcofigfile=None):
    possible_status, data = read_vantive(filename);

    query = (
        'INSERT INTO area_local(areaLocal, cidade, tecnologia, ' + \
        ', '.join( [(f"`{i}`") for i in possible_status]) + \
        ', dia)' + 'VALUES (' + \
        ', '.join(["%s" for i in range(0, len(possible_status)+4)]) + ')'
    )

    db = DatabaseConnector()
    db.configureDB(dbconfigfile)
    db.executaQuery(query, data)

def testaVantive(filename):
    status, data = read_vantive(filename)
    print(status)
    for d in data:
        print(d)

if __name__ == '__main__':
    filename = 'datasheets/Relatorio_Area_Local09042019080046.csv'
    dbconfigfile = 'dbconfigs.env'
    processVantive(filename, dbconfigfile)
    #testaVantive(filename)
