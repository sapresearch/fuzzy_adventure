import MySQLdb



def escape_string(string):
	return str(MySQLdb.escape_string(string))
	
	
def camel_case(string):
	return  ' '.join(i.capitalize() for i in string.split(' '))
	
	
def pretty_print_duration(duration):

	days = int(duration / 3600 / 24)
	duration = duration - days * 3600 * 24

	hours = int(duration / 3600)
	duration = duration - hours * 3600

	minutes = int(duration / 60)
	duration = duration - minutes * 60

	seconds = duration
	
	pretty = ""
	if days > 0:
		pretty = "%d day(s) " % days
	if hours > 0 or days > 0:
		pretty += "%d hour(s) " % hours
	if minutes > 0 or hours > 0 or days > 0:
		pretty += "%d minute(s) " % minutes
	if seconds > 0 or minutes > 0 or hours > 0 or days > 0:
		pretty += "%f second(s)" % seconds

	return pretty
	
	
