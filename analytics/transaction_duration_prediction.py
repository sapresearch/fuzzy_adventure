from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import ElasticNet
import MySQLdb
from datetime import *
import numpy as np
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import TanhLayer
import time

import NN_weights_persistence

# Vectorization librairies
import featured_transaction as ft
from sklearn.feature_extraction import DictVectorizer
from scipy.sparse import csr_matrix


def get_transactions(nb_trans):
		
	db = MySQLdb.connect(host="localhost", user="root", passwd="nolwen", db="watchTower")
	db.query("""SELECT *, programmers.name, components.name 
	FROM transactions, programmers, components 
	WHERE programmer_id = programmers.id AND component_id = components.id 
	LIMIT %d""" % nb_trans)
	transactions = db.store_result().fetch_row(0,1)
	db.close()
	
	# Filter the transactions that have no end date. We only need the transactions that we can
	# create a label.
	transactions = [t for t in transactions if t['end_date'] is not None]
	print "\n%d transactions loaded from the database." % len(transactions)

	return transactions
		
	
def transaction_duration(transaction):
	"""
	Based on a list of messages, returns the time elapsed between the first and the last one.
	"""
	start_date = transaction['start_date']
	end_date = transaction['end_date']
	return (end_date - start_date).days + 1

	
def elastic_net(data, targets):
	model = ElasticNet(alpha=1, rho=0.7)
	model.fit(data, targets)
	return model


def ridgeCV(data, targets):
	"""
	Returns a RidgeCV linear model for predictions with alphas [1, 10, 50, 100, 1000]
	Takes the data and the associated targets as arguments.
	"""
	model = RidgeCV(alphas=[1, 10, 50, 100, 1000])
	model.fit(data, targets)
	return model
	
	
def lasso(data, targets):
	"""
	Returns a Lasso linear model for predictions with alpha 0.1
	Takes the data and the associated targets as arguments.
	"""
	model = Lasso(alpha=0.1)
	model.fit(data, targets)
	return model
	
	
def linear_regression(data, targets):
	"""
	Returns a Linear Regression model for predictions.
	Takes the data and the associated targets as arguments.
	"""
	model = LinearRegression()
	model.fit(data, targets)
	return model
	
	
def vectorize_data(transactions):
	"""
	From a list of transctions, returns a 2D array of the featured transactions and an array of 
	the associated targets.
	The features transactions 2D array is of dimension nbTranscations X nbFeatures
	The targets array is of dimension nbTransactions X 1
	"""
	featured_transactions = []
	targets = []

	for transaction in transactions:
		features = ft.FeaturedTransaction(transaction).as_dict()

		# Add the array of features of that transaction to the set
		featured_transactions.append(features)
		targets.append(transaction_duration(transaction))
	
	
	#featured_transactions = np.array(featured_transactions)
	targets = np.array(targets)
	vec = DictVectorizer()
	featured_transactions = vec.fit_transform(featured_transactions)

	
	return featured_transactions, targets
	

def mean_squared_error(test_data, test_targets):
	"""
	Returns the mean squared error of a model's predictions vs the real targets.
	"""
	squared = ((test_data - test_targets)**2)
	mse = (np.mean(squared))**0.5
	
	return mse
	

def score(model, test_data, test_targets):
	"""
	Returns a model's score of its predictions vs the real targets
	"""
	return model.score(test_data, test_targets)
	
	
def model_predictions(model, test_data):
	"""
	Returns an array of a model's predictions
	"""
	return model.predict(test_data)
	
	
def negative_predictions(predictions):
	"""
	Returns an array of the negative value predictions. This is informative. Besides knowing
	how many were negatives there is no use for this function.
	"""
	return predictions[predictions < 0]


def main(nb_transactions):

	
	transactions = get_transactions(nb_transactions)

	featured_transactions, targets = vectorize_data(transactions)
	featured_transactions_as_array = featured_transactions.todense()


	print "\n%d featured transactions" % featured_transactions.shape[0]
	print "%d features for a transaction" % featured_transactions.shape[1]


	size = 0.8
	training_size = int(len(featured_transactions_as_array) * size)
	test_size = len(featured_transactions_as_array) - training_size
	training_data = csr_matrix(featured_transactions_as_array[:training_size])
	training_targets = targets[:training_size]


	print "\n%d transactions in the training set" % len(training_data.toarray())

	test_data = csr_matrix(featured_transactions_as_array[-test_size:])
	test_targets = targets[-test_size:]
	print "%d transactions in the test set" % len(test_data.toarray())

	
	model = elastic_net(training_data.todense(), training_targets)
	print type(model), '\n'
	
	start = time.time()
	print "Took %s seconds to complete with %d training examples" %(time.time() - start, len(training_data.toarray()))
	print "\nScore: %f" % score(model, test_data, test_targets)
	predictions = model_predictions(model, test_data)
	mse = mean_squared_error(predictions, test_targets)
	print "\nMean Squared Error = %f." % (mse)
	neg = negative_predictions(predictions)
	print "\n%d negative values in predictions" % len(neg)

	max_duration = np.amax(training_targets)
	random_prediction = np.random.gamma(5, 1, size = len(test_targets))
	mse_bench = mean_squared_error(random_prediction, test_targets)
	print "\nBench using random as predicted value for all test set = %f" % mse_bench

	return mse

#ridge_model = ridgeCV(training_data, training_targets)
#print "Took %s seconds to complete ridge model with %d training examples" %(time.time() - start, len(training_data.toarray()))
#lasso_model = lasso(training_data, training_targets)
#linear_regression_model = linear_regression(training_data, training_targets)




main(10000)

"""
print "\n", "~" * 50
print "\tNEURAL NETWORK"
print "~" * 50


f = file('result.txt','a')
start = time.time()
net = buildNetwork(72, 3, 1, hiddenclass = TanhLayer, bias = True)
ds = SupervisedDataSet(72, 1)


for i in range(len(training_data)):
	ds.addSample(training_data[i], training_targets[i])


trainer = BackpropTrainer(net, ds)
print trainer.trainUntilConvergence()

NN_weights_persistence.dump(net.params)

#f.write("Predicted value: %f" % net.activate(test_data[0]))
#f.write("Real value:" % test_targets[0])
f.write("NN took %f seconds with a trainUntilConvergence()\n" % (time.time()-start))
f.close()
"""