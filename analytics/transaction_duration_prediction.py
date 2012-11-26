from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import RidgeCV
import MySQLdb
from datetime import *
import numpy

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
	print "%d transactions loaded from the database." % len(transactions)

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
	Return a numpy array containing all zeros except for the transaction's priority.
	This array act as a classifier. Only the priority of the transaction is equal to one,
	all other priorities are zeros.
	"""
	vector = numpy.zeros(len(priorities))
	priority = transaction[9]
	for i in range(len(priorities)):
		vector[i] = int(priorities[i] == priority)
	return vector


def vectorize_status(transaction):
	"""
	Return a numpy array containing all zeros except for the transaction's status.
	This array act as a classifier. Only the status of the transaction is equal to one,
	all other statuses are zeros.
	"""
	vector = numpy.zeros(len(statuses))
	status = transaction[11]
	for i in range(len(statuses)):
		vector[i] = int(statuses[i] == status)
	return vector
		
		
def vectorize_component(transaction):
	"""
	Returns a numpy array containing all zeros except for the transaction's component.
	This array act as a classifier. Only the component of the transaction is equal to one,
	all other components are zeros.
	"""
	vector = numpy.zeros(len(stemmed_components))
	component_id = transaction[12]
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
	features = numpy.array([])
	features = numpy.append(features, vectorize_priority(transaction))
	features = numpy.append(features, vectorize_status(transaction))
	features = numpy.append(features, vectorize_component(transaction))
	return features

	
def get_message_chain(transaction):
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
	first_message = messages[0]
	last_message = messages[-1]
	return (last_message[3] - first_message[3]).days + 1

	
def ridgeCV(data, targets):
	model = RidgeCV(alphas=[1, 10, 20, 30, 35])
	model.fit(data, targets)
	return model
	
def lasso(data, targets):
	model = Lasso(alpha=0.1)
	model.fit(data, targets)
	return model
	
def linear_regression(data, targets):
	model = LinearRegression()
	model.fit(data, targets)
	return model
	
def extract_data_from_transactions(transactions):
	featured_transactions = []
	targets = []
	#transactions = [t for t in transactions if len(get_message_chain(t)) > 0]

	for transaction in transactions:
		features = build_transaction_features(transaction)
		
		# Add the array of features of that transaction to the test set
		featured_transactions.append(numpy.array(features))
		targets.append(get_messages_time_span(get_message_chain(transaction)))
		
	featured_transactions = numpy.array(featured_transactions)
	targets = numpy.array(targets)
	
	return featured_transactions, targets
	
transactions, messages, components = get_base_informations()
stemmed_components = stem_components(components)
# Filter the transactions that have no messages.
# This is done only because the messages are used to determine the duration of a transaction
transactions = [t for t in transactions if len(get_message_chain(t)) > 0]

featured_transactions, targets = extract_data_from_transactions(transactions)

size = 9
training_data = [featured_transactions[i] for i in range(len(featured_transactions)) if (i % size != 0)]
training_targets = [targets[i] for i in range(len(targets)) if (i % size != 0)]
print "%d transactions in the training set" % len(training_data)

test_data = [featured_transactions[i] for i in range(len(featured_transactions)) if (i % size == 0)]
test_targets = [targets[i] for i in range(len(targets)) if (i % size == 0)]
print "%d transactions in the test set" % len(test_data)


ridge_model = ridgeCV(training_data, training_targets)
lasso_model = lasso(training_data, training_targets)
linear_regression_model = linear_regression(training_data, training_targets)

ridge_predictions = ridge_model.predict(test_data)
lasso_predictions = lasso_model.predict(test_data)
linear_regression_predictions = linear_regression_model.predict(test_data)

i = 0
neg_ridge = []
for prediction in ridge_predictions:
	if prediction < 0:
		neg_ridge.append(prediction)
		i += 1

print "%d negative values in ridge predictions" % i

neg_lasso = []		
i = 0
for prediction in lasso_predictions:
	if prediction < 0:
		neg_lasso.append(prediction)
		i += 1
		
print "%d negative values in lasso predictions" % i

neg_linear = []	
i = 0	
for prediction in linear_regression_predictions:
	if prediction < 0:
		neg_linear.append(prediction)
		i += 1
		
print "%d negative values in linear regression predictions" % i
		
		
ridge_squared_error_sum = 0
lasso_squared_error_sum = 0
linear_reg_squared_error_sum = 0
zeros_bench_sum = 0
for i in range(len(test_data)):
	ridge_squared_error_sum = (ridge_predictions[i] - test_targets[i])**2
	lasso_squared_error_sum = (lasso_predictions[i] - test_targets[i])**2
	linear_reg_squared_error_sum = (linear_regression_predictions[i] - test_targets[i])**2

print "Mean Squared Error using ridge = %f. Best alpha is %f" % (numpy.mean(ridge_squared_error_sum)**0.5, ridge_model.best_alpha)
print "Mean Squared Error using lasso = %f" % numpy.mean(lasso_squared_error_sum)**0.5
print "Mean Squared Error using linear regression = %f" % numpy.mean(linear_reg_squared_error_sum)**0.5

for i in range(len(test_data)):
	ridge_squared_error_sum = (ridge_predictions[i])**2
	lasso_squared_error_sum = (lasso_predictions[i])**2
	linear_reg_squared_error_sum = (linear_regression_predictions[i])**2
	
print "Zeros bench using ridge = %f" % numpy.mean(ridge_squared_error_sum)**0.5
print "Zeros bench using lasso = %f" % numpy.mean(lasso_squared_error_sum)**0.5
print "Zeros bench using linear regression = %f" % numpy.mean(linear_reg_squared_error_sum)**0.5



