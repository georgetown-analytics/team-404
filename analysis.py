##!!!!!!!!!!!!!!!!!!!!!!!!!!!!This code should not be run from untrusted connections.!!!!!!!!!!!!
##!!!!!!!!!!!!!!!!!!!!!!!!!!!!It is vulnerable to SQL Injection attacks.!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


import csv
import psycopg2
import pickle
import random

#Connection information is stored in config file that is added to .gitignore
from config.rdsconfig import host, rdsuser, rdspassword

#set up a cursor
def startcursor():
	try:
		conn = psycopg2.connect(
			host=host,
			port="5432",
			database="weirdo",
			user=rdsuser,
			password=rdspassword
		)
	except:
		print ("\n_________CONNECTION FAILURE_________\n")
	cur = conn.cursor()
	return cur

#get all of the table names
def tblnames(cur):
	cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
	tblList = cur.fetchall()
	return tblList

#Make a list of unique users (also includes some source computers).  We need to decide how we define a 'user'
##and if we remove the computers.

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
	pkl(unique, "jar/uniqueusers.pkl")
	return unique

#Make a list of the unique redteam users.
def unqRTusr(cur):
	cur.execute("SELECT DISTINCT usr FROM redteam")
	unqRT = cur.fetchall()
	pkl(unqRT, "jar/unqredteamusrs.pkl")
	print(unqRT)
	return unqRT

#Query all the tables in the database for a particular field value.
def queryalltbl(cur, tblList):
	queries = []
	for i, tbl in tblList:
		queries[i] = "SELECT "

#Subset the auth table by user.
def mkusrtbl(unqusr,cur):
	for usr in unqusr:
		query = "CREATE TABLE " + usr[0] + \
		" AS SELECT * FROM auth WHERE srcusr = \'" + usr[0] + "\' LIMIT 10;"
		print(query)
		cur.execute(query)

#Close postgres connection
def cc(cur):
	cur.close()

#Select n random unique values a table.
def pickrandom(cur, n, unqlist, table, field):
	"""Select n unique values from a list.\
	Then, query a specified field and table for the results.\
	Saves a pkl and csv."""
	sample = []
	output = []
	sample = random.sample(unqlist, n)
	sample = [x[0] for x in sample]
	for i in sample:
		query = "SELECT * FROM " + table + " WHERE " + field + "= \'" + i + "\' ;"
		cur.execute(query)
		queryresult = cur.fetchall()
		output.extend(queryresult)
	pkl(output, 'jar/' + str(n) + 'randomsamples.pkl')
	tocsv('output/' + str(n) + 'randomsamples.csv', output)
	return(output)

def pickselect(cur,start, stop, unqlist, table, field):
	print(cur)

def pickuniqueuser(cur, n, table, column, uniquelist):
	for i in range(n):
		query = "SELECT * from " + table + " WHERE " + column + " = \'" + i + "\' ;"
		print(query)

def tocsv(filename,data):
	with open(filename,'w', newline='') as file:
		writer = csv.writer(file)
		try:
			for row in data:
				writer.writerow([row])
			print("File saved.")
		except csv.Error as e:
			print(e)

def pkl(cucumber, filename):
	with open(filename, 'wb') as output:
		pickle.dump(cucumber, output, pickle.HIGHEST_PROTOCOL)
		print("Pickle made. Filename = " + filename)

def unpkl(filename):
	with open(filename, 'rb') as input:
		cucumber = pickle.load(input)
		return cucumber

class session
	cur = cur
	def define sessions
		for each unique user select the time that authorient = logon and authtype = authmap
		for each uniuqe user select the time that authorient = log off and authtype = authmap
		all times between are session i for user


for item in sessionlist;
	build count and dummy variable stats

## make some test variables
x = range(10)
l = list(x)
filename = 'woc11.csv'
cur = startcursor()
unqusr = [('U66',),('U2837',)]
unqredteam = unpkl('jar/unqredteamusrs.pkl')
