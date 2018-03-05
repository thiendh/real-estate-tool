username = 'appUser'
password = 'EWRET12345'
database = 'EastWestRealEstateTool'

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()
    cur.execute( "SELECT ML_Number, Street_Full_Address, APN FROM test" )
    for line in cur.fetchall() :
        print(line)

import pymysql
import csv

conn = pymysql.connect(host='localhost', port=3306, user='appUser', passwd=password, db=database)

cur = conn.cursor()
#cur.execute("INSERT INTO `EastWestRealEstateTool`.`test` (`ML_Number`, `Street_Full_Address`, `APN`) VALUES (123, 'Street Adrress', '123456')")
with open('test.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		sql = '''INSERT INTO `EastWestRealEstateTool`.`test` 
			(`ML_Number`,
			 `Street_Full_Address`,
			 `APN`)
			VALUES (%s,%s,%s);'''
		data = (int(row['ML_Number']), row['Street Full Address'], row['APN'])
		print('Inserting data ', data)
		cur.execute(sql, data)

cur.close()
conn.commit()
