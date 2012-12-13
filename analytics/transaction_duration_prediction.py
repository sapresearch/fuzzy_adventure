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

# Vectorization librairies
import featured_transaction as ft
from sklearn.feature_extraction import DictVectorizer
from scipy.sparse import csr_matrix


priorities = []
statuses = []
programmers = []
contract_priorities = []
products = []



def get_base_informations():
	global priorities, statuses, programmers, contract_priorities, products
	"""
	Obtain the basic informations needed from the database for the duration prediction
	"""
	db = MySQLdb.connect(host="localhost", user="root", passwd="nolwen", db="watchTower")

	db.query("""SELECT *, programmers.name, components.name 
	FROM transactions, programmers, components 
	WHERE programmer_id = programmers.id AND component_id = components.id 
	LIMIT 100000""")
	transactions = db.store_result().fetch_row(0,1)

	# Filter the transactions that have no end date.
	transactions = [t for t in transactions if t['end_date'] is not None]
	print "\n%d transactions loaded from the database." % len(transactions)

	db.query("""SELECT * FROM components""")
	rows = db.store_result().fetch_row(0,1)
	#components = [row['name'] for row in rows]
	components = list(set([transaction['components.name'] for transaction in transactions]))
	print "%d components" % len(components)
	programmers = list(set([transaction['programmers.name'] for transaction in transactions]))
	print "%d programmers" % len(programmers)
	

	priorities = list(set([transaction['priority'] for transaction in transactions]))
	print "%d priority levels" % len(priorities)
	statuses = list(set([transaction['status'] for transaction in transactions]))
	print "%d different status" % len(statuses)
	contract_priorities = list(set([transaction['contract_priority'] for transaction in transactions]))
	print "%d contract priority levels" % len(contract_priorities)
	products = list(set([transaction['product'] for transaction in transactions]))
	print "%d different products" % len(products)
	db.close()
	
	return transactions, components
	

def stem_components(components):
	"""
	Return a list containing all the components stem.
	A component stem is the top hierarchy for that component's family.
	e.g. SRD-CC-IAM is SRD
	"""
	component_set = set([component.split('-')[0] for component in components])
	print "%d component families in the database" % len(component_set)
	return list(component_set)
		
	
def vectorize_programmer(transaction):
	"""
	Return a np array containing all zeros except for the transaction's programmer.
	This array act as a classifier. Only the programmer of the transaction is equal to one,
	all other programmers are zeros.
	"""
	vector = np.zeros(len(programmers))
	programmer = transaction['priority']
	for i in range(len(programmers)):
		vector[i] = int(programmers[i] == programmer)
	return vector


def vectorize_priority(transaction):
	"""
	Return a np array containing all zeros except for the transaction's priority.
	This array act as a classifier. Only the priority of the transaction is equal to one,
	all other priorities are zeros.
	"""

	vector = np.zeros(len(priorities))
	priority = transaction['priority']
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
	status = transaction['status']
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
	component_id = transaction['component_id'] - 1

	component = components[component_id]


	component = component.split('-')[0]

	for i in range(len(stemmed_components)):
		vector[i] = int(stemmed_components[i] == component)
	return vector
		

def vectorize_contract_priority(transaction):
	"""
	Return a np array containing all zeros except for the transaction's contract priorities.
	This array act as a classifier. Only the contract priority of the transaction is equal to one,
	all other contract priorities are zeros.
	"""
	vector = np.zeros(len(contract_priorities))
	contract_priority = transaction['contract_priority']
	for i in range(len(contract_priorities)):
		vector[i] = int(contract_priorities[i] == contract_priority)
	return vector
	
	
def vectorize_product(transaction):
	"""
	Return a np array containing all zeros except for the transaction's product.
	This array act as a classifier. Only the product of the transaction is equal to one,
	all other contract products are zeros.
	"""
	vector = np.zeros(len(products))
	product = transaction['product']
	for i in range(len(products)):
		vector[i] = int(products[i] == product)
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
	features = np.append(features, vectorize_programmer(transaction))
	features = np.append(features, vectorize_contract_priority(transaction))
	features = np.append(features, vectorize_product(transaction))
	
	len(features)
	return features


def transaction_duration(transaction):
	"""
	Based on a list of messages, returns the time elapsed between the first and the last one.
	"""
	start_date = transaction['start_date']
	end_date = transaction['end_date']
	return (end_date - start_date).days + 1

	
def ridgeCV(data, targets):
	"""
	Returns a RidgeCV linear model for predictions with alphas [1, 10, 50, 100, 1000]
	Takes the data and the associated targets as arguments.
	"""
	model = RidgeCV(alphas=[1, 10, 1000])
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

	nb_transactions = len(transactions)
	modulo = nb_transactions / 100

	for transaction in transactions:
		#features = build_transaction_features(transaction)
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


transactions, components = get_base_informations()
#stemmed_components = stem_components(components)

featured_transactions, targets = extract_data_from_transactions(transactions)
featured_transactions_as_array = featured_transactions.todense()


print "\n%d featured transactions" % featured_transactions.shape[0]
print "%d features for a transaction" % featured_transactions.shape[1]


size = 0.7

training_size = int(len(featured_transactions_as_array) * size)
test_size = len(featured_transactions_as_array) - training_size

training_data = csr_matrix(featured_transactions_as_array[:training_size])
training_targets = targets[:training_size]


print "\n%d transactions in the training set" % len(training_data.toarray())

test_data = csr_matrix(featured_transactions_as_array[-test_size:])
test_targets = targets[-test_size:]
print "%d transactions in the test set" % len(test_data.toarray())

start = time.time()
ridge_model = ridgeCV(training_data, training_targets)
print "Took %s seconds to complete ridge model with %d training examples" %(time.time() - start, len(training_data.toarray()))
#lasso_model = lasso(training_data, training_targets)
#linear_regression_model = linear_regression(training_data, training_targets)

print "\nRidge score: %f" % score(ridge_model, test_data, test_targets)
#print "Lasso score: %f" % score(lasso_model, test_data, test_targets)
#print "Linear score: %f" % score(linear_regression_model, test_data, test_targets)

ridge_predictions = predictions(ridge_model, test_data)
#lasso_predictions = predictions(lasso_model, test_data)
#linear_regression_predictions = predictions(linear_regression_model, test_data)

	
ridge_mse = mean_squared_error(ridge_predictions, test_targets)
#lasso_mse = mean_squared_error(lasso_predictions, test_targets)
#linear_regression_mse = mean_squared_error(linear_regression_predictions, test_targets)

print "\nMean Squared Error using ridge = %f. Best alpha is %f" % (ridge_mse, ridge_model.best_alpha)
#print "Mean Squared Error using lasso = %f" % lasso_mse
#print "Mean Squared Error using linear regression = %f" % linear_regression_mse



neg_ridge = negative_predictions(ridge_predictions)
print "\n%d negative values in ridge predictions" % len(neg_ridge)
#neg_lasso = negative_predictions(lasso_predictions)	
#print "%d negative values in lasso predictions" % len(neg_lasso)
#neg_linear = negative_predictions(linear_regression_predictions)	
#print "%d negative values in linear regression predictions" % len(neg_linear)


mse_bench = mean_squared_error(np.ones(len(test_data.toarray())), test_targets)
print "\nBench using 1 as predicted value for all test set = %f" % mse_bench



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