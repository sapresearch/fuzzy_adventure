""" Uses the Decorator design pattern. This class wraps another class and adds the .template function to that class.
This .template function just allows us to put an 'A' or 'B' in the data file, rather than the long SQL statement that
the line corresponds with.  This way, we can change the SQL statement without modifying each example in the training file.
To use this, the class accepts an instance of another class at initialization:

bayes = Bayes(data_file)
classifier = TemplateClassifier(bayes)
classifier.tempate(query)

I don't want the Bayes class or the WordSpace class to inherit this function from a superclass, because I'll use them in other modules where this function isn't necessary. """


class TemplateSelector():

    q1 = ("select PROGRAMMERS.FULL_NAME from TRANSACTIONS inner join PROGRAMMERS on TRANSACTIONS.PROGRAMMER_ID = PROGRAMMERS.ID where END_DATE is not null and PROGRAMMERS.FULL_NAME is not null group by PROGRAMMERS.FULL_NAME order by count(*) desc limit 1", ())
    q2 = ("select COMPONENTS.NAME from COMPONENTS where ID = (select TRANSACTIONS.COMPONENT_ID from TRANSACTIONS group by TRANSACTIONS.COMPONENT_ID order by count(TRANSACTIONS.COMPONENT_ID) desc limit 1)", ())
    q3 = ("select count(TRANS_NUMBER) from TRANSACTIONS inner join PROGRAMMERS on TRANSACTIONS.PROGRAMMER_ID = PROGRAMMERS.ID where PROGRAMMERS.FULL_NAME='%s' and TRANSACTIONS.END_DATE is not null", (str,))
    q4 = ("select avg(SECONDS_BETWEEN(START_DATE, END_DATE)) from TRANSACTIONS where PRIORITY = '%s'", (str,))
    q5 = ("select avg(SECONDS_BETWEEN(START_DATE, END_DATE)) from TRANSACTIONS where TRANSACTIONS.END_DATE is not null and TRANSACTIONS.PROGRAMMER_ID=(select ID from PROGRAMMERS where PROGRAMMERS.FULL_NAME = '%s')", (str,))
    q6 = ("select count(*) from TOUCHED inner join PROGRAMMERS on TOUCHED.PROGRAMMER_ID=PROGRAMMERS.ID where PROGRAMMERS.FULL_NAME='%s'", (str,))
    q7 = ("select avg(SECONDS_BETWEEN(START_DATE, END_DATE)) from TRANSACTIONS", ())
    q8 = ("select avg(MPT) from TRANSACTIONS", ())
    q9 = ("select count(TRANS_NUMBER) from TRANSACTIONS inner join PROGRAMMERS on TRANSACTIONS.PROGRAMMER_ID = PROGRAMMERS.ID where PROGRAMMERS.FULL_NAME = '%s' and TRANSACTIONS.FLAG_24H is not null", (str,))
    q10 = ("select TRANS_NUMBER, COMPONENTS.NAME from TRANSACTIONS inner join COMPONENTS on TRANSACTIONS.COMPONENT_ID = COMPONENTS.ID where TRANSACTIONS.END_DATE IS NULL and COMPONENTS.NAME = '%s'", (str,))
    q11 = ("select TRANS_NUMBER from TRANSACTIONS inner join PROGRAMMERS on TRANSACTIONS.PROGRAMMER_ID = PROGRAMMERS.ID where PROGRAMMERS.NAME IS NULL", ())
    # q12 = ("select START_DATE from TRANSACTIONS inner join PROGRAMMERS on TRANSACTIONS.PROGRAMMER_ID = PROGRAMMERS.ID inner join COMPONENTS on TRANSACTIONS.COMPONENT_ID = COMPONENTS.ID where COMPONENTS.NAME='%s' and PROGRAMMERS.NAME='%s'", (str, str,))


    templates = {'A': q1, 'B': q2, 'C': q3, 'D': q4, 'E':q5, 'F': q6, 'G': q7,'H': q8,'I': q9,'J': q10,'K': q11}#, 'L': q12}

    def __init__(self, model):
        self.model = model
    
    def template(self, query):
        category = self.model.predict([query])
        sql = self.templates[category[0]]
        return sql, category
