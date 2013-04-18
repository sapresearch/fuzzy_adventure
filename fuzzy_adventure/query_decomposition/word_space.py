from numpy import *
from random import shuffle
from numpy.linalg import norm
import nltk
from nltk import *
from sklearn import tree
from sklearn.ensemble import ExtraTreesClassifier
from fuzzy_adventure.test import load_data
import time

class WordSpace():

    def __init__(self, file_path, vector_length=100):
        self.file_path = file_path
        self.vector_length = vector_length
        self.zero = 98
        self.one = 1
        self.length = self.zero + (2 * self.one) # for both positive and negative count.


    def predict(self, query, model=None, word_vector_hash=None):
        pred = self.hardcode(query)
        if pred != None:
            return pred
        if model == None or word_vector_hash == None:
            questions, types = load_data.load_questions(self.file_path)
            questions = questions[1::2]
            types = types[1::2]
            model, word_vector_hash = self.fit(questions, types)
        q = query.split(" ")
        q_vect = self.question_vectors(word_vector_hash, [q])[0]
        pred = model.predict(q_vect)[0]
        return pred


    def fit(self, questions, types):
        question_arrays = []
        for q in questions:
            question_arrays.append(q.split(" "))
    
        word_vector_hash = self.word_vectors(question_arrays)
        questions = self.question_vectors(word_vector_hash, question_arrays)
    
        xtrees = ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0)
        model = xtrees.fit(questions, types)
        return model, word_vector_hash


    """ Takes as input a multidimensional array
    with a subarray for each section of the corpus:
    [['hello' 'world'], ['goodbye', 'world']]
    It returns a dictionary of each word to its vector. """
    def word_vectors(self, corpus):
        count = 0
        all_words = []
        for section in corpus:
            all_words += section
        vectors = self.empty_vectors(all_words)
        for line in corpus:
            context_vector = self.random_vector(self.zero, self.one)
            for word in line:
                vectors[word] += context_vector # Every word in the same sentance gets added the same vector. Since a word can be present multiple sentence, it'll be added many times here. 
    
        # Normalize them.
        for word,vect in vectors.items():
            norm = linalg.norm(vect)
            vectors[word] = (vect/norm).round(2)
        return vectors


    def empty_vectors(self, words):
        words = set(words) # unique them
        dict = {}
        for w in words:
            dict[w] = zeros(self.length)
        return dict


    def random_vector(self, zero, one):
        z = zeros(zero)
        positives = ones(one)
        negatives = ones(one) * -1
        merged = array(list(z) + list(positives) + list(negatives))
        shuffle(merged)
        return merged
    
    
    def question_vectors(self, word_vector_hash, questions):
        question_vectors = []
        for q in questions:
            vect = zeros(self.vector_length)
            for word in q:
                if word in word_vector_hash: # See if case sensitive or not
                    vect += word_vector_hash[word] # From the vectors that we built in word_vectors, find the one corresponding to the word in the question if it exists. Add all the vectors of all the words in a question
            question_vectors.append(vect)
        return question_vectors
    

    def hardcode(self, query):
        return None