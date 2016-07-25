month_number = []
start_time = 1
for i in range (6):
	month_label = 1
	end_time = start_time + 2591999
	i = [month_label,start_time,end_time]
	start_time = end_time + 1
	month_number.append(i)

	
def Update_month(table):
	for x in month_number:
		print ('UPDATE %s SET %s.month = \'%s\' WHERE %s.tstamp >= %s AND %s.tstamp <= %s' % (table, table, x[0], table, x[1], table, x[2]))

if __name__ == '__main__':
	Update_month('table')