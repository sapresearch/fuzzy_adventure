import MySQLdb as mdb
import random


class Population(object):

    size = 0
    transactions = []

    def __init__(self, size):
        self.size = size
        self.fetch_all()
        #self.build_sets(size)


    def fetch_all(self):
        """
        Fetches all the data from the database.
        """
        if len(self.transactions) == 0:
            db = mdb.connect(host="localhost", user="root", passwd="nolwen", db="watchTowerSpace")

            # Put all the transactions in memory. This could be an issue with bigger data
            db.query("""SELECT *, programmers.name, components.name 
            FROM transactions, programmers, components 
            WHERE programmer_id = programmers.id AND component_id = components.id""")
            self.transactions = db.store_result().fetch_row(0,1) # Rows are returned as dictionnary [column name, value]

            # Filter the transactions that have no end date. We only need the transactions that we can
            # create a label.
            self.transactions = [Transaction(t) for t in self.transactions if t['end_date'] is not None]
            random.shuffle(self.transactions)
            self.transactions = self.transactions[:self.size]
            db.close()


    def build_sets(self, size):
        """
        Master method to create all the sets (training, CV and test) with proportions 60%, 20% and 20%.
        """
        training_size = int(size * 0.6)
        cv_size = int(size * 0.2)
        test_size = size - training_size - cv_size

        training(0, training_size)
        cv(training_size, training_size + cv_size)
        test(training_size + cv_size, training_size + cv_size + test_size)



class Transaction(object):
    features_ = {}
    target_ = None

    def __init__(self, transaction):
        self.features(transaction)
        self.target(transaction)


    def features(self, transaction):
        self.features_['Component'] = transaction['components.name']
        # Classify programmers by level of expertise instead
        #self.features_['Programmer'] = transaction['programmers.name']
        #self.features_['Status'] = transaction['status']
        self.features_['Priority'] = transaction['priority']
        self.features_['Contract Priority'] = transaction['contract_priority']   
        #self.features_['Product'] = transaction['product']
        #self.features_['OS'] = transaction['os']
        #self.features_['System Type'] = transaction['system_type']


    def target(self, transaction):
        start_date = transaction['start_date']
        end_date = transaction['end_date']
        self.target_ = (end_date - start_date).total_seconds()
