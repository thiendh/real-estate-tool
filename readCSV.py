import csv

with open('test.csv', newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		print(row['Street Full Address'])
