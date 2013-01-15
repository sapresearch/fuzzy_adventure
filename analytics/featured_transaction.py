import data

class FeaturedTransaction(object):

	def __init__(self, transaction):
		# The transaction comes from a database as a dictionnary
		self.transaction = transaction

		
	def as_dict(self):
		features = {}
		
		features['Component'] = self.transaction['components.name']
		# Classify programmers by level of expertise instead
		#features['Programmer'] = self.transaction['programmers.name']
		#features['Status'] = self.transaction['status']
		features['Priority'] = self.transaction['priority']
		features['Contract Priority'] = self.transaction['contract_priority']	
		#features['Product'] = self.transaction['product']
		#features['OS'] = self.transaction['os']
		#features['System Type'] = self.transaction['system_type']
		return features
		
	
class Vectorizer(object):

	def __init__(self):
		self.maps = {}
		self.sets = {}
		self.features_type = {}

	def fit_transform(self, transactions):
		"""
		Takes a list of Transaction objects.
		If the value associated with a key is a string, it will get converted to a numerical value to be used by a regression model.
		The order of the inputs is preserved.
		"""
		if not isinstance(transactions, list) or len(transactions) == 0:
			raise ValueError("Argument must be of class 'list' and non empty.")

		self.build_sets(transactions)
		self.build_maps()

		result = []
		for transaction in transactions:
			transaction.features_ = self.vectorize_input(transaction)
			result.append(transaction)

		return result


	def build_sets(self, transactions):
		"""
		Takes a list of dictionnaries (hash) representing features/inputs and returns a dictonnaries (hash) with the feature names and the possible values associated with it.
		"""
		
		keys = transactions[0].features_.keys()
		self.obtain_features_type(transactions)
		for key in keys:
			feature_set = list()
			for transaction in transactions:
				if self.features_type[key] is type('') and feature_set.count(transaction.features_[key]) == 0:
					feature_set.append(transaction.features_[key])
			self.sets[key] = list(feature_set)


	def obtain_features_type(self, transactions):
		"""
		Takes a list of dictionnaries (hash) representing features/inputs and returns a dictonnaries (hash) with the features' type.
		Raises ValueError if the dictonnaries do not all contain the same features.
		"""
		keys = transactions[0].features_.keys()
		for key in keys:
			feature_type = type(transactions[0].features_[key])
			# If some special treatement needs to be done for a particular feature (e.g. force it to be a string even though it's a number)
			# it can be done here
			for transaction in transactions:
				if key in transaction.features_:
					if type(transaction.features_[key]) is not feature_type:
						feature_type = type('')
						break
					#elif (<condition>):
						#do something
				else:
					raise ValueError('The list of dictionnaries must all contain the same information. i.e. they must all have the same features.')
			self.features_type[key] = feature_type


	def build_maps(self):
		"""
		Maps the possible values of every features to a numerical value.
		"""
		for feature_name in self.sets:
			values = self.sets[feature_name]
			mapping = {}
			for i in range(len(values)):
				mapping[values[i]] = i + 1
			self.maps[feature_name] = mapping


	def features(self):
		"""
		Returns a list of all the features name. Must have called fit_transform first, otherwise RuntimeError is raised.
		"""
		if self.features_type is not None:
			return self.features_type.keys()
		else:
			raise RuntimeError('No features have been fitted. Call fit_transform first.')


	def map(self, feature_name):
		"""
		Returns the map corresponding to the specified feature name.
		Raises ValueError if the name does not exist, 
		"""
		if feature_name in self.maps:
			return self.maps[feature_name]
		else:
			raise ValueError('No feature goes by the specified name.')


	def vectorize_input(self, transaction):
		"""
		Uses the maps previously created to associate the feature value to a numerical one for the specified input.
		Raises ValueError if 'input' is not a dictionnary.
		"""
		if not isinstance(transaction.features_, dict):
			raise ValueError("Every input must be dictionnary with the feature names as the key and its corresponding value as the value.")

		keys = self.features()
		vector = []
		for key in keys:
			value = transaction.features_[key]
			try:
				map = self.map(key)
				numerical_value = map[value]
				vector.append(numerical_value)
			except:
				vector.append(value)
		return vector
