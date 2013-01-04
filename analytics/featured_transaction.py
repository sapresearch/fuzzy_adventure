

class FeaturedTransaction(object):

	def __init__(self, transaction):
		# The transaction comes from a database as a dictionnary
		self.transaction = transaction

		
	def as_dict(self):
		features = {}
		
		features['Component'] = self.transaction['components.name']
		# Classify programmers by level of expertise instead
		#features['Programmer'] = self.transaction['programmers.name']
		features['Status'] = self.transaction['status']
		features['Priority'] = self.transaction['priority']
		features['Contract Priority'] = self.transaction['contract_priority']	
		features['Product'] = self.transaction['product']
		features['OS'] = self.transaction['os']
		return features
		
	
class Vectorizer(object):

	def __init__(self):
		self.maps = {}
		self.sets = {}

	def fit_transform(self, inputs):
		"""
		Takes a list of dictionnaries (or hash) representing features/inputs.
		If the value associated with a key is a string, it will get converted to a numerical value to be used by a regression model.
		"""
		if not isinstance(inputs, list) or len(inputs) == 0:
			raise ValueError("Argument must be of class 'list' and non empty.")

		self.build_sets(inputs)
		self.build_maps()
		result = []
		for input in inputs:
			vec = self.vectorize_input(input)
			result.append(vec)

		return result


	def build_sets(self, features):
		"""
		Takes a list of dictionnaries (hash) representing features/inputs and returns a dictonnaries (hash) with the feature names and the possible values associated with it.
		Raises ValueError if the dictonnaries do not all contain the same features.
		"""
		
		keys = features[0].keys()
		for key in keys:
			feature_set = list()
			for feature in features:
				if feature.has_key(key):
					if feature_set.count(feature[key]) == 0:
						feature_set.append(feature[key])
				else:
					raise ValueError('The list of dictionnaries must all contain the same information. i.e. they must all have the same features.')
			self.sets[key] = list(feature_set)


	def build_maps(self):
		"""
		Maps the possible values of every features to a numerical value.
		"""
		for feature_name in self.sets:
			values = self.sets[feature_name]
			map = {}
			for i in range(len(values)):
				map[values[i]] = i + 1
			self.maps[feature_name] = map


	def features(self):
		"""
		Returns a list of all the features name. Must have called fit_transform first, otherwise RuntimeError is raised.
		"""
		if self.maps is not None:
			return self.maps.keys()
		else:
			raise RuntimeError('No features have been fitted. Call fit_transform first.')


	def map(self, feature_name):
		"""
		Returns the map corresponding to the specified feature name.
		Raises ValueError if the name does not exist, 
		"""
		if self.maps.has_key(feature_name):
			return self.maps[feature_name]
		else:
			raise ValueError('No feature goes by the specified name.')


	def vectorize_input(self, input):
		"""
		Uses the maps previously created to associate the feature value to a numerical one for the specified input.
		Raises ValueError if 'input' is not a dictionnary.
		"""
		if not isinstance(input, dict):
			raise ValueError("Every input must be dictionnary with the feature names as the key and its corresponding value as the value.")

		keys = self.features()
		vector = []
		for key in keys:
			value = input[key]
			map = self.map(key)
			numerical_value = map[value]
			vector.append(numerical_value)

		return vector
