load data local infile '/home/vaughn.hagerty/orange/data/parview.txt' replace into table dash_orange_property fields terminated by '|';
delete from dash_orange_property where pin = '';

