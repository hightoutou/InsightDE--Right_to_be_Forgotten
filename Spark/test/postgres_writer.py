#####################
# Write data to postgreSQL
#####################

import psycopg2, datetime
 
counts = [('Android App Unknown Phone/Tablet', 25), ('Tablet', 21), ('iPhone', 134), ('Android Phone', 55), ('iPad Tablet', 45), ('Windows Desktop', 170), ('Mac Desktop', 231), ('iPodtouch', 1), ('Linux Desktop', 3), ('Chromebook', 2)]

connection = psycopg2.connect(host = 'ip-10-0-0-5', port = '5431', database = 'my_db', user = 'spark', password = 'spark')
cursor = connection.cursor()

timestamp = datetime.datetime.now()
for count in counts:
    query = 'INSERT INTO device_counts VALUES (%s, %s, %s)'
    data = (timestamp, count[0], count[1])
    cursor.execute(query, data)

connection.commit()
connection.close()
