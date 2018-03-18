from nltk.tokenize import word_tokenize
import numpy as np
from nltk.corpus import stopwords
import nltk
import sys
import os

class Nltk_Similarity_Checker:

	def __init__(self):
		self.me = 'me'

	def process(self,text):
		tokens = word_tokenize(text)
		words = [w.lower() for w in tokens]

		porter = nltk.PorterStemmer()
		stemmed_tokens = [porter.stem(t) for t in words]

		# removing stop words
		stop_words = set(stopwords.words('english'))
		filtered_tokens = [w for w in stemmed_tokens if not w in stop_words]

		# count words
		count = nltk.defaultdict(int)
		for word in filtered_tokens:
			count[word] += 1
		return count;

	def cos_sim(self, a, b):
		dot_product = np.dot(a, b)
		norm_a = np.linalg.norm(a)
		norm_b = np.linalg.norm(b)
		return dot_product / (norm_a * norm_b)

	def getSimilarity(self,text1, text2):
		dict1 = self.process(text1)
		dict2 = self.process(text2)

		all_words_list = []
		for key in dict1:
			all_words_list.append(key)
		for key in dict2:
			all_words_list.append(key)
		all_words_list_size = len(all_words_list)

		v1 = np.zeros(all_words_list_size, dtype=np.int)
		v2 = np.zeros(all_words_list_size, dtype=np.int)
		i = 0
		for (key) in all_words_list:
			v1[i] = dict1.get(key, 0)
			v2[i] = dict2.get(key, 0)
			i = i + 1
		sim = self.cos_sim(v1, v2)
		return sim
