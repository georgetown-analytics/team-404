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

def splittable(unqusrlist, table, conn, splitdict, filepaths):
    """Split a remote table by a fieldname.
    Save as a pickle at ./table/uniquefieldname"""
    fieldname = splitdict[table]
    print(filepaths)
    print("#####")
    print(type(filepaths))
    filepath = filepaths.get(table)
    toobig = []
    emptyfiles = []
    toomanyrows = {}
    for usr in unqusrlist:
        ##Kludge because auth tbls aren't following the naming convention
        if table == 'auth':
            print("TABLE IS AUTH")
            savelocation = os.path.join(filepath,usr)
        else:
            savelocation = os.path.join(filepath,(usr + '.pkl'))

        if os.path.isfile(savelocation) == True:
            print(usr + ' File Exists')
        else:
            try:
                ##Ran into loads of memory errors.  Even on the Postgres server.
                ##Easier to just subset the data and then check it against the redteams.
                print("Getting: " + usr)
                cur = conn.cursor()
                cur.execute("SELECT * FROM %s WHERE %s = '%s'" % (table, fieldname, usr))
                count = cur.rowcount
                if 0 < count < 7000000:
                    print("Table is " + str(count) + " rows.  Fetching.")
                    result = []
                    data = cur.fetchall()
                    pkl(data, os.path.abspath(savelocation))
                    # for record in servercur:
                    #     result.append(record)
                    #     pkl(result, os.path.abspath(savelocation))
                        #cc(servercur)
                    cc(cur)
                    next
                elif count == 0:
                    print("No records, recording and skipping.")
                    emptyfiles.append(usr)
                    pkl(emptyfiles,os.path.join("",filepaths['workspace'],(table + 'emptyfiles.pkl')))
                    cc(cur)
                    next
                else:
                    print("Table " + usr + "is " + str(count) + "rows.  Skipping.")
                    toomanyrows[usr] = count
                    pkl(toomanyrows,os.path.join(filepaths['workspace'],(table + "toomanyrows.pkl")))
                    cc(cur)
                    next
            except MemoryError:
                print("Table is too big!  Saving and going to the next one")
                toobig.append(usr)
                pkl(toobig, os.path.abspath('/media/pcgeller/SharedDrive/weirdo/workspace/toobig.pkl'))
                cc(cur)
                next
            except psycopg2.ProgrammingError:
                print("Serverside cursor already exists")
                conn.rollback()
                cur = conn.cursor()
                next
            except psycopg2.InternalError:
                print("Cursor not rolledback")
                conn.rollback()
                next
def comp(list1, list2):
    for val in list1:
        if val in list2:
            return True
    return False
#Quick check to see if all redteam users are in the extracted auth data.
#TRUE
#comp(listdir(filepaths['auth']), uniquert)

# ##!!!!!Kludge before of messedup auth names
# def splitauthtable(unqusrlist, table, conn, savepath, fieldname='srcusr',):
#     """Split a remote table by a fieldname.
#     Save as a pickle at ./table/uniquefieldname"""
#     for usr in unqusrlist:
#         savelocation = os.path.abspath(savepath + '/' + usr)
#         if os.path.isfile(savelocation) == True:
#             print(usr + ' File Exists')
#             continue
#         else:
#             print("Getting: " + usr)
#             servercur = conn.cursor('serverside')
#             servercur.execute("SELECT * FROM %s WHERE %s = '%s'" % (table, fieldname, usr))
#             print("Query sent")
#             result = []
#             for record in servercur:
#                 result.append(record)
#             pkl(result, os.path.abspath(savelocation))
#             cc(servercur)

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
#cur.execute("select distinct usr from redteam")
#uniquert = cur.fetchall()
#uniquert = pkl(uniquert,'jar/uniquert.pkl')
uniquert = t2l(unpkl('jar/uniquert.pkl'))

filepaths = {"auth":'/media/pcgeller/PHOTOS',
            "flows":'/media/pcgeller/SharedDrive/weirdo/flows',
            "redteam":'/media/pcgeller/SharedDrive/weirdo/redteam',
            "proc":'/media/pcgeller/SharedDrive/weirdo/proc',
            "dns":'/media/pcgeller/SharedDrive/weirdo/dns',
            "workspace":'/media/pcgeller/SharedDrive/weirdo/workspace',
            "dataframes":'/media/pcgeller/SharedDrive/weirdo/dataframes'}

splitdict = {"auth":'srcusr',
            "flows":'srccomputer',
            "redteam":'usr',
            "proc":'comp',
            "dns":'srccomputer'}


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

x = range(10)
l = list(x)
filename = 'woc11.csv'
unqusr = [('U66',),('U2837',)]
nonRTusers = [x for x in uniqueusers if x not in uniquert]
nonRTusrsamp = random.sample(nonRTusers, 350)
usrs = nonRTusrsamp + uniquert

#



#servercur = conn.cursor('serverside')
# labelauthsessions(headers['auth'],filepaths['auth'],workspace)
####Handy Code
# onlyfile = [f for f in listdir(authfilepath) if isfile(join(authfilepath,f))]
# d = {f: [os.path.getsize(join(authfilepath, f)), size(os.path.getsize(join(authfilepath,f)))] for f in listdir(authfilepath)}
# c1 = sorted(unpkl(join(authfilepath,authfiles[1])), key=itemgetter(1))
# df = pd.DataFrame(c1, columns = header)
# #am = df.loc[df['authorient'] == "AuthMap"]
# colcounts = df.groupby('authorient').size()
# colcountsalt = df.authorient.value_counts()
