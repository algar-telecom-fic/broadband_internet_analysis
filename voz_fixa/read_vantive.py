from datetime import date

def read_vantive(filename=None):

    database = {}
    possible_status = []
    with open(filename, 'r', encoding='ISO-8859-1') as input_file:
        next(input_file)

        for line in input_file.readlines():
            attributes = line.strip().split(';')

            quantidade = attributes[0];
            areaLocal  = attributes[1];
            localidade = attributes[2];
            status     = attributes[3];
            tecnologia = attributes[4];

            if status not in possible_status:
                possible_status.append(status)

            if localidade not in database:
                database[localidade] = {'area local' : areaLocal}

            if tecnologia not in database[localidade]:
                database[localidade][tecnologia] = {}

            if status not in database[localidade][tecnologia]:
                database[localidade][tecnologia][status] = 0

            database[localidade][tecnologia][status]+=int(quantidade)

    possible_status.sort()
    print(possible_status)

    hoje = date.today()

    lista_vantive = []

    for cidade in sorted(database):
        for tecnologia in database[cidade]:
            if tecnologia == 'area local': continue

            item = [cidade, database[cidade]['area local'], tecnologia]

            for status in possible_status:
                if status not in database[cidade][tecnologia]:
                    item.append(0)
                else:
                    item.append(database[cidade][tecnologia][status])

            item.append(hoje)

            lista_vantive.append(tuple(item))

    return lista_vantive


if __name__ == '__main__':
    filename = 'datasheets/Relatorio_Area_Local09042019080046.csv'
    #filename = 'datasheets/area_local_minimizado.csv'
    for data in read_vantive(filename):
        print(data)
