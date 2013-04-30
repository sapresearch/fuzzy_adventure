import data
import numpy as np

class Vectorizer(object):

	def __init__(self):
		self.maps = {}
		self.sets = {}
		self.features_type = {}
		self.means_map = {}

	def fit_transform(self, transactions, normalize = False):
		"""
		Takes a list of Transaction objects.
		If the value associated with a key is a string, it will get converted to a numerical value to be used by a regression model.
		The order of the inputs is preserved.
		"""
		if not isinstance(transactions, list) or len(transactions) == 0:
			raise ValueError("Argument must be of class 'list' and non empty.")

		self.build_sets(transactions)
		self.build_maps()
		self.vectorize_input_as_means(transactions)

		result = self.vectorize_inputs(transactions)
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


	def vectorize_inputs(self, transactions):
		"""
		Uses the maps previously created to associate the feature value to a numerical one for the specified input.
		Raises ValueError if 'input' is not a dictionnary.
		"""

		result = []
		keys = self.features()

		for transaction in transactions:
			features = []
			if not isinstance(transaction.features_, dict):
				raise ValueError("Every input must be dictionnary with the feature names as the key and its corresponding value as the value.")
			for key in keys:
				value = transaction.features_[key]

				mean = self.means_map[key][value]
				features.append(mean)
				"""
				try:
					mapping = self.map(key)
					numerical_value = mapping[value]
					features.append(numerical_value)
				except:
					features.append(value)
				"""

			transaction.features_ = features
			result.append(transaction)

		return result


	def vectorize_input_as_means(self, transactions):
		self.means_map = {}
		for key in self.sets.keys():
			pairs = {}
			for value in self.sets[key]:
				mean = np.mean([t.target_ for t in transactions if t.features_[key] == value])
				pairs[value] = mean
			self.means_map[key] = pairs