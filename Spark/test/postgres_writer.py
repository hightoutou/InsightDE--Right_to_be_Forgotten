#####################
# Write data to postgreSQL
#####################

import psycopg2, datetime
 
counts = [(('view', 'Android App Unknown Phone/Tablet'), 25), (('click', 'Tablet'), 21)]

connection = psycopg2.connect(host = 'ip-10-0-0-5', port = '5431', database = 'my_db', user = 'spark', password = 'spark')
cursor = connection.cursor()

timestamp = datetime.datetime.now()
for count in counts:
    query = 'INSERT INTO device_avg_time_filter VALUES (%s, %s, %s, %s)'
    data = (timestamp, count[0][0], count[0][1], count[1])
    cursor.execute(query, data)

connection.commit()
connection.close()
