from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim,sys,os,csv

reload(sys)
#sys.setdefaultencoding('utf8')

def main(argv):
	find_Topics_In_Tweets("tweets_To_Analyze")

def find_Topics_In_Tweets(dir):
	# set where to find tweets to analyze
	mypath = os.path.dirname(__file__)
	tweetFilesPath = os.path.join(mypath, dir)
	tweetFiles = [f for f in os.listdir(tweetFilesPath) if os.path.isfile(os.path.join(tweetFilesPath, f))]

	# analyze each tweets file
	for file in tweetFiles:
		with open(os.path.join(tweetFilesPath, file)) as csvFile:
			reader = csv.reader(csvFile, delimiter=';')

			tweet_set = []
			for row in reader:
				if row[4] == "text":
					continue
				# compile tweets into a list
				tweet_set.append(row[4])

			tokenizer = RegexpTokenizer(r'\w+')

			# create English stop words list
			en_stop = get_stop_words('en')

			# Create p_stemmer of class PorterStemmer
			p_stemmer = PorterStemmer()

			# list for tokenized documents in loop
			preprocessedTweets = []

			# loop through document list
			for tweet in tweet_set:
				# clean and tokenize document string
				loweredTweet = tweet.lower()
				tweetTokens = tokenizer.tokenize(loweredTweet)

				# remove stop words from tokens
				stopped_tokens = [i for i in tweetTokens if not i in en_stop]

				# stem tokens
				encodingErr = False
				try:
					#stemmed_tokens = [p_stemmer.stem(i).encode('utf-8') for i in stopped_tokens]
					stemmed_tokens = [i.encode('utf-8') for i in stopped_tokens]
				except Exception as ex:
					encodingErr=True
				if encodingErr:
					continue


				# add tokens to list
				preprocessedTweets.append(stemmed_tokens)

			# turn our tokenized documents into a id <-> term dictionary
			dictionary = corpora.Dictionary(preprocessedTweets)

			# convert tokenized documents into a document-term matrix
			corpus = [dictionary.doc2bow(text) for text in preprocessedTweets]

			# generate LDA model
			ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=10)
			print(ldamodel.print_topics(num_topics=5, num_words=5))
			#print(dictionary.token2id)
			#print corpus


def myfunction(text):
    try:
        text = unicode(text, 'utf-8')
    except TypeError:
        return text

	return text

if __name__ == "__main__":
    main(sys.argv)

reload(sys)
sys.setdefaultencoding('utf8')


