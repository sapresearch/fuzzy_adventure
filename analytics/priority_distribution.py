import MySQLdb as mdb
from datetime import datetime
import general_persistence as gp



def transaction_duration(transaction):
	"""
	Based on a list of messages, returns the time elapsed between the first and the last one in seconds.
	"""
	start_date = transaction['start_date']
	end_date = transaction['end_date']
	return (end_date - start_date).total_seconds()


db = mdb.connect(host="localhost", user="root", passwd="nolwen", db="watchTowerSpace")


db.query("""SELECT priority, start_date, end_date FROM transactions""")
rows = db.store_result().fetch_row(0,1)
rows = [row for row in rows if row['end_date'] is not None]

priorities_dist = {}
for row in rows:
	priority = row['priority']
	if priority not in priorities_dist:
		priorities_dist[priority] = [transaction_duration(row)]
	else:
		priorities_dist[priority].append(transaction_duration(row))

gp.dump(priorities_dist, 'out/priority_dist.out')

