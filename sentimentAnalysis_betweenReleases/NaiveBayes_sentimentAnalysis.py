import os, csv, sys
import matplotlib.pyplot as plt
from matplotlib import pylab
from dateutil import parser
import nltk
import numpy as np
import pickle

reload(sys)
sys.setdefaultencoding('utf8')

def main(argv):
    global word_features
    word_features = []

    #train naive bayes classifier on training data
    #trainClassifier()

    #load naive bayes classifier from file
    classifier, word_features = loadClassifier()

    #set where to find release dates files
    mypath = os.path.dirname(__file__)
    tweetFilesPath = os.path.join(mypath, 'tweets_To_Analyze')
    tweetFiles = [f for f in os.listdir(tweetFilesPath) if os.path.isfile(os.path.join(tweetFilesPath, f))]

    #analyze each tweets file
    for file in tweetFiles:
        with open(os.path.join(tweetFilesPath,file)) as csvFile:
           reader = csv.reader(csvFile, delimiter=';')

           dates,scores,  flooredDates, flooredScores = getDatesAndScores2(classifier,reader)
           dates = convertDatesToPassedDays(dates)
           plotPolynomials(dates,scores,csvFile)
           flooredDates = convertDatesToPassedDays(flooredDates)
           plotPolynomials(flooredDates, flooredScores,csvFile)

           csvFile.close()

############################ NAIVE BAYES CLASSIFIER HELPER FUNTIONS#########################

def trainClassifier():
    global word_features
    print "Training classifier"
    mypath = os.path.join(os.path.dirname(__file__))
    trainDataPath = os.path.join(mypath, 'Sentiment140')
    trainDataFiles = [f for f in os.listdir(trainDataPath) if os.path.isfile(os.path.join(trainDataPath, f))]
    for file in trainDataFiles:
        with open(os.path.join(os.path.dirname(__file__), 'Sentiment140/') + file) as trainingFile:
           reader = csv.reader(trainingFile, delimiter=',')
           pos_tweets = []
           neg_tweets = []
           for row in reader:
               if(row[0]=="0"):
                   neg_tweets.append((row[5],"negative"))
               elif(row[0]=="4"):
                   pos_tweets.append((row[5], "positive"))

           print "positive: " + str(len(pos_tweets))
           print "negative: " + str(len(neg_tweets))

            #Arrayify tweets
           tweets = []
           for (words, sentiment) in pos_tweets[0:5000] + neg_tweets[0:5000]:
               words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
               tweets.append((words_filtered, sentiment))

           word_features = get_word_features(get_words_in_tweets(tweets))
           training_set = nltk.classify.apply_features(extract_features, tweets)
           classifier = nltk.NaiveBayesClassifier.train(training_set)
           print classifier.show_most_informative_features(32)

           f = open('NaiveBayesClassifier.pickle', 'wb')
           pickle.dump(classifier, f)
           f.close()

           f = open('word_features.pickle', 'wb')
           pickle.dump(word_features, f)
           f.close()

        trainingFile.close()

    print "Classifier trained and saved"


def getDatesAndScores2(classifier, reader):
    included_cols = [1, 4]
    sentimentScoresDict = dict()
    flooredSentimentScoresDict = dict()
    dateCounts = dict()
    flooredDateCounts = dict()
    averageScores = dict()
    flooredAverageScores = dict()
    i=0
    separator = ' '

    for row in reader:
        if (row[4] == 'text'):
            continue;

        content = list(row[i] for i in included_cols)

        #assign numeric value to classified tweets
        if (classifier.classify(extract_features(content[1].split())) == "positive"):
            rowScore = 1
        else:
            rowScore = -1

        date = parser.parse(row[1].split(separator, 1)[0]).date()

        #add date and score to dictionary
        if (date in sentimentScoresDict):
            dateCounts[date] = dateCounts[date] + 1;
            sentimentScoresDict[date] = sentimentScoresDict[date] + rowScore
        else:
            sentimentScoresDict[date] = rowScore
            dateCounts[date] = 1;

        #print to see if programm is still running
        i=i+1
        if i%1000 == 0:
            print i

    for date, scoreSum in sentimentScoresDict.iteritems():
        averageScores[date] = scoreSum / dateCounts[date]

    for flooredDate, scoreSum in flooredSentimentScoresDict.iteritems():
        flooredAverageScores[flooredDate] = scoreSum / flooredDateCounts[flooredDate]
        i = i + 1
        print i

    return averageScores.keys(), averageScores.values(), flooredAverageScores.keys(), flooredAverageScores.values()


def loadClassifier():
    f = open('NaiveBayesClassifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()

    f = open('word_features.pickle', 'rb')
    wordFeatures = pickle.load(f)
    f.close()
    return classifier, wordFeatures

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

def plotPolynomials(dates,scores):
    x = dates
    y = scores

    # calculate polynomial
    z2 = np.polyfit(x, y, 2)
    z3 = np.polyfit(x, y, 3)
    z4 = np.polyfit(x, y, 4)
    f2 = np.poly1d(z2)
    f3 = np.poly1d(z3)
    f4 = np.poly1d(z4)

    # calculate new x's and y's
    x_new = np.linspace(0, max(x), 200)
    y_new2 = f2(x_new)
    y_new3 = f3(x_new)
    y_new4 = f4(x_new)


    plt.plot(x, y, 'o', x_new, y_new2, '.', x_new, y_new3, '-', x_new,y_new4, '--')
    pylab.title('Polynomial Fit with Matplotlib')
    plt.show()


def convertDatesToPassedDays(dates):
    minDate = min(dates)
    passedDays = []

    for date in dates:
        passedDays.append(abs((date - minDate).days))
    return passedDays

if __name__ == "__main__":
    main(sys.argv)

reload(sys)
sys.setdefaultencoding('utf8')


