#function to add the data from the file to the database
def add_port(filename, locale, station, cto, status):
    #using the global database
    global database
    
    #if any of these values is not in the dictionary yet, create the it's dictionary
    if locale not in database[filename]:
        database[filename][locale] = {}
    if station not in database[filename][locale]:
        database[filename][locale][station] = {}
        
    
    #the cto dictionary is where we're gonna count the registers by their status 
    if cto not in database[filename][locale][station]:
        database[filename][locale][station][cto] = {
            'DEFEITO':   0,
            'DESIGNADO': 0,
            'OCUPADO':   0,
            'RESERVADO': 0,
            'VAGO':      0,
            'AUDITORIA': 0,
            'total':     0,
        }
    
    #all lines add in the total
    database[filename][locale][station][cto]['total'] += 1
    
    #each line also adds in it's own status
    database[filename][locale][station][cto][status] += 1

#function to show everything in the database similarly to the spreadsheet
def show_database(filename):
    global database

    for locale in database[filename]:
        for station in database[filename][locale]:
            for cto in database[filename][locale][station]:
                print("%s %s %s" %(locale, station, cto) , end="")
               
                #print(database[filename][locale][station][cto])
                for status,value in database[filename][locale][station][cto].items():
                    print(" (%s: %i)" %(status, value), end="")
                

                print("")
    

                
#function for extrating the useful data from the file
def read_file(filename):
    
    #declaring the database as global will help we use it across different functions 
    global database
    
    #incially, the database for that file is just an empty dictionary
    database[filename] = {}
    
    #open the file
    with open(filename, 'r',  encoding = 'ISO-8859-1') as input_file:

        #iterate for all the lines
        for line in input_file.readlines():

            #split the csv by the semi-colon
            v = line.split(';')
            
            #take the cto status form the list
            status_cto = str(v[4]).strip()
            #we must consider only the existing CTO
            if status_cto == "EXISTENTE":
                #separate the important properties
                locale = str(v[14]).strip()
                station = str(v[15]).strip()
                cto = str(v[1]).strip()     
                status = str(v[13]).strip()    
                
                #printing in the screen just for debug purposes
                #print("%s %s %s %s" %(locale, station, cto, status))
                
                #add this line's data to the database
                add_port(filename, locale, station, cto, status)
            




global database
database = {}

filename='datasheets/Circuitos CTO-01-25.csv'
read_file(filename)
show_database(filename)
