import os, csv, sys, re
import matplotlib.pyplot as plt
from matplotlib import pylab
from dateutil import parser
import nltk
import numpy as np
import pickle
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.model_selection import StratifiedKFold

reload(sys)
sys.setdefaultencoding('utf8')

def main(argv):
    global word_features
    word_features = []

    #train naive bayes classifier on training data
    #trainClassifier()

    #execute cross validation (for thesis text)
    corpus, labels = make_Corpus_From_Tweets(root_dir='datasets/Sentiment140_testData')
    execute_crossValidation(fold_splits=4, corpus=corpus, labels=labels)

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

def execute_crossValidation(fold_splits, corpus, labels):
    kf = StratifiedKFold(n_splits=fold_splits)

    #choose classifiers to evaluate
    iter=1;

    #performance metrics initialization
    crossValidationAccuracy = []
    crossValidationRecall = []
    crossValidationPrecision = []
    crossValidationFmeasure = []
    confusionMatrix = np.zeros((2, 2))*1.0;  #confusion matrix

    print "Starting n-fold training with number of folds:"+str(fold_splits)
    for train_index, test_index in kf.split(corpus, labels):
        #create arrays and corpuses according to current fold
        X_train = [corpus[i] for i in train_index]
        X_test = [corpus[i] for i in test_index]
        y_train, y_test = labels[train_index], labels[test_index]

        # Arrayify tweets
        tweets = []
        for idx, traintweet in enumerate(X_train):
            words_filtered = [e.lower() for e in traintweet.split() if len(e) >= 3]
            tweets.append((words_filtered, y_train[idx]))

        word_features = get_word_features(get_words_in_tweets(tweets))
        training_set = nltk.classify.apply_features(extract_features, tweets)
        classifier = nltk.NaiveBayesClassifier.train(training_set)

        #fit(train) models and check performance on testing part of data
        result = []
        for testtweet in X_test:
            result.append(classifyAndAddNumericValue(classifier, testtweet))


        crossValidationAccuracy.append(accuracy_score(y_test,result))
        crossValidationRecall.append(recall_score(y_test, result))
        crossValidationPrecision.append(precision_score(y_test, result))
        crossValidationFmeasure.append(f1_score(y_test, result))
        conf_matrix = confusion_matrix(y_test, result)
        normalized_conf_matrix = np.divide(conf_matrix, len(result), dtype=float)
        confusionMetrice = confusionMatrix + normalized_conf_matrix

        print "Models succesfully trained, number of iteration:" + str(iter)

        #iterator for logging messages
        iter = iter+1

    print str(fold_splits) + "-fold cross validation done, confusion matrices:"

    print "Cross validation accuracy: ",
    for item in crossValidationAccuracy: print item,
    print "Cross validation accuracy average:" + str(sum(crossValidationAccuracy) / len(crossValidationAccuracy))
    print "Cross validation precision: ",
    for item in crossValidationPrecision: print item,
    print "Cross validation precision average:" + str(
        sum(crossValidationPrecision) / len(crossValidationPrecision))
    print "Cross validation recall: ",
    for item in crossValidationRecall: print item,
    print "Cross validation accuracy average:" + str(
        sum(crossValidationRecall) / len(crossValidationRecall))
    print "Cross validation F measure: ",
    for item in crossValidationFmeasure: print item,
    print "Cross validation accuracy average:" + str(
        sum(crossValidationFmeasure) / len(crossValidationFmeasure))

    print "Cross validation confusion matrix:" + str(confusionMatrix/fold_splits)

def make_Corpus_From_Tweets(root_dir):
    print "Creating training corpus from training tweets"
    mypath = os.path.dirname(__file__)
    trainDataPath = os.path.join(mypath, root_dir)
    trainDataFiles = [f for f in os.listdir(trainDataPath) if os.path.isfile(os.path.join(trainDataPath, f))]

    corpus = []
    #Sentiment140 contains 499 tweets
    labels = np.zeros(359);
    for file in trainDataFiles:
        with open(os.path.join(mypath, root_dir+'/') + file) as trainingFile:
            reader = csv.reader(trainingFile, delimiter=',')
            iterator = -1;
            a = 0
            #for each tweet in file
            for row in reader:
                #if it's either positive or negative
                if (row[0] == "0" or row[0] == "4"):
                    #increase index because we're adding to corpus
                    iterator = iterator + 1
                    #add the tweet to corpus
                    corpus.append(unicode(preprocess(row[5]), errors='ignore'))
                    #add positive or negative label
                    if (row[0] == "0"):
                        labels[iterator] = 0
                    elif (row[0] == "4"):
                        labels[iterator] = 1

        trainingFile.close()
    return corpus,labels

def preprocess(raw_text):
    #remove hashtags, @references,
    letters_only_text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(#[A-Za-z0-9]+)|(\w+:\/\/\S+)"," ",raw_text).split())
    return letters_only_text


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
        if (row[4] == 'text'):    #next(reader) ?
            continue;

        content = list(row[i] for i in included_cols)

        #assign numeric value to classified tweets
        rowScore = classifyAndAddNumericValue(classifier, content[1].split())

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

def classifyAndAddNumericValue(classifier, content):
    output = classifier.classify(extract_features(content))
    '''if (output == "positive"):
        rowScore = 1
    else:
        rowScore = -1'''
    return output

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


