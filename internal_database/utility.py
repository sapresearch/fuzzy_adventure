import MySQLdb



def escape_string(string):
	return str(MySQLdb.escape_string(string))
	
	
def camel_case(string):
	return  ' '.join(i.capitalize() for i in string.split(' '))
	
	
	
