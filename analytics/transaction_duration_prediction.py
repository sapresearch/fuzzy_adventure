from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import RidgeCV
import MySQLdb
from datetime import *
import numpy as np
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import TanhLayer
import time

import NN_weights_persistence



priorities = ['Very high', 'High', 'Medium', 'Low']
statuses = ['Confirmed', \
'Completed', \
'In Process', \
'New', \
'Author Action', \
'Completed for Author', \
'Partner Action']




def get_base_informations():
	"""
	Obtain the basic informations needed from the database for the duration prediction
	"""
	db = MySQLdb.connect(host="localhost", user="root", passwd="", db="batcave")

	db.query("""SELECT * FROM transactions""")
	transactions = db.store_result().fetch_row(0)
	print "\n%d transactions loaded from the database." % len(transactions)

	db.query("""SELECT * FROM messages""")
	messages = db.store_result().fetch_row(0)

	db.query("""SELECT * FROM components""")
	raw_components = db.store_result().fetch_row(0)
	components = [component[1] for component in raw_components]
	

	db.close()
	
	return transactions, messages, components
	
	
def stem_components(components):
	"""
	Return a list containing all the components stem.
	A component stem is the top hierarchy for that component's family.
	e.g. SRD-CC-IAM is SRD
	"""
	component_set = set([component.split('-')[0] for component in components])
	print "%d component families in the database" % len(component_set)
	return list(component_set)
		
		
def vectorize_priority(transaction):
	"""
	Return a np array containing all zeros except for the transaction's priority.
	This array act as a classifier. Only the priority of the transaction is equal to one,
	all other priorities are zeros.
	"""
	vector = np.zeros(len(priorities))
	priority = transaction[9]
	for i in range(len(priorities)):
		vector[i] = int(priorities[i] == priority)
	return vector


def vectorize_status(transaction):
	"""
	Return a np array containing all zeros except for the transaction's status.
	This array act as a classifier. Only the status of the transaction is equal to one,
	all other statuses are zeros.
	"""
	vector = np.zeros(len(statuses))
	status = transaction[11]
	for i in range(len(statuses)):
		vector[i] = int(statuses[i] == status)
	return vector
		
		
def vectorize_component(transaction):
	"""
	Returns a np array containing all zeros except for the transaction's component.
	This array act as a classifier. Only the component of the transaction is equal to one,
	all other components are zeros.
	"""
	vector = np.zeros(len(stemmed_components))
	component_id = transaction[12] - 1
	#raw_input(component_id)
	component = components[component_id]

	#raw_input(component)
	component = component.split('-')[0]
	#raw_input(component)
	for i in range(len(stemmed_components)):
		vector[i] = int(stemmed_components[i] == component)
	return vector
		
		
def build_transaction_features(transaction):
	"""
	Build the transaction's features. This is where new features must be added.
	At the moment, priority, status and component are beeing considered.
	"""
	features = np.array([])
	features = np.append(features, vectorize_priority(transaction))
	features = np.append(features, vectorize_status(transaction))
	features = np.append(features, vectorize_component(transaction))
	return features

	
def get_message_chain(transaction):
	"""
	Returns all the messages associated with a transaction as an array
	"""
	messages_chain = []
	first_message_id = int(transaction[14])
	if first_message_id == -1:
		return messages_chain
	
	next_message_id = first_message_id
	while next_message_id is not None:
		next_message = messages[next_message_id - 1]
		messages_chain.append(next_message)
		next_message_id = next_message[5]
		
	return messages_chain


def get_messages_time_span(messages):
	"""
	Based on a list of messages, returns the time elapsed between the first and the last one.
	"""
	first_message = messages[0]
	last_message = messages[-1]
	return (last_message[3] - first_message[3]).days + 1

	
def ridgeCV(data, targets):
	"""
	Returns a RidgeCV linear model for predictions with alphas [1, 10, 20, 30, 35]
	Takes the data and the associated targets as arguments.
	"""
	model = RidgeCV(alphas=[1, 10, 30, 60, 100])
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
	
	
def extract_data_from_transactions(transactions):
	"""
	From a list of transctions, returns a 2D array of the featured transactions and an array of 
	the associated targets.
	The features transactions 2D array is of dimension nbTranscations X nbFeatures
	The targets array is of dimension nbTransactions X 1
	"""
	featured_transactions = []
	targets = []
	#transactions = [t for t in transactions if len(get_message_chain(t)) > 0]

	for transaction in transactions:
		features = build_transaction_features(transaction)
		
		# Add the array of features of that transaction to the test set
		featured_transactions.append(np.array(features))
		targets.append(get_messages_time_span(get_message_chain(transaction)))
		
	featured_transactions = np.array(featured_transactions)
	targets = np.array(targets)
	
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
	
	
def predictions(model, test_data):
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


transactions, messages, components = get_base_informations()
stemmed_components = stem_components(components)
# Filter the transactions that have no messages.
# This is done only because the messages are used to determine the duration of a transaction
# If we had any other way of assuming the duration, we wouldn't have to filter.
transactions = [t for t in transactions if len(get_message_chain(t)) > 0]

featured_transactions, targets = extract_data_from_transactions(transactions)

size = 0.7
training_size = int(len(featured_transactions) * size)
test_size = len(featured_transactions) - training_size
training_data = featured_transactions[:training_size]
training_targets = targets[:training_size]
print "\n%d transactions in the training set" % len(training_data)

test_data = featured_transactions[-test_size:]
test_targets = targets[-test_size:]
print "%d transactions in the test set" % len(test_data)

"""
ridge_model = ridgeCV(training_data, training_targets)
lasso_model = lasso(training_data, training_targets)
linear_regression_model = linear_regression(training_data, training_targets)

print "\nRidge score: %f" % score(ridge_model, test_data, test_targets)
print "Lasso score: %f" % score(lasso_model, test_data, test_targets)
print "Linear score: %f" % score(linear_regression_model, test_data, test_targets)

ridge_predictions = predictions(ridge_model, test_data)
lasso_predictions = predictions(lasso_model, test_data)
linear_regression_predictions = predictions(linear_regression_model, test_data)

	
ridge_mse = mean_squared_error(ridge_predictions, test_targets)
lasso_mse = mean_squared_error(lasso_predictions, test_targets)
linear_regression_mse = mean_squared_error(linear_regression_predictions, test_targets)

print "\nMean Squared Error using ridge = %f. Best alpha is %f" % (ridge_mse, ridge_model.best_alpha)
print "Mean Squared Error using lasso = %f" % lasso_mse
print "Mean Squared Error using linear regression = %f" % linear_regression_mse



neg_ridge = negative_predictions(ridge_predictions)
print "\n%d negative values in ridge predictions" % len(neg_ridge)
neg_lasso = negative_predictions(lasso_predictions)	
print "%d negative values in lasso predictions" % len(neg_lasso)
neg_linear = negative_predictions(linear_regression_predictions)	
print "%d negative values in linear regression predictions" % len(neg_linear)


ridge_mse_bench = mean_squared_error(np.ones(len(test_data)), test_targets)
lasso_mse_bench = mean_squared_error(np.ones(len(test_data)), test_targets)
lin_reg_mse_bench = mean_squared_error(np.ones(len(test_data)), test_targets)
	
print "\nOnes bench using ridge = %f" % ridge_mse_bench
print "Ones bench using lasso = %f" % lasso_mse_bench
print "Ones bench using linear regression = %f" % lin_reg_mse_bench
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
