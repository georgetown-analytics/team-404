import psycopg2
conn = psyopg2.connect("dbname=weirdo user=pcgeller")
cur = conn.cursor()

cur.execute()


cur.close()
conn.close()

