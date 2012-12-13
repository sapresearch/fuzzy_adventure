

class FeaturedTransaction(object):

	def __init__(self, transaction):
		self.transaction = transaction

		
	def as_dict(self):
		features = {}
		
		features['Component'] = self.transaction['components.name']
		features['Programmer'] = self.transaction['programmers.name']
		features['Status'] = self.transaction['status']
		features['Priority'] = self.transaction['priority']
		features['Contract Priority'] = self.transaction['contract_priority']	
		features['Product'] = self.transaction['product']
	
		return features