import ftplib
import datetime
from subprocess import call
import MySQLdb


table = 'raleigh_incidents'
database = 'crime'
data_path = '/home/vaughn.hagerty/crime-scrapers/data/'
server = 'ftp.raleighpd.org'
ftp_user = {'user': 'opennc@raleighpd.org', 'pw': '4560$Bzitrj'}
db_user = {'user': 'crimeloader', 'pw': 'redaolemirc'}


def make_filename():
    year = datetime.datetime.today().strftime('%Y')
    doy = str(int((datetime.datetime.today() - datetime.timedelta(days=1)).strftime('%j')))
    return year + doy + '.txt'


def load_data(filename):
    load_command = 'mysql --local-infile --user=' + db_user['user'] + ' --password=' + db_user[
        'pw'] + ' ' + database + ' -e ' \
                   + '"load data local infile \'' + data_path + filename + '\' ' \
                   + 'replace into table ' + table + '";'
    print load_command
    exit()
    call(load_command, shell=True)

    sql = "insert into incidents(record_id, agency, county, charge, date_reported, time_reported, on_date, address, lat, lon, scrape_type, id_generate) \
          select report_id, 'Raleigh Police Department','Wake', charge, date_reported, time_reported, if(date_occurred != '0000-00-00', date_occurred, ''), address, lat, lon, 'custom', 0 from raleigh_incidents"
    connection = MySQLdb.connect(user=db_user['user'],passwd=db_user['pw'],db=database)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


def print_file(data, filename):
    datafile = ''
    keys_wanted = ['Report Number', 'OffCode', 'OffDesc', 'Date Reported', 'Time Reported', 'Start Occurrence Date',
                   'Address', 'Beat', 'lat', 'lon']
    for row in data:
        line = []
        for key in keys_wanted:
            line.append(row[key])
        datafile += "\t".join(line) + "\n"
    with open(data_path + filename, 'w') as f:
        f.write(datafile)
        f.close()


def get_data(ftp, filename):
    data = []
    lat_lon = ['lat', 'lon']
    ftp.retrlines("RETR " + filename, data.append)
    headers = data.pop(0).split('|')
    headers = [header.strip() for header in headers]
    data = [row.strip().replace('.0000000', '') for row in data]
    data = [row.split('|') for row in data]
    data = [row + row[7].split(',') for row in data]
    keyed_data = [dict(zip(headers + lat_lon, row)) for row in data]
    print_file(keyed_data, filename)
    load_data(filename)


def main():
    filename = make_filename()
    ftp = ftplib.FTP(server)
    ftp.login(ftp_user['user'], ftp_user['pw'])
    # ls = []
    #    ftp.retrlines('NLST', ls.append )
    get_data(ftp, filename)
    ftp.close()


if __name__ == '__main__':
    main()
