from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

import sys
import os

class Scikit_TfIdf_Checker:

	def __init__(self):
		self.me = 'me'
		self.vect = TfidfVectorizer(min_df=1)


	def getSimilarity(self,text1, text2):
		tfidf = self.vect.fit_transform([text1, text2])
		return (tfidf * tfidf.T).A
