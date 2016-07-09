import psycopg2

conn = psycopg2.connect("dbname=weirdo user=postgres;")
cur = conn.cursor()

uniquecomputers = cur.execute("SELECT DISTINCT computer FROM auth;")

for computer in uniquecomputers:
	print computer
	SQL = "CREATE TABLE %s 
	
	data = computer
	cur.execute(

cur.close()
conn.close()

