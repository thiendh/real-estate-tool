username = 'appUser'
password = 'EWRET12345'
database = 'EastWestRealEstateTool'

fieldList = ('Street Full Address',
'Subdist Desc',
'Property_Type_Code',
'Latitude',
'Longitude',
'Bedrooms',
'Total Bathrooms',
'Square Footage',
'APN',
'HOA Dues',
'Year Built',
'Lot Size - Sq Ft',
'Views Desc',
'Address - ZIP',
'Status')

import pymysql
import csv
import time
import os

ilog = open("insert.csv", "a")
ulog = open("update.csv","a")

conn = pymysql.connect(host='localhost', port=3306,
                         user='appUser', passwd=password, db=database,
                         use_unicode=True, charset="utf8")

cur = conn.cursor()
insert = 'INSERT INTO `EastWestRealEstateTool`.`property_sample` ('
replace = ''
fields = ''
for field in fieldList:
    fields = fields + ' `' + field + '`,'
    replace = replace + '%s, '

fields = fields[0: len(fields)-1]
replace = replace[0:len(replace)-2]

APNList = list()

with open('sfh-property.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    i = 0
    for row in reader:
      i = i+1
      data = ''

      if len(row['APN']) == 0 or row['APN'] == 'New Or Under Construction': row['APN'] = row['Street Full Address']

      cur.execute('''SELECT APN FROM `EastWestRealEstateTool`.`property_sample`
                    WHERE APN = %s;''', row['APN'])
      search = cur.fetchone()

      if search is None: #New record
          sql = '''INSERT INTO `EastWestRealEstateTool`.`property_sample`
                    (`﻿Street Full Address`,
                    `Subdist Desc`,
                    `Property_Type_Code`,
                    `Latitude`,
                    `Longitude`,
                    `Bedrooms`,
                    `Total Bathrooms`,
                    `Square Footage`,
                    `APN`,
                    `HOA Dues`,
                    `Year Built`,
                    `Lot Size - Sq Ft`,
                    `Views Desc`,
                    `Address - ZIP`,
                    `Status`)
                    VALUES ('''
          for field in fieldList:
              if len(row[field]) == 0: data = data + 'NULL,'
              else: data= data + "'" + row[field] + "', "
          # print('Inserting data ', data[0:len(data)-2])
          sql = sql + data[0:len(data)-2] + ');'
          print('Insert ',i)
          #time.sleep(5)
          cur.execute(sql)
          ilog.write(row['APN'] + '\n')
      else: #already in DB, need update
          print('Update ',i)
          sql = '''UPDATE `EastWestRealEstateTool`.`property_sample`
                    SET '''
          for field in fieldList:
              # No update for APN / Street address / Null values
              if field != 'APN' and field != 'Street Full Address' and len(row[field]) != 0:
                  data = data + ' `' + field + "` = '" + row[field] + "', "
          sql = sql + data[0:len(data)-2] + " WHERE APN = '" + row['APN'] + "';"
          # print(sql)
          cur.execute(sql)
          ulog.write(row['APN'] + '\n')

ilog.close()
ulog.close()
cur.close()
conn.commit()
