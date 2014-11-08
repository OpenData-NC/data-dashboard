import datetime
import MySQLdb


def find_min_date(agency):
    user = 'crimeloader'
    pw = 'redaolemirc'
    db = 'crime'
    data_tables = ['accidents','arrests','citations','incidents']
    connection = MySQLdb.connect(user=user, passwd=pw, db=db)
    cursor = connection.cursor()
    sql = 'select min(date_reported) from incidents where agency = "' + agency + '" and date_reported > "00-00-00"'
    cursor.execute(sql)
    min_date = cursor.fetchone()[0]
    if not min_date:
        sql = 'select min(date_occurred) from arrests where agency = "' + agency + '" and date_occurred > "00-00-00"'
        cursor.execute(sql)
        min_date = cursor.fetchone()[0]
    if agency == 'Huntersville Police Department':
        sql = 'select min(date_occurred) from citations where agency = "' + agency + '" and date_occurred > "00-00-00"'
        cursor.execute(sql)
        min_date = cursor.fetchone()[0]

    cursor.close()
    return min_date

#make an array of formatted dates we'll use to grab
#each of the bulletin pages
def make_dates(agency, howfar=0):
    howfar_save = howfar
    min_date = find_min_date(agency)
#    start_hist_date = datetime.datetime.strptime(min_date,'%Y-%m-%d')
    dates = []
    while howfar >= 0:
        date = (datetime.datetime.today() - datetime.timedelta(days=howfar)).strftime('%m/%d/%Y')
        dates.append(date)
        howfar -= 1
    howfar = howfar_save
    if min_date:
        while howfar > 0:
            date = (min_date - datetime.timedelta(days=howfar)).strftime('%m/%d/%Y')
            dates.append(date)
            howfar -= 1
    print agency
    print dates
    return dates


def find_range(farback, start_date = 0):
    if not start_date:
        start_date = datetime.datetime.today()
    date_wanted = (start_date - datetime.timedelta(days=farback)).strftime('%m/%d/%Y')
    return {'MasterPage$mainContent$txtDateFrom2': date_wanted, 'MasterPage$mainContent$txtDateTo2': date_wanted}


def make_date_ranges(agency, howfar = 0):
    howfar_save = howfar
    min_date = find_min_date(agency)
    date_ranges = []
    while howfar >= 0:
        date_ranges.append(find_range(howfar))
        if min_date:
            date_ranges.append(find_range(howfar,min_date))
        howfar -= 1
    print agency
    print date_ranges
    return date_ranges

	
def format_db_datetime(date_string):
    if date_string.find('M') != -1:
        return datetime.datetime.strptime(date_string, '%m/%d/%Y %I:%M:%S %p').strftime('%Y/%m/%d %H:%M:%S')
    elif len(date_string.split(':')) == 3:
        return datetime.datetime.strptime(date_string, '%m/%d/%Y %H:%M:%S').strftime('%Y/%m/%d %H:%M:%S')
    elif date_string.find('/') != -1:
        try:
            return datetime.datetime.strptime(date_string, '%m/%d/%Y %H:%M').strftime('%Y/%m/%d %H:%M')
        except ValueError as e:
            print date_string
            return ''
    else:
    #there's no date or it has an odd format
        print date_string
        return ''
    

def format_db_date(date_string):
    return datetime.datetime.strptime(date_string, '%m/%d/%Y').strftime('%Y/%m/%d')


def format_search_date(date_string):
    return datetime.datetime.strptime(date_string, '%Y/%m/%d').strftime('%m/%d/%Y')


def format_db_date_part(date_string):
    if date_string.find('M') != -1:
        return datetime.datetime.strptime(date_string, '%m/%d/%Y %I:%M:%S %p').strftime('%Y/%m/%d')
    elif len(date_string.split(':')) == 3:
        return datetime.datetime.strptime(date_string, '%m/%d/%Y %H:%M:%S').strftime('%Y/%m/%d')
    else:
        return datetime.datetime.strptime(date_string, '%m/%d/%Y %H:%M').strftime('%Y/%m/%d')
    


def format_db_time_part(date_string):
    if date_string.find('M') != -1:
        return datetime.datetime.strptime(date_string, '%m/%d/%Y %I:%M:%S %p').strftime('%H:%M:%S')
    elif len(date_string.split(':')) == 3:
        return datetime.datetime.strptime(date_string, '%m/%d/%Y %H:%M:%S').strftime('%H:%M:%S')
    else:
        return datetime.datetime.strptime(date_string, '%m/%d/%Y %H:%M').strftime('%H:%M')

def format_date_time(data, position):
    if position not in data:
        data[position] = ''
        data['date_occurred'] = ''
        data['time_occurred'] = ''
    elif data[position].find(':') != -1:
        data['date_occurred'] = format_db_date_part(data[position])
        data['time_occurred'] = format_db_time_part(data[position])
    else:
        data['date_occurred'] = format_db_date(data[position])
        data['time_occurred'] = ''
    return data

def format_reported_date(data,position):
    if position not in data:
        data[position] = ''
    else:
        if data[position].find(':') != -1:
            data['date_reported'] = format_db_date_part(data[position])
            data['time_reported'] = format_db_time_part(data[position])
        else:
            data['date_reported'] = format_db_date(data[position])
            data['time_reported'] = ''
        data[position] = format_db_datetime(data[position])
    return data

def on_between(data):
    on_and_between = {'on_date': '', 'from_date': '', 'to_date': ''}
    if data['on_or_between'] == 'on':
        date_pieces = data['occurred_date'].split(', ')
        if date_pieces[0].find(':') == -1:
            date_pieces[0] = (' ').join(date_pieces)
        on_and_between['on_date'] = format_db_datetime(date_pieces[0])
    else:
        pieces = data['occurred_date'].split(' and ')
        from_date_pieces = pieces[0].split(', ')
        to_date_pieces = pieces[1].split(', ')
        if from_date_pieces[1].find(':') == -1:
            from_date = from_date_pieces[1] + ' ' + from_date_pieces[0]
        else:
            from_date = from_date_pieces[1]
        if to_date_pieces[1].find(':') == -1:
            to_date = to_date_pieces[1] + ' ' + to_date_pieces[0]
        else:
            to_date = to_date_pieces[1]
        on_and_between['from_date'] = format_db_datetime(from_date)
        on_and_between['to_date'] = format_db_datetime(to_date)
    return dict(data.items() + on_and_between.items())
