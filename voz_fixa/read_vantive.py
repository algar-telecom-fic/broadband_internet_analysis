#filename = 'datasheets/area_local_minimizado.csv'
filename = 'datasheets/Relatorio_Area_Local09042019080046.csv'

database = {}
possible_status = []
with open(filename, 'r', encoding='ISO-8859-1') as input_file:
    #status = input_file.readline().split(';')[:-1]
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

        lista_vantive.append(item)

print(lista_vantive)
