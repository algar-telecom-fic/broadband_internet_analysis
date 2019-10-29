from CTO import CTO
from CTODict import CTODict
from City import City

class ProcessFile:
    def __init__(self, filepath):
        self.filepath = filepath

    def run(self):
        with open(self.filepath, 'r', encoding='ISO-8859-1') as file:
            cto_data = CTODict()
            city_data = CTODict()

            next(file) #skips the first line
            for line in file.readlines():

                attributes = line.split(';')

                localidade = str(attributes[14])
                estacao    = str(attributes[15])
                cto        = str(attributes[1])
                status     = str(attributes[13])

                if localidade == 'VIRTUAL':
                    continue

                cto_data.get(cto, CTO(localidade, estacao, cto)).add(status)
                city_data.get(localidade, City(localidade)).add(status)

            return (cto_data, city_data)
