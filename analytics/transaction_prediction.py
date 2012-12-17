from transaction_analytics import Transaction, OpenTransactions
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from numpy import *
import math
from datetime import datetime
import time

class TransactionPrediction():

	#def duration():

	@classmethod
	def training_data(self):
		trans = Transaction.all()
		very_high, high, medium, low = OpenTransactions(trans, ['Very high']), OpenTransactions(trans, ['High']), OpenTransactions(trans, ['Medium']), OpenTransactions(trans, ['Low'])

		priorities = {'Very high':1., 'High':0.67, 'Medium':0.33, 'Low':0.}
		data = []
		targets = []

		# Only select ones after August
		august = datetime.date(datetime(2012, 2, 1))
		trans = filter(lambda p: p.start >= august, trans)
		print "Training items: " + str(len(trans))
		for t in trans:
			t_data = []
			t_data.append(very_high.open(t.start))
			t_data.append(very_high.open(t.start) ** 2)
			t_data.append(high.open(t.start))
			t_data.append(high.open(t.start) ** 2)
			t_data.append(medium.open(t.start))
			t_data.append(medium.open(t.start) ** 2)
			t_data.append(low.open(t.start))
			t_data.append(low.open(t.start) ** 2)
			priority = priorities[t.priority]
			t_data.append(priority)
			data.append(t_data)
			targets.append(t.duration())

		
		# Scale each feature.
		# Find the max item fo reach feature and scale.
		num_of_features = len(data[0])
		print "Features: " + str(num_of_features)
		for i in range(num_of_features):
			max = 0.
			for d in data:
				max = d[i] if d[i] > max else max
			for j,d in enumerate(data):
				data[j][i] = round((d[i]/max), 3)
				
		# Change lists to numpy arrays.
		for i,d in enumerate(data):
			data[i] = array(d)

		return data, targets
	
	@classmethod
	def duration(self):
		data, targets = TransactionPrediction.training_data()
		test_d, test_t = data[2::3], targets[2::3]
		data = data[0::3] + data[1::3]
		targets = targets[0::3] + targets[1::3]
		print "Training items: " + str(len(data))
		#model = GradientBoostingRegressor(n_estimators=10, learn_rate=1.0, max_depth=10, random_state=0, loss='ls')
		model = LinearRegression(normalize=True)
		model = model.fit(data, targets)
		print model

		preds = model.predict(test_d)
		new = []
		for i in preds:
			if i < 0.:
				new.append(0.)
			else:
				new.append(round(i))
		preds = array(new)
		print [round(i, 1) for i in preds[40:200]]
		print "--------------"
		print targets[40:200]
		print "--------------"
		cost = mean(((preds - test_t) ** 2) ** 0.5)
		print "Avg error: " + str(cost)
		preds = zeros(len(test_d))
		cost = mean(((preds - test_t) ** 2) ** 0.5)
		print "Benchmark avg error: " + str(cost)
		return cost

s = time.time()
#TransactionPrediction.training_data()
print TransactionPrediction.duration()
print "Duration: " + str(time.time() - s)
