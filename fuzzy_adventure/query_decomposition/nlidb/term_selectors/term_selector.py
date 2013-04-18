import MySQLdb
from fuzzy_adventure.hana import connection
from fuzzy_adventure.query_decomposition import permutation
from time import time

class TermSelector():

    @classmethod
    def fill_in_the_blanks(self, sql_template, keywords):
        metadata = sql_template[1]
        #blanks = sql_template[1]
        template = sql_template[0]

        if len(keywords) < len(metadata):
            raise RuntimeError("There were not enough keywords provided to fill all the variables in the SQL template")

        all_queries = []
        if len(metadata) == 0:
            all_queries.append(template)
        else:
            combos = permutation.permutations(keywords, len(metadata))
            all_queries = []
            for combo in combos:
                try:
                # filled_query = template % combo
                    filled_query = template % apply_type(combo, metadata)
                    all_queries.append(filled_query)
                except Exception:
                    continue

        return self.filter_answers(self.crash_and_burn(all_queries))
        #return all_queries
    

    @classmethod
    def apply_type(elements, types):
        applied = []
        for (i, element) in enumerate(elements):
            type_to_apply = types(i)
            applied.append(type_to_apply(element))
        return applied


    @classmethod
    def crash_and_burn(self, queries):
        answers = []
        cur = connection.get_cursor()
        for query in queries:
            try:
                cur.execute(query)
                result = cur.fetchall()[0][0]
                answers.append(result)
            except (Exception):
                pass
        cur.close()
        return answers
    
    @classmethod
    def filter_answers(self, answers):
        temp = [a for a in answers if a > 0] 
        result = temp[0] if len(temp) > 0 else None
        return result


#sql = "SELECT COUNT(transactions.id) FROM transactions WHERE transactions.end_date <>'0000-00-0000' AND transactions.programmer_id=(SELECT id FROM %s WHERE programmers.name = '%s');"
"""
keywords = ['jeff', 'baumer', 'hello', '0100157232', 'transactions', 'mark', 'rob', 'other', 'thing', 'world', 'foo', 'bar', 'programmers']
arg = (sql, 2)

start = time()
queries = TermSelector.fill_in_the_blanks(arg, keywords)
answers = TermSelector.crash_and_burn(queries)
correct = TermSelector.filter_answers(answers)
print correct
print "Duration: " + str(time() - start)
"""
