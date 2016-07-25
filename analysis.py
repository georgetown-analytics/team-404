import psycopg2 as pg

#store connection information in seperate file that is in .gitignore

from config.rdsconfig import host, rdsuser, rdspassword

#set up
def connectaws():
		conn = pg.connect(
			host=host,
			port="5432",
			database="weirdo",
			user=rdsuser,
			password=rdspassword
		)
		cur = conn.cursor()
		return cur

#create list of tables
#cur()
#create list of unique computers
#create list of unique users

#cur = cur

<<<<<<< HEAD
cur.execute("SELECT DISTINCT usr FROM redteam;")
unqredteamusr = list(cur.fetchall())

cur.execute("SELECT DISTINCT dst FROM redteam;")
rdteamunqcmp = cur.fetchall()
#uniqueredteamcomputers = cur.fetchall()
for computer in rdteamunqcmp:
	print computer
=======
#
#cur.execute("SELECT DISTINCT computer FROM redteam;")
#uniqueredteamcomputers = cur.fetchall()

# for computer in uniqueredteamcomputers:
# 	print computer
>>>>>>> 65a7caf9d2f5e2d182563e11eec50687c6d77e87
	#SQL = "CREATE TABLE %s

	#data = computer
	#cur.execute(

def disconnectaws():
	cur.close()
	conn.close()
	return

