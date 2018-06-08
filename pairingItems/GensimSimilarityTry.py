from nltk.tokenize import word_tokenize
import gensim

raw_documents = [
                 "My socks are a force multiplier.",
				 ]

gen_docs = [[w.lower() for w in word_tokenize(text)] for text in raw_documents]
dictionary = gensim.corpora.Dictionary(gen_docs)
bagOfWords = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
print(bagOfWords)

#term frequency-inverse document frequency
#term frequency - how often the word shows up in document
# inverse document frequency - scales tf according how rare the word is in the corpus
tf_idf_model = gensim.models.TfidfModel(bagOfWords)
sims = gensim.similarities.Similarity('/usr/workdir/',tf_idf_model[bagOfWords], num_features=len(dictionary))

query_doc = [w.lower() for w in word_tokenize("Socks are a force for good.")]
print(query_doc)
query_doc_bow = dictionary.doc2bow(query_doc)
print(query_doc_bow)
query_doc_tf_idf = tf_idf_model[query_doc_bow]
print(query_doc_tf_idf)

