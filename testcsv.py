username = 'appUser'
password = 'EWRET12345'
database = 'EastWestRealEstateTool'

fieldList = ('ML_Number',
'Street Full Address',
'Subdist Desc',
'Selling Date',
'Listing Price',
'Selling Price',
'Listing Agent Name',
'Listing Co-Agent Name',
'Selling Agent Name',
'Selling Co-Agent Name',
'Property_Type_Code',
'Latitude',
'Longitude',
'Bedrooms',
'Total Bathrooms',
'Square Footage',
'Selling_Price_Per_Sqft',
'DOM',
'APN',
'# of Units')

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
    cur = conn.cursor()
    cur.execute( "SELECT ML_Number, Street_Full_Address, APN FROM test" )
    for line in cur.fetchall() :
        print(line)

import pymysql
import csv
import time
from sshtunnel import SSHTunnelForwarder

with SSHTunnelForwarder(
         ('sp18-cs411-dso-003.cs.illinois.edu', 22),
         ssh_password="theominhD0",
         ssh_username="thiendo2",
         remote_bind_address=('127.0.0.1', 3306)) as server:

    conn = pymysql.connect(host='localhost', port=server.local_bind_port, user='appUser', passwd=password, db=database)

    cur = conn.cursor()
    insert = 'INSERT INTO `EastWestRealEstateTool`.`test` ('
    replace = ''
    fields = ''
    for field in fieldList:
        fields = fields + ' `' + field + '`,'
        replace = replace + '%s, '

    fields = fields[0: len(fields)-1]
    replace = replace[0:len(replace)-2]
    # sql = sql + fields + ') VALUES (' + replace + ');'


    with open('test.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
          data = ''
          sql = ''
          for field in fieldList:
                if len(row[field]) == 0: data = data + 'NULL,'
                else: data= data + "'" + row[field] + "', "
            # print('Inserting data ', data[0:len(data)-2])
          sql = insert + fields + ') VALUES (' + data[0:len(data)-2] + ');'
          print(sql)
         # time.sleep(5)
          cur.execute(sql)

    cur.close()
    conn.commit()
