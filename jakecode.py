import psycopg2
#from auth_js import connection_string_js

# def connect_db(connection_data):
# 	try:
# 		conn = psycopg2.connect(connection_data)
# 	except:
# 		print ("\n_________CONNECTION FAILURE_________\n")
# 	cur = conn.cursor()
# 	return cur

This generates a list of lists. The sub-lists include three items: a number 1-180,
# representing 180 consecutive 24/hr periods (this is six months), the
# timestamps at the begining of the 24/hr period, and the timestamp at the end of the 24/hr period.
def time_converter_day():
	day_number = []
	start_time = 1
	for i in range (180):
		day_label = 1
		end_time = start_time + 86399 #number of seconds in 24 hours
		i = [day_label,start_time,end_time]
		start_time = end_time + 1
		day_number.append(i)
	return day_number

# This is same as time_converter_day() only for a month long period.
def time_converter_month():
	month_number = []
	start_time = 1
	for i in range (6):
		month_label = 1
		end_time = start_time + 2591999 #number of seconds in 30 days
		i = [month_label,start_time,end_time]
		start_time = end_time + 1
		month_number.append(i)
	return month_number

# SQL query to create new column in table, acepts arguments
# for table name, column name, and data type. Can use this to insert day
# and month columns for one or several tables.
def insert_column(cur,table,column,type):
	cur.execute("""ALTER TABLE %s ADD COLUMN %s %s""" % (table,column,type))

# Update day and month column based on timestamps. This loops through the month_number list generated above, and generates queries to update the month column based on the calculated timestamp parameters.
# With the string input filled in, the query should read: UPDATE <table> SET <table>.month = <first value in sub-list in month_number> WHERE <table>.tstamp >= <second value in sub-list in month_number> AND <table>.tstamp <= <third value in sub-list in month_number>
def Update_month(table):
	for x in month_number:
		cur.execute("""UPDATE %s SET %s.month = %s WHERE %s.tstamp >= %s AND %s.tstamp <= %s""" % (table, table, x[0], table, x[1], table, x[2]))

# SQL query to creat table based on month designation. Can use this to break
# down large tables into tables based on month to make them smaller and easier to work with.
def generate_table_by_select(table, month, new_table):
	cur.execute(command)


def disconnect_db():
	cur.close()
	connx.close()

if __name__ == '__main__':
	connect_db(connection_string_js)
	time_converter_day()
	time_converter_month()
	#insert_column('redteam','day','INT')
	#insert_column('redteam','month','INT')
	disconnect_db()
