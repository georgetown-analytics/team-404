import psycopg2

conn = psycopg2.connect(
	host="team404.czuxenny2zus.us-east-1.rds.amazon.aws.com",
	port=5439,
	dbname="weirdo",
	user="pcgeller"
)
cur = conn.cursor()

uniquecomputers = cur.execute("SELECT DISTINCT computer FROM auth;")

for computer in uniquecomputers:
	print computer
	SQL = "CREATE TABLE %s 
	
	data = computer
	cur.execute(

cur.close()
conn.close()

