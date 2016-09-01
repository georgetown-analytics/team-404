##!!!!!!!!!!!!!!!!!!!!!!!!!!!!This code should not be run from untrusted connections.!!!!!!!!!!!!
##!!!!!!!!!!!!!!!!!!!!!!!!!!!!It is vulnerable to SQL Injection attacks.!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pylab
from os import listdir
import os
from os.path import isfile, join
from os import listdir
from operator import itemgetter
from hurry.filesize import size,si
#Connection information is stored in config file that is added to .gitignore
from config.rdsconfig import host, rdsuser, rdspassword
from helperfunctions import *
#set up a cursor

import csv
import psycopg2
import pickle

def startconn():
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
	return(conn)

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

#Close postgres connection
def cc(cur):
	cur.close()

#get all of the table names
def gettblnames(cur):
	cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
	tblList = cur.fetchall()
	return tblList

def unq(cur):
	"""Gets a unique list of usrs and comps from all tables
	Doesn't dedup correctly.  See fix and end"""
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

def pickuniqueuser(cur, n, table, column, uniquelist):
	"""pick a unique user from the database"""
	for i in range(n):
		query = "SELECT * from " + table + " WHERE " + column + " = \'" + i + "\' ;"
		print(query)

def mkfiledictionary(path):
	"""Make dictionary of files and their byte size and readable size\
	Sorted by their filesize in bytes."""
	filelist = [f for f in listdir(path) if isfile(join(path,f))]
	dict = {f: [os.path.getsize(join(path,f)), size(os.path.getsize(join(path,f)))] for f in filelist}
	#dict = sorted(dict, key = itemgetter(0))
	return(dict)

def labelsessions(df,tstamplist):
	"""Label the sessions for a unique user or computer."""
	i = 0
	for s in tstamplist:
		#print(s)
		if i == 0:
			print("first item")
			print(i)
			sub = df[(df.tstamp < tstamplist[i])]
			df.loc[sub.index,'session'] = i
			i += 1
		elif i >= 1 and i < len(tstamplist) - 1:
			print(i)
			print(type(i))
			print( i >= 1 and i < len(tstamplist) - 1)
			sub = df[(df.tstamp >= tstamplist[i -1]) & (df.tstamp < tstamplist[i])]
			df.loc[sub.index,'session'] = i
			i += 1
		elif i == len(tstamplist) - 1:
			print("on last item")
			sub = df[(df.tstamp >= tstamplist[i])]
			df.loc[sub.index,'session'] = i
			print(tstamplist[i])
			print("Filelist looped")

def labelNONAUTHsessions(tblnames, headers ,filepaths, tstamps):
	for t in tblnames:
		filelist = listdir(filepaths[t])




def labelauthsessions(header, openpath, savepath):
	"""Open unique user and computer pickle from auth table.
	Read file as dataframe.  Loop through and extract AuthMap events and
	the timestamp they occured. Store tstamps in dictionary keyed on unique usr/comp
	Pickle dataframe. <- worth it?"""
	filelist = listdir(openpath)
	filelist.remove('$RECYCLE.BIN')
	tstampdict = {}
	emptyfiles = []
	for f in filelist:
		try:
			data = sorted(unpkl(os.path.join(openpath,f)), key=itemgetter(1))
		except EOFError:
			print("File " + f + " is empty!")
			emptyfiles.append(f)
			pkl(emptyfiles, '/media/pcgeller/SharedDrive/weirdo/workspace/emptyfiles.pkl')
			next
		df = pd.DataFrame(data, columns = header)
		df.sort(columns = 'tstamp')
		authdata = df.loc[df['authorient'] == "AuthMap"]
		tstamplist = authdata['tstamp']
		tstamplist = sorted(tstamplist)
		tstampdict[f] = tstamplist
		labelsessions(df, tstamplist)
		pkl(tstampdict, '/home/pcgeller/workspace/weirdo/tstampdict.pkl')
		pkl(df, os.path.abspath(savepath + f + '.pkl'))
	return(tstampdict)

def splittable(unqusrlist, table, conn, fieldname, filepaths):
	"""Split a remote table by a fieldname.
	Save as a pickle at ./table/uniquefieldname"""
	filepath = filepaths.get(table)
	toobig = []
	toomanyrows = {}
	for usr in unqusrlist:
		if table == 'auth':
			savelocation = os.path.join(filepath,usr)
		else:
			savelocation = os.path.abspath(filepath,usr + table + '.pkl')

		if os.path.isfile(savelocation) == True:
			print(usr + ' File Exists')
			continue
		else:
			try:
				print("Getting: " + usr)
				servercur = conn.cursor('serverside')
				servercur.execute("SELECT * FROM %s WHERE %s = '%s'" % (table, fieldname, usr))
					if servercur.rowcount < 7000000:
						print("Table is " + servercur.rowcount + " rows.  Fetching.")
						result = []
						for record in servercur:
						result.append(record)
						pkl(result, os.path.abspath(savelocation))
						cc(servercur)
					else:
						print("Table " + usr + "is " + servercur.rowcount + "rows.  Skipping.")
						toomanyrows[usr] = servercur.rowcount
						pkl(os.path.join(filepaths['workspace'],"toomanyrows.pkl"))
						next
			except MemoryError:
				print("Table is too big!  Saving and going to the next one")
				toobig.append(usr)
				pkl(toobig, os.path.abspath('/media/pcgeller/SharedDrive/weirdo/workspace/toobig.pkl'))
				cc(servercur)
				next




# ##!!!!!Kludge before of messedup auth names
# def splitauthtable(unqusrlist, table, conn, savepath, fieldname='srcusr',):
# 	"""Split a remote table by a fieldname.
# 	Save as a pickle at ./table/uniquefieldname"""
# 	for usr in unqusrlist:
# 		savelocation = os.path.abspath(savepath + '/' + usr)
# 		if os.path.isfile(savelocation) == True:
# 			print(usr + ' File Exists')
# 			continue
# 		else:
# 			print("Getting: " + usr)
# 			servercur = conn.cursor('serverside')
# 			servercur.execute("SELECT * FROM %s WHERE %s = '%s'" % (table, fieldname, usr))
# 			print("Query sent")
# 			result = []
# 			for record in servercur:
# 				result.append(record)
# 			pkl(result, os.path.abspath(savelocation))
# 			cc(servercur)

def dfFilepathdict(tblnames):
	dffp = {}
	for t in tblnames:
		dffp[t] = os.path.join('/media/pcgeller/SharedDrive/weirdo/dataframes/' + t)
	return(dffp)

def t2l(tuple):
	'''converts a list of tuples to a list'''
	list = [x[0] for x in tuple]
	return(list)

#headers = getheaders(tblnames)

def getheaders(tablelist):
	headers = {}
	for t in tablelist:
		cur.execute("SELECT column_name from information_schema.columns WHERE \
		table_name = '%s'" % (t))
		headers[t]= t2l(cur.fetchall())
	return(headers)

####Handy Variables
conn = startconn()
cur = conn.cursor()
#KLUDGE to dedup so the sql queries don't need to run
#uniqueusers returned by unq() contains duplicates
uniqueusers = t2l(unpkl('jar/uniqueusers.pkl'))
uniqueusers = list(set(uniqueusers))

filepaths = {"auth":'/media/pcgeller/PHOTOS', "flows":'/media/pcgeller/SharedDrive/weirdo/flows', \
			"redteam":'/media/pcgeller/SharedDrive/weirdo/redteam',"proc":'/media/pcgeller/SharedDrive/weirdo/proc', \
			"dns":'/media/pcgeller/SharedDrive/weirdo/dns', \
			"workspace":'media/pcgellerSharedDrive/weirdo/workspace'}


alltblnames = t2l(gettblnames(cur))
tblnames = alltblnames[:-1]
#tblnamesNOAUTH = tblnames.remove('auth')
headers = getheaders(tblnames)
dfFilepaths = dfFilepathdict(tblnames)
authfiles = listdir(filepaths['auth'])
authfiles.remove('$RECYCLE.BIN')
workspace = '/media/pcgeller/SharedDrive/weirdo/workspace/'

# authfiles = listdir(filepaths['auth'])
# authfiles.remove('$RECYCLE.BIN')

##Make some dummy variables
authuniqueusersize = "26320"
# sampleusr = unpkl('jar/U8556')
lastvalue = "C23917"
jarpath = './jar'
filelist = ["U8946"]
x = range(10)
l = list(x)
filename = 'woc11.csv'
unqusr = [('U66',),('U2837',)]

sampleusr = unpkl(os.path.join(filepaths['auth'], "U2109"))
sampledf = pd.DataFrame(sampleusr, columns = headers['auth'])

samplecomp = unpkl(os.path.join(filepaths['auth'], "U2109"))
samplecompdf = pd.DataFrame(samplecomp, columns = headers['auth'])

#servercur = conn.cursor('serverside')
#test = labelauthsessions(headers['auth'],filepaths['auth'],workspace)
####Handy Code
# onlyfile = [f for f in listdir(authfilepath) if isfile(join(authfilepath,f))]
# d = {f: [os.path.getsize(join(authfilepath, f)), size(os.path.getsize(join(authfilepath,f)))] for f in listdir(authfilepath)}
# c1 = sorted(unpkl(join(authfilepath,authfiles[1])), key=itemgetter(1))
# df = pd.DataFrame(c1, columns = header)
# #am = df.loc[df['authorient'] == "AuthMap"]
# colcounts = df.groupby('authorient').size()
# colcountsalt = df.authorient.value_counts()
