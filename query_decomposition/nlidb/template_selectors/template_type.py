""" Uses the Decorator design pattern. This class wraps another class and adds the .template function to that class.
This .template function just allows us to put an 'A' or 'B' in the data file, rather than the long SQL statement that
the line corresponds with.  This way, we can change the SQL statement without modifying each example in the training file.
To use this, the class accepts an instance of another class at initialization:

bayes = Bayes(data_file)
classifier = TemplateClassifier(bayes)
classifier.tempate(query)

I don't want the Bayes class or the WordSpace class to inherit this function from a superclass, because I'll use them
in other modules where this function isn't necessary. """

import sys
import os
sys.path.append(os.environ['FUZZY_ADVENTURE'] + "/query_decomposition")
from confidence_estimator import *
class TemplateClassifier():

    q1 = ("SELECT name, COUNT(transactions.programmer_id) AS close_count FROM programmers, transactions WHERE programmers.id = transactions.programmer_id AND programmers.name <>'' GROUP BY transactions.programmer_id ORDER BY close_count DESC LIMIT 1;", 0)
    q2 = ('SELECT name, COUNT(transactions.component_id) FROM components INNER JOIN transactions on components.id = transactions.component_id GROUP BY transactions.component_id ORDER BY COUNT(transactions.component_id) DESC LIMIT 1;', 0)
    q3 = ("SELECT COUNT(transactions.id) FROM transactions WHERE transactions.end_date IS NOT NULL AND transactions.programmer_id=(SELECT id FROM programmers WHERE programmers.name = '%s');", 1)
    q4 = ("SELECT AVG(SECONDS_BETWEEN(start_date, end_date)) FROM transactions WHERE priority = '%s'", 1)
    q5 = ("SELECT AVG(SECONDS_BETWEEN(start_date, end_date)) FROM transactions WHERE transactions.end_date IS NOT NULL AND transactions.programmer_id=(SELECT id FROM programmers WHERE programmers.name = '%s')", 1)

    """
    q6 = ("SELECT COUNT(*) FROM TOUCHED WHERE PROGRAMMER_ID=%d", 1)
    q7 = ("SELECT AVG(SECONDS_BETWEEN(start_date, end_date)) FROM transactions", 1)
    q8 = ("SELECT AVG(MPT) FROM TRANSACTIONS", 0)
    q9 = ("SELECT COUNT(*) FROM TRANSACTIONS WHERE %s='%s'", 2)
    q10 = ("SELECT TRANS_NUMBER, COMPONENTS.NAME FROM TRANSACTIONS INNER JOIN COMPONENTS ON TRANSACTIONS.COMPONENT_ID = COMPONENTS.ID WHERE TRANSACTIONS.END_DATE IS NULL AND COMPONENTS.NAME = '%s'", 1)   
    q11 = ("SELECT TRANS_NUMBER FROM TRANSACTIONS INNER JOIN PROGRAMMERS ON TRANSACTIONS.PROGRAMMER_ID = PROGRAMMERS.ID WHERE PROGRAMMERS.NAME IS NULL", 0)
    """

    """
    q1 = ("SELECT name, COUNT(transactions.programmer_id) AS close_count FROM programmers, transactions WHERE programmers.id = transactions.programmer_id AND programmers.name <>'' GROUP BY transactions.programmer_id ORDER BY close_count DESC LIMIT 1;", ())
    q2 = ('SELECT name, COUNT(transactions.component_id) FROM components INNER JOIN transactions on components.id = transactions.component_id GROUP BY transactions.component_id ORDER BY COUNT(transactions.component_id) DESC LIMIT 1;', ())
    q3 = ("SELECT COUNT(transactions.id) FROM transactions WHERE transactions.end_date IS NOT NULL AND transactions.programmer_id=(SELECT id FROM programmers WHERE programmers.name = '%s');", (str,))
    q4 = ("SELECT AVG(SECONDS_BETWEEN(start_date, end_date)) FROM transactions WHERE priority = '%s'", (str,))
    q5 = ("SELECT AVG(SECONDS_BETWEEN(start_date, end_date)) FROM transactions WHERE transactions.end_date IS NOT NULL AND transactions.programmer_id=(SELECT id FROM programmers WHERE programmers.name = '%s')", (str,))
    
    q6 = ("SELECT COUNT(*) FROM TOUCHED WHERE PROGRAMMER_ID=%d", (int,))
    q7 = ("SELECT AVG(SECONDS_BETWEEN(start_date, end_date)) FROM transactions", ())
    q8 = ("SELECT AVG(MPT) FROM TRANSACTIONS", ())
    q9 = ("SELECT COUNT(*) FROM TRANSACTIONS WHERE %s='%s'", (str,str))
    q10 = ("SELECT TRANS_NUMBER, COMPONENTS.NAME FROM TRANSACTIONS INNER JOIN COMPONENTS ON TRANSACTIONS.COMPONENT_ID = COMPONENTS.ID WHERE TRANSACTIONS.END_DATE IS NULL AND COMPONENTS.NAME = '%s'", (str,))   
    q11 = ("SELECT TRANS_NUMBER FROM TRANSACTIONS INNER JOIN PROGRAMMERS ON TRANSACTIONS.PROGRAMMER_ID = PROGRAMMERS.ID WHERE PROGRAMMERS.NAME IS NULL", ())
    """

    templates = {'A': [q1, LAT.Programmer], 'B': [q2, LAT.Component], 'C': [q3, LAT.Integer], 'D': [q4, LAT.Decimal], 'E':[q5, LAT.Decimal]}#, 'F': [q6, LAT.Unknown], 'G': [q7, LAT.Unknown],'H': [q8, LAT.Unknown],'I': [q9, LAT.Unknown],'J': [q10, LAT.Unknown],'K':[q11, LAT.Unknown]}

    def __init__(self, model):
        self.model = model
    
    def template(self, query):
        klass = self.model.predict(query)
        sql = self.templates[klass][0]
        lat_type = self.templates[klass][1] # we aren't using this right now
        return sql, klass
