import datetime

def now():
    now = datetime.date.today()
    return str(now)
    

def date_difference(old_date):
    now = datetime.datetime.now()
    
    #erase the next line plz
    #now = datetime.datetime.strptime('2019-1-25', '%Y-%m-%d')
    
    old = datetime.datetime.strptime(old_date, '%Y-%m-%d %H:%M:%S')
    return (now-old).days
