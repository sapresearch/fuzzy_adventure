

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
		
		
	def stem_component(component):
		"""
		Return the component stem.
		A component stem is the top hierarchy for that component's family.
		e.g. SRD-CC-IAM is SRD
		"""
		stem = component.split('-')[0]
		
		if stem == "" or stem is None:
			raise ValueError
		
		return stem