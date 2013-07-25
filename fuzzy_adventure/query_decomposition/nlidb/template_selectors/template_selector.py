""" Uses the Decorator design pattern. This class wraps another class and adds the .template function to that class.
This .template function just allows us to put an 'A' or 'B' in the data file, rather than the long SQL statement that
the line corresponds with.  This way, we can change the SQL statement without modifying each example in the training file.
To use this, the class accepts an instance of another class at initialization:

bayes = Bayes(data_file)
classifier = TemplateClassifier(bayes)
classifier.tempate(query)

I don't want the Bayes class or the WordSpace class to inherit this function from a superclass, because I'll use them in other modules where this function isn't necessary. """


class TemplateSelector():

    q1 = ("SELECT PROGRAMMERS.FULL_NAME FROM TRANSACTIONS INNER JOIN PROGRAMMERS ON TRANSACTIONS.PROGRAMMER_ID = PROGRAMMERS.ID WHERE END_DATE IS NOT NULL AND PROGRAMMERS.FULL_NAME IS NOT NULL GROUP BY PROGRAMMERS.FULL_NAME ORDER BY COUNT(*) DESC LIMIT 1", ())
    q2 = ("SELECT COMPONENTS.NAME FROM COMPONENTS WHERE ID = (SELECT TRANSACTIONS.COMPONENT_ID FROM TRANSACTIONS GROUP BY TRANSACTIONS.COMPONENT_ID ORDER BY COUNT(TRANSACTIONS.COMPONENT_ID) DESC LIMIT 1)", ())
    q3 = ("select count(trans_number) from TRANSACTIONS inner join PROGRAMMERS ON TRANSACTIONS.PROGRAMMER_ID = PROGRAMMERS.ID where PROGRAMMERS.FULL_NAME='%s' and TRANSACTIONS.END_DATE is not null", (str,))
    q4 = ("SELECT AVG(SECONDS_BETWEEN(start_date, END_DATE)) FROM TRANSACTIONS WHERE priority = '%s'", (str,))
    q5 = ("SELECT AVG(SECONDS_BETWEEN(start_date, END_DATE)) FROM TRANSACTIONS WHERE TRANSACTIONS.END_DATE IS NOT NULL AND TRANSACTIONS.PROGRAMMER_ID=(SELECT ID FROM PROGRAMMERS WHERE PROGRAMMERS.FULL_NAME = '%s')", (str,))
    q6 = ("SELECT COUNT(*) FROM TOUCHED INNER JOIN PROGRAMMERS ON TOUCHED.PROGRAMMER_ID=PROGRAMMERS.ID WHERE PROGRAMMERS.FULL_NAME='%s'", (str,))
    q7 = ("SELECT AVG(SECONDS_BETWEEN(start_date, END_DATE)) FROM TRANSACTIONS", ())
    q8 = ("SELECT AVG(MPT) FROM TRANSACTIONS", ())
    q9 = ("select count(trans_number) from TRANSACTIONS inner join PROGRAMMERS on TRANSACTIONS.PROGRAMMER_ID = PROGRAMMERS.ID where PROGRAMMERS.FULL_NAME = '%s' and TRANSACTIONS.FLAG_24H is not null", (str,))
    q10 = ("SELECT TRANS_NUMBER, COMPONENTS.NAME FROM TRANSACTIONS INNER JOIN COMPONENTS ON TRANSACTIONS.COMPONENT_ID = COMPONENTS.ID WHERE TRANSACTIONS.END_DATE IS NULL AND COMPONENTS.NAME = '%s'", (str,))
    q11 = ("SELECT TRANS_NUMBER FROM TRANSACTIONS INNER JOIN PROGRAMMERS ON TRANSACTIONS.PROGRAMMER_ID = PROGRAMMERS.ID WHERE PROGRAMMERS.NAME IS NULL", ())
    # q12 = ("SELECT START_DATE FROM TRANSACTIONS INNER JOIN PROGRAMMERS ON TRANSACTIONS.PROGRAMMER_ID = PROGRAMMERS.ID INNER JOIN COMPONENTS ON TRANSACTIONS.COMPONENT_ID = COMPONENTS.ID WHERE COMPONENTS.NAME='%s' AND PROGRAMMERS.NAME='%s'", (str, str,))


    templates = {'A': q1, 'B': q2, 'C': q3, 'D': q4, 'E':q5, 'F': q6, 'G': q7,'H': q8,'I': q9,'J': q10,'K': q11}#, 'L': q12}

    def __init__(self, model):
        self.model = model
    
    def template(self, query):
        category = self.model.predict([query])
        sql = self.templates[category[0]]
        return sql, category
