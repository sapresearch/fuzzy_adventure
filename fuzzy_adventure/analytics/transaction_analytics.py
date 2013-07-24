import MySQLdb
import time
from datetime import datetime
from datetime import timedelta
import copy



def load_db(sql):
	s = time.time()
	db = MySQLdb.connect(host="localhost", user="root", passwd="", db="batcave_beta")
	db.query(sql)
	trans = db.store_result().fetch_row(0)
	db.close()
	print "In load DB. Duration: " + str(time.time() - s) + ". Query: " + str(sql)
	all_t = {}
	for t in trans:
		all_t[t[0]] = t
	return all_t

all_messages = load_db("""SELECT * FROM messages""")

class OpenTransactions():

	def __init__(self, all_trans, priorities=None):
		self.open_count, self.close_count, self.start_date, self.end_date = self.counts(all_trans, priorities)

	def counts(self, all_trans, priorities=None):
		if priorities != None:
			all_trans = filter(lambda t: t.priority in priorities, all_trans)
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
		return open_count, close_count, first, last

	def open(self, date):
		if date not in self.open_count:
			if date < self.end_date:
				while date not in self.open_count:
					date += timedelta(days=1)
			else:
				date = self.end_date
		open = self.open_count[date]
		close = self.close_count[date] - self.close_count[self.start_date]
		total = open - close
		return total


class Transaction():

	previous_start = datetime.date(datetime(2012, 3, 3))

	def __init__(self, params, filtered_messages, previous_transaction=None):
		self.priority = params[9]
		message_id = params[14]
		self.first_message = Message.find(message_id)
		self.messages = Message.message_chain(self.first_message)
		self.start = self.get_start(previous_transaction)
		self.end = self.get_end()
		Transaction.previous_start = self.start

	@classmethod
	def all(self):
		filtered_messages = all_messages
		all_params = load_db("""SELECT * FROM transactions""")
		all_trans = []
		s = time.time()
		for p in all_params.values():
			t = Transaction(p, filtered_messages)
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
	
	@classmethod
	def avg_duration_by_others_open(self, all_trans, _open):
		groups = {}
		for i in range(30):
			groups[(i*5)] = []
		for t in all_trans:
			duration = round((t.duration() * 2), -1)/2
			if duration in groups:
				others_open = _open.open(t.start)
				groups[duration].append(others_open)
		for k,v in groups.items():
			length = float(len(v))
			avg_open = sum(v)/length if length > 0 else 0
			avg_open = round(avg_open)
			groups[k] = avg_open
		groups = sorted(groups.iteritems())
		return groups

class Message():

	@classmethod
	def all(self):
		return all_messages
	
	@classmethod
	def message_chain(self, message):
		if message == None:
			return []
		next_message_id = message[0]
		chain = []
		while next_message_id != None:
			next_message = all_messages[next_message_id]
			chain.append(next_message)
			next_message_id = next_message[5]
		return chain
		#for m in all_messages:
			#if m[0] == next_message_id:
				#chain.append(m)
				#next_message_id = m[5]
				#if next_message_id == None:
					#return chain
	
	@classmethod
	def find(self, message_id):
		messages = all_messages#Message.all
		if message_id in messages:
			return messages[message_id]
		else:
			return None
		#for m in messages:
			#if m[0] == message_id:
				#messages.remove(m)
				#return m, messages


#Transaction.all()
#s = time.time()
#params = Transaction.all()
#open_ = OpenTransactions(params, ['Very high', 'High'])
#august = datetime.date(datetime(2012, 8, 1))
#params = filter(lambda p: p.start >= august, params)
#print len(params)
#print Transaction.avg_duration_by_others_open(params, open_)
#for prior in ['Low', 'Medium', 'High', 'Very high']:
	#print str(prior) + ': ' + str(Transaction.avg_duration([prior]))
#print "Duration: " + str(time.time() - s)
