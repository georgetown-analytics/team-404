##Script to create a new table of user features.  Lists all unique users in the data and creates features in the table.  Features include: number of log on/off, session time, frequency, average time they get to work.

import csv
import psycopg2
import pickle

from more_itertools import unique_everseen

#Connection information is stored in config file that is added to .gitignore
from config.rdsconfig import host, rdsuser, rdspassword

#set up a cursor
def startcursor():
		conn = psycopg2.connect(
			host=host,
			port="5432",
			database="weirdo",
			user=rdsuser,
			password=rdspassword
		)
		cur = conn.cursor()
		return cur

#get all of the table names
def tblnames(cur):
	cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
	tblList = cur.fetchall()
	return tblList

def unq(cur):
		cur.execute("SELECT DISTINCT comp FROM proc;")
		allusrs = cur.fetchall()

		cur.execute("SELECT DISTINCT usr FROM redteam;")
		temp = cur.fetchall()
		allusrs.extend(temp)

		cur.execute("SELECT DISTINCT srcusr FROM auth;")
		temp = cur.fetchall()
		allusrs.extend(temp)

		cur.execute("SELECT DISTINCT dstusr FROM auth;")
		temp = cur.fetchall()
		allusrs.extend(temp)
		#unique = list(unique_everseen(allusrs))
		unique = allusrs
		print("Unique users compiled and deduped.")
		tocsv('uniqueusersfile.csv',unique)
		return unique

def unqRTusr(cur):
	cur.execute("SELECT DISTINCT usr FROM redteam")
	unqRT = cur.fetchall()
	pkl(unqRT, "jar/unqredteamusrs.pkl")
	print(unqRT)
	return unqRT

def queryalltbl(cur, tblList):
	queries = []
	for i, tbl in tblList:
		queries[i] = "SELECT "

def tocsv(filename,data):
	with open(filename,'w', newline='') as file:
		writer = csv.writer(file)
		try:
			for row in data:
				writer.writerow([row])
			print("File saved.")
		except csv.Error as e:
			print(e)

def mkusrtbl(unqusr,cur):
	for usr in unqusr:
		query = "CREATE TABLE " + usr[0] + \
		" AS SELECT * FROM auth WHERE srcusr = \'" + usr[0] + "\' LIMIT 10;"
		print(query)
		cur.execute(query)

def cc(cur):
	cur.close()

def pickuniqueuser(cur, sample, table, column, uniquelist):
	for i in range(sample):
		query = "SELECT * from " + table + " WHERE " + column + " = \'" + i + "\' ;"
		print(query)

def pkl(cucumber, picklename):
	with open(picklename, 'wb') as output:
		pickle.dump(cucumber, output, pickle.HIGHEST_PROTOCOL)
		print("Pickle made. Filename = " + picklename)


## make some test variables
x = range(10)
l = list(x)
filename = 'woc11.csv'
cur = startcursor()
unqusr = [('U66',),('U2837',)]
