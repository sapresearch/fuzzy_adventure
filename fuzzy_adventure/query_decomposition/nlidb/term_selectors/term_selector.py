#import MySQLdb
from fuzzy_adventure.hana import connection
from fuzzy_adventure.query_decomposition import permutation
from time import time
import numpy as np
from pandas import DataFrame

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
    def apply_type(self, elements, types):
        if len(elements) != len(types):
            raise IndexError("The number of elements and types must be equals.")

        applied = []
        for (i, element) in enumerate(elements):
            type_to_apply = types[i]
            applied.append(type_to_apply(element))
        return applied


    @classmethod
    def crash_and_burn(self, queries):
        answers = []
        cur = connection.get_cursor()
        for query in queries:
            try:
                cur.execute(query)
                result = cur.fetchall()
                df = DataFrame(result)
                answers.append(df[0].tolist())
            except (Exception):
                pass
        cur.close()
        return answers
    
    @classmethod
    def filter_answers(self, answers):
        temp = np.array([a for a in answers if a > 0 and a != '' and a != None])
        result = temp[0] if len(temp) > 0 else None
        return result


