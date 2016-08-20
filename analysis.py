##!!!!!!!!!!!!!!!!!!!!!!!!!!!!This code should not be run from untrusted connections.!!!!!!!!!!!!
##!!!!!!!!!!!!!!!!!!!!!!!!!!!!It is vulnerable to SQL Injection attacks.!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


import csv
import psycopg2
import pickle
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
import os
from os.path import isfile, join
from os import listdir
from operator import itemgetter
from hurry.filesize import size,si
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
	unique = set(allusrs)
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

#Subset the auth table by user.  Save to pickle on external harddrive.
def mkusrtbl(unqusr,cur):
	for usr in unqusr:
		if os.path.isfile('/media/pcgeller/PHOTOS/' + usr[0]) == True:
		#query = "CREATE TABLE " + usr[0] + "AS"\
			print(usr[0] + ' File Exists')
			continue
		else:
			query = "SELECT * FROM auth WHERE srcusr = \'" + usr[0] + "\' ;"
			print(query)
			cur.execute(query)
			result = cur.fetchall()
			pkl(result, os.path.abspath('/media/pcgeller/PHOTOS/' + usr[0]))

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

def labelallsessions(filelist):
	for f in filelist:
		usrrecorddict = []
		authdata = sorted(unpkl(join(jarpath,f)), key=itemgetter(1))
		cur.execute("SELECT column_name from information_schema.columns WHERE table_name = 'auth'")
		header = cur.fetchall()
		header = [x[0] for x in header]
		for record in authdata:
			recorddict = {k: v for k, v in zip(header,record)}
			print(recorddict)
			usrrecorddict.extend(recorddict)
			print(usrrecorddict)

# class session
# 	cur = cur
# 	def define sessions
# 		for each unique user select the time that authorient = logon and authtype = authmap
# # 		for each uniuqe user select the time that authorient = log off and authtype = authmap
# # 		all times between are session i for user
#
# def modata(usr, ):
# 	for usr in uniqueusers:
# 		cur.execute("SELECT * FROM ")
#
# for item in sessionlist;
# 	build count and dummy variable stats

def mkfiledictionary(path):
	"""Make dictionary of files and their byte size and readable size\
	Sorted by their filesize in bytes."""
	filelist = [f for f in listdir(path) if isfile(join(path,f))]
	dict = {f: [os.path.getsize(join(path,f)), size(os.path.getsize(join(path,f)))] for f in filelist}
	dict = sorted(dict, key = itemgetter(0))

## make some test variables
x = range(10)
l = list(x)
filename = 'woc11.csv'
cur = startcursor()
unqusr = [('U66',),('U2837',)]

cur.execute("SELECT column_name from information_schema.columns WHERE table_name = 'auth'")
authheader = cur.fetchall()
cur.execute("SELECT column_name from information_schema.columns WHERE table_name = 'proc'")
procheader = cur.fetchall()
cur.execute("SELECT column_name from information_schema.columns WHERE table_name = 'flows'")
flowsheader = cur.fetchall()
cur.execute("SELECT column_name from information_schema.columns WHERE table_name = 'dns'")
dnsheader = cur.fetchall()
cur.execute("SELECT column_name from information_schema.columns WHERE table_name = 'redteam'")
redteamheader = cur.fetchall()


authuniqueusersize = "26320"
uniqueusers = unpkl('jar/uniqueusers.pkl')
lastvalue = "C23917"
jarpath = '/media/pcgeller/PHOTOS'
files = listdir(jarpath)
# onlyfile = [f for f in listdir(jarpath) if isfile(join(jarpath,f))]
# d = {f: [os.path.getsize(join(jarpath, f)), size(os.path.getsize(join(jarpath,f)))] for f in listdir(jarpath)}
#uniqueusers returned by unq() contains duplicates
#KLUDGE to dedup so the sql queries don't need to run
uniqueusers = list(set(uniqueusers))
sampleusr = unpkl('jar/U8556')
cur.execute("SELECT column_name from information_schema.columns WHERE table_name = 'auth'")
header = cur.fetchall()
header = [x[0] for x in header]
c1 = sorted(unpkl(join(jarpath,files[1])), key=itemgetter(1))
df = pd.DataFrame(c1, columns = header)

am = df.loc[df['authorient'] == "AuthMap"]
colcounts = df.groupby('authorient').size()
colcountsalt = df.authorient.value_counts()
