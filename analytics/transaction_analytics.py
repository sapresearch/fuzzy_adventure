import MySQLdb
import time
from datetime import datetime
from datetime import timedelta
import copy



def load_db(sql):
	db = MySQLdb.connect(host="localhost", user="root", passwd="", db="batcave_beta")
	db.query(sql)
	trans = db.store_result().fetch_row(0)
	db.close()
	return trans

all_messages = load_db("""SELECT * FROM messages""")

class OpenTransactions():

	def __init__(self, all_trans):
		self.open_count, self.close_count, self.start_date = self.counts(all_trans)

	def counts(self, all_trans):
		all_trans = sorted(all_trans, key=lambda trans: trans.start)
		first = all_trans[0].start
		last = all_trans[-1].start
		open_count = {}
		close_count = {}
		for t in all_trans:
			open_count[t.start] = 0.
			close_count[t.start] = 0.

		total = 0.
		for t in all_trans:
			total += 1.
			open_count[t.start] = total

		total = 0.
		all_trans = sorted(all_trans, key=lambda trans: trans.end)
		for t in all_trans:
			total += 1.
			end_time = copy.copy(t.end)
			if end_time < last:
				while end_time not in close_count:
					end_time += timedelta(days=1)
			if end_time in close_count:
				close_count[end_time] = total

		#print "Open count: " + str(open_count)
		#print "Close count: " + str(close_count)
		return open_count, close_count, first

	def open(self, date):
		open = self.open_count[date]
		print open
		close = self.close_count[date] - self.close_count[self.start_date]
		print close
		total = open - close
		return total


class Transaction():

	previous_start = datetime.date(datetime(2012, 3, 3))

	def __init__(self, params, previous_transaction=None):
		self.priority = params[9]
		self.first_message = Message.find(params[14])
		self.messages = Message.message_chain(self.first_message)
		self.start = self.get_start(previous_transaction)
		self.end = self.get_end()
		Transaction.previous_start = self.start

	@classmethod
	def all(self):
		all_params = load_db("""SELECT * FROM transactions""")#[0:5000]
		all_trans = []
		for p in all_params:
			t = Transaction(p)
			all_trans.append(t)
		return all_trans
	
	def get_start(self, previous_transaction):
		if self.first_message == None:
			return Transaction.previous_start
		return self.first_message[3]
	
	def get_end(self):
		if self.first_message == None:
			return Transaction.previous_start
		return self.messages[-1][3]
	
	def duration(self):
		if self.end == None or self.start == None:
			return 0.
		dur = self.end - self.start
		days = dur.days
		return days
	
	@classmethod
	def avg_duration(self, filter=['Low', 'Medium', 'High', 'Very high']):
		all_trans = self.all()
		total = 0.
		total_count = 0.
		for t in all_trans:
			if t.priority in filter:
				total += t.duration()
				total_count += 1.
		print "Number of type: " + str(total_count)
		avg = total/total_count
		return avg

class Message():

	@classmethod
	def all(self):
		return all_messages
	
	@classmethod
	def message_chain(self, message):
		if message == None:
			return []
		next_message_id = message[0]
		messages = Message.all()
		chain = []
		for m in messages:
			if m[0] == next_message_id:
				chain.append(m)
				next_message_id = m[5]
				if next_message_id == None:
					return chain
	
	@classmethod
	def find(self, message_id):
		messages = self.all()
		for m in messages:
			if m[0] == message_id:
				return m


s = time.time()
params = Transaction.all()
open_ = OpenTransactions(params)
print params[5000].start
print open_.open(params[5000].start)
#for prior in ['Low', 'Medium', 'High', 'Very high']:
	#print str(prior) + ': ' + str(Transaction.avg_duration([prior]))
print "Duration: " + str(time.time() - s)
