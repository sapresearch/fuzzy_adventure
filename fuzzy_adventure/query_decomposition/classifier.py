from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from fuzzy_adventure.test import load_data
from sklearn import cross_validation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from numpy import random


class TemplateClassifier(object):

    def __init__(self, file_path, model, test_size = 0.3):
        self.file_path = file_path
        self.model = model
        self.data, self.target = load_data.load_questions(self.file_path)
        self.test_size = test_size
        self.train, self.test, self.t_train, self.t_test = None, None, None, None
    
    def fit(self):
        self.train, self.test, self.t_train, self.t_test = cross_validation.train_test_split(self.data, 
                                                        self.target, 
                                                        test_size=self.test_size, 
                                                        random_state=random.RandomState())

        self.classifier = Pipeline([('nlp', NLP_Transform()), ('vect', CountVectorizer(ngram_range=(1,1))), ('clf', self.model)])  
        self.classifier.fit(self.train, self.t_train)

    
    def predict(self, text):
        prediction = self.classifier.predict(text)
        return prediction


    def score(self):
        return self.classifier.score(self.test, self.t_test)


from fuzzy_adventure.query_decomposition.nlp_system import nlp_nlidb
class NLP_Transform(object):

    def fit(self, raw_documents, y=None):
        return self


    def transform(self, raw_documents):
        documents = []

        for raw_doc in raw_documents:
            everything = []
            allWords, required_values, target, conditions, tables, question_type, proper_nouns = nlp_nlidb.nlp_nlidb(raw_doc)
            # everything.extend(allWords)
            # everything.extend(required_values)
            # everything.extend(target)
            # everything.extend(conditions)
            everything.extend(tables)
            # everything.extend(question_type)
            # everything.extend(question)
            
            everything.extend(allWords)
            everything.extend(proper_nouns)
            if len(everything) == 0:
                 documents.append(raw_doc)
            else:
                documents.append(' '.join(everything))

        return documents
