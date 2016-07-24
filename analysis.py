import psycopg2 as pg

#store connection information in seperate file that is in .gitignore

from config.rdsconfig import host, rdsuser, rdspassword

#set up

conn = pg.connect(
	host=host,
	port="5439",
	database="weirdo",
	user=rdsuser,
	password=rdspassword
)
cur = conn.cursor()

#create list of tables

#create list of unique computers


#create list of unique users

#associate red team activity with rest of data

#
#cur.execute("SELECT DISTINCT computer FROM redteam;")
#uniqueredteamcomputers = cur.fetchall()

# for computer in uniqueredteamcomputers:
# 	print computer
	#SQL = "CREATE TABLE %s

	#data = computer
	#cur.execute(

cur.close()
conn.close()
