
class TermSelector():

	@classmethod
	def fill_in_the_blanks(sql_template, keywords):
		blanks = sql_template[1]
		template = sql_template[0]
		if blanks == 0:
			return template
		combos = []
		combo_count = combo_factorial(len(keywords), blanks)
		for i in range(combo_count):
			combos.append([])
		while len(combos[0]) < blanks:
			for word in keywords:
				for combo in combos:
					if word not in combo:
						combo.append(word)
		print combos
		return all_queries
	
	@classmethod
	def test_them(queries)
		for query in queries:
			execute(query)
		return answer
	
def combo_factorial(m,n):
	return math.factorial(m)/math.factorial(n)
