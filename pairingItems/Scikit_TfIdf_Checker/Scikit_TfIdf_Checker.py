from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

import sys
import os

class Scikit_TfIdf_Checker:

	def __init__(self):
		self.me = 'me'
		self.vect = TfidfVectorizer()


	def getSimilarity(self,text1, text2):
		tfidf = self.vect.fit_transform([text1, text2])

		#dot product to calculate cosine similarity
		similarity = (tfidf * tfidf.T).A
		#another option using sklearn.metrics.pairwise.cosine_similarity
		cosine = cosine_similarity(tfidf[1], tfidf)

		return similarity[0][1]
