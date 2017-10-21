import os, csv, sys
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import StratifiedKFold

reload(sys)
sys.setdefaultencoding('utf8')

def main(argv):
    # Create a corpus from training data
    corpus, labels = make_Corpus_From_Tweets(root_dir='datasets/Sentiment140')

    #define vectorizer parameters for models creation
    vectorizer = TfidfVectorizer(min_df=5, max_df=0.8, sublinear_tf=True, use_idf=True, stop_words='english')
    #execute_crossValidation(fold_splits=4, corpus=corpus, labels=labels, vectorizer=vectorizer)
    #model1_linearSVC, model2_multinomNB = create_Models(corpus=corpus,labels=labels,vectorizer=vectorizer)

    # set where to find release dates files
    mypath = os.path.dirname(__file__)
    tweetFilesPath = os.path.join(mypath, 'tweets_To_Analyze')
    tweetFiles = [f for f in os.listdir(tweetFilesPath) if os.path.isfile(os.path.join(tweetFilesPath, f))]

    # analyze each tweets file
    for file in tweetFiles:
        with open(os.path.join(tweetFilesPath,file)) as csvFile:
            reader = csv.reader(csvFile, delimiter=';')

def make_Corpus_From_Tweets(root_dir):
    mypath = os.path.dirname(__file__)
    trainDataPath = os.path.join(mypath, root_dir)
    trainDataFiles = [f for f in os.listdir(trainDataPath) if os.path.isfile(os.path.join(trainDataPath, f))]

    corpus = []
    #initialization of numpy array needed (1,600,000 is size of my sentiment140 training dataset)
    labels = np.zeros(1600000);
    for file in trainDataFiles:
        with open(os.path.join(mypath, root_dir+'/') + file) as trainingFile:
            reader = csv.reader(trainingFile, delimiter=',')
            iterator = -1;
            #for each tweet in file
            for row in reader:
                #if it's either positive or negative
                if (row[0] == "0" or row[0] == "4"):
                    #increase index because we're adding to corpus
                    iterator = iterator + 1
                    #add the tweet to corpus
                    corpus.append(unicode(row[5], errors='ignore'))
                    #add positive or negative label
                    if (row[0] == "0"):
                        labels[iterator] = 0
                    elif (row[0] == "4"):
                        labels[iterator] = 1

        trainingFile.close()
    return corpus,labels

def make_Corpus_From_Movies(root_dir):
    polarity_dirs = [os.path.join(os.path.join(os.path.dirname(__file__), root_dir),f) for f in os.listdir(os.path.join(os.path.dirname(__file__), root_dir))]
    #polarity_dirs = [os.path.join(root_dir, f) for f in os.listdir(root_dir)]
    corpus = []
    for polarity_dir in polarity_dirs:
        reviews = [os.path.join(polarity_dir, f) for f in os.listdir(polarity_dir)]
        for review in reviews:
            doc_string = "";
            with open(review) as rev:
                for line in rev:
                    doc_string = doc_string + line
            if not corpus:
                corpus = [doc_string]
            else:
                corpus.append(doc_string)
    return corpus


def execute_crossValidation(fold_splits, corpus, labels, vectorizer):
    kf = StratifiedKFold(n_splits=fold_splits)

    totalsvm = 0  # Accuracy measure on 2000 files
    totalNB = 0
    totalMatSvm = np.zeros((2, 2));  # Confusion matrix on 2000 files
    totalMatNB = np.zeros((2, 2));

    iter=1;
    print "Starting n-fold training with number of folds:"+str(fold_splits)
    for train_index, test_index in kf.split(corpus, labels):
        #create arrays and corpuses according to current fold
        X_train = [corpus[i] for i in train_index]
        X_test = [corpus[i] for i in test_index]
        y_train, y_test = labels[train_index], labels[test_index]
        train_corpus_tf_idf = vectorizer.fit_transform(X_train)
        test_corpus_tf_idf = vectorizer.transform(X_test)

        #define and fit(train) models
        model1_linearSVC = LinearSVC()
        model2_multinomNB = MultinomialNB()
        model1_linearSVC.fit(train_corpus_tf_idf, y_train)
        model2_multinomNB.fit(train_corpus_tf_idf, y_train)

        print "Models succesfully trained, number of iteration:" + str(iter)

        #make prediction on test data
        result1 = model1_linearSVC.predict(test_corpus_tf_idf)
        result2 = model2_multinomNB.predict(test_corpus_tf_idf)

        #add partial results of current iteration to global results for all folds
        totalMatSvm = totalMatSvm + confusion_matrix(y_test, result1)
        totalMatNB = totalMatNB + confusion_matrix(y_test, result2)

        totalsvm = totalsvm + sum(y_test == result1)
        totalNB = totalNB + sum(y_test == result2)

        #iterator for logging messages
        iter = iter+1

    print str(fold_splits) + "-fold cross validation done, confusion matrices:"

    print totalMatSvm
    print totalsvm / len(labels)
    print totalMatNB
    print totalNB / len(labels)

def create_Models(corpus, labels, vectorizer):
    train_corpus_tf_idf = vectorizer.fit_transform(corpus)

    # define and fit(train) models
    model1_linearSVC = LinearSVC()
    model2_multinomNB = MultinomialNB()
    model1_linearSVC.fit(train_corpus_tf_idf, labels)
    model2_multinomNB.fit(train_corpus_tf_idf, labels)

    return model1_linearSVC, model2_multinomNB

if __name__ == "__main__":
    main(sys.argv)

reload(sys)
sys.setdefaultencoding('utf8')


