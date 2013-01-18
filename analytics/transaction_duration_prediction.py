# Scikit Learn Librairies (Linear Models)
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import ElasticNet
from sklearn.svm import SVR

# Pybrain Librairies (NN)
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import TanhLayer

# Misc
import MySQLdb
from datetime import *
import numpy as np
import time
import general_persistence
import random
from data import Population

# Vectorization librairies
import featured_transaction as ft
from sklearn.feature_extraction import DictVectorizer
from scipy.sparse import csr_matrix

all_transactions = []
def get_transactions(nb_trans):
    global all_transactions

    if len(all_transactions) == 0:
        db = MySQLdb.connect(host="localhost", user="root", passwd="nolwen", db="watchTowerSpace")

        # Put all the transactions in memory. This could be an issue with bigger data
        start = time.time()
        db.query("""SELECT *, programmers.name, components.name 
        FROM transactions, programmers, components 
        WHERE programmer_id = programmers.id AND component_id = components.id""")
        all_transactions = db.store_result().fetch_row(0,1) # Rows are returned as dictionnary [column name, value]
        print "\n%-60s | %-s" % ("Importing all transactions from the database", pretty_print_duration(time.time() - start))
        db.close()

    # Create a pool of integer to query random row in the database. No repeat.
    start = time.time()
    total_nb_transactions = len(all_transactions)
    choose_from = range(1,total_nb_transactions)
    random.shuffle(choose_from)

    # If the number of transactions asked is greater than what is available, return everything
    if nb_trans > len(choose_from):
        nb_trans = len(choose_from)

    transactions = []
    for i in range(nb_trans):
        index = choose_from[i]
        transactions.append(all_transactions[index])
    print "%-60s | %-s" % ("Choosing random transactions", pretty_print_duration(time.time() - start))

    # Filter the transactions that have no end date. We only need the transactions that we can
    # create a label.
    transactions = [t for t in transactions if t['end_date'] is not None]
    print "%-60s | %-d" % ("Transactions left after filtering on end date not null",  len(transactions))

    return transactions
        
    
def transaction_duration(transaction):
    """
    Based on a list of messages, returns the time elapsed between the first and the last one.
    """
    start_date = transaction['start_date']
    end_date = transaction['end_date']
    return (end_date - start_date).total_seconds()

    
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
    The features transactions 2D array is of size nbTranscations X nbFeatures
    The targets array is of size nbTransactions X 1
    """
    vec = ft.Vectorizer()
    start = time.time()
    vec_transactions = vec.fit_transform(transactions)
    print "%-60s | %-s" % ("Fit Transform the transactions", pretty_print_duration(time.time() - start))
    
    return vec_transactions
    

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


def mean_duration_per_priority(transactions):
    """
    Used to get the mean duration for every priority. The transactions are separated by priority
    and a dictionnary is returned containing {priority: mean}
    """
    durations = {}
    priorities_dist = {}
    for transaction in transactions:
        priority = transaction['priority']
        duration = transaction_duration(transaction)
        if priority not in priorities_dist:
            priorities_dist[priority] = [duration]
        else:
            priorities_dist[priority].append(duration)

    for key in priorities_dist.keys():
        durations[key] = np.mean(priorities_dist[key])

    return durations


def predictions_with_mean_duration(test_data, durations):
    targets = []
    for test in test_data:
    	priority = test['priority']
    	duration = durations[priority]
        targets.append(duration)

    return targets




def main(nb_transactions, model):

    print_header_with(str(nb_transactions) + ' - ' + model.__class__.__name__)

    population = Population(nb_transactions)
    transactions = vectorize_data(population.transactions)
    print "\n%-60s | %d" % ("Features for a transaction", len(transactions[0].features_))

    training_size = int(len(transactions) * 0.6)
    CV_size = int(len(transactions) * 0.8)
    test_size = len(transactions) - CV_size

    training_data = [t.features_ for t in transactions[:training_size]]
    training_targets = [t.target_ for t in transactions[:training_size]]
    print "%-60s | %d" % ("Transactions in the training set", len(training_data))

    CV_data = [t.features_ for t in transactions[training_size:CV_size]]
    CV_targets = [t.target_ for t in transactions[training_size:CV_size]]
    print "%-60s | %d" % ("Transactions in the CV set", len(CV_data))

    test_data = [t.features_ for t in transactions[-test_size:]]
    test_targets = [t.target_ for t in transactions[-test_size:]]
    print "%-60s | %d" % ("Transactions in the test set", len(test_data))


    start = time.time()
    model.fit(training_data, training_targets)
    
    print "Took %s seconds to complete with %d training examples" %(time.time() - start, len(training_data))

    print "\n%-60s | %f" % ("Score", score(model, test_data, test_targets))
    predictions = model_predictions(model, test_data)
    mse = mean_squared_error(predictions, test_targets)
    print "%-60s | %s" % ("Mean Squared Error", pretty_print_duration(mse))
    neg = negative_predictions(predictions)
    print "%d negative values in predictions" % len(neg)

    """
    random_prediction = np.random.gamma(5, 1, size = len(test_targets))
    mse_bench = mean_squared_error(random_prediction, test_targets)
    print "\nBench using random as predicted value for all test set = %s" % pretty_print_duration(mse_bench)
    """

    #durations = mean_duration_per_priority(transactions[:training_size])
    #mean_predictions = predictions_with_mean_duration(transactions[-test_size:], durations)
    #mse_mean = mean_squared_error(mean_predictions, test_targets)
    #print "\nBench using mean values based on priority = %s" % pretty_print_duration(mse_mean)
    #print durations

    training_predictions = model_predictions(model, training_data)
    training_mse = mean_squared_error(training_predictions, training_targets)

    return mse, training_mse


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
        if seconds < 1:
            pretty += "%f second" % seconds
        else:    
            pretty += "%d second(s)" % seconds

    return pretty


def print_header_with(value):
    value_len = len(str(value))
    print ''
    print '*' * 40
    spacer = (40 - value_len) / 2
    print ' ' * spacer, str(value)
    print '*' * 40




mse = []
models = []
#models.append(ElasticNet(alpha=1, rho=0.7))
#models.append(RidgeCV(alphas=[1, 10, 50, 100, 1000]))
#models.append(Lasso(alpha=0.1))
#models.append(LinearRegression())
models.append(SVR(epsilon=3600, verbose=True))

"""
for model in models:
    main(10000, model)
"""





for x in range(40000, 40100, 100):
    y_mse, y_training_mse = main(x, models[0])
    tuple = (x, y_mse, y_training_mse)
    mse.append(tuple)

general_persistence.dump(mse, 'SVR.out')
