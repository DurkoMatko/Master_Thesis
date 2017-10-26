import os, csv, sys
from textblob import TextBlob
from matplotlib import pyplot
from matplotlib import pylab
from dateutil import parser
import numpy as np

reload(sys)
sys.setdefaultencoding('utf8')

def main(argv):
    #set where to find release dates files
    mypath = os.path.dirname(__file__)
    tweetFilesPath = os.path.join(mypath, 'tweets_To_Analyze')
    tweetFiles = [f for f in os.listdir(tweetFilesPath) if os.path.isfile(os.path.join(tweetFilesPath, f))]

    execute_crossValidation(dir='datasets/Sentiment140')

    #analyze each tweets file
    for file in tweetFiles:
        with open(os.path.join(tweetFilesPath,file)) as csvFile:
           reader = csv.reader(csvFile, delimiter=';')

           dates,scores, flooredDates, flooredScores = getDatesAndScores1(reader)
           dates = convertDatesToPassedDays(dates)
           plotPolynomials(dates,scores,file)
           flooredDates = convertDatesToPassedDays(flooredDates)
           plotPolynomials(flooredDates, flooredScores,file)

           csvFile.close()


######################### TextBlob sentiment analysis helper funcions ############################

def getDatesAndScores1(reader):
    included_cols = [1, 4]
    sentimentScoresDict = dict()
    flooredSentimentScoresDict = dict()
    dateCounts = dict()
    flooredDateCounts = dict()
    averageScores = dict()
    flooredAverageScores = dict()

    for row in reader:
        rowScore = sentiment1(row, included_cols);
        if (rowScore == 0 or row[4] == 'text'):
            continue;

        date = parser.parse(row[1].split(' ', 1)[0]).date()

        if (date in sentimentScoresDict):
            sentimentScoresDict[date] = sentimentScoresDict[date] + rowScore
            dateCounts[date] = dateCounts[date] + 1;
            date = date.replace(day=1)
            flooredSentimentScoresDict[date] = flooredSentimentScoresDict[date] + rowScore
            flooredDateCounts[date] = flooredDateCounts[date] + 1;
        else:
            sentimentScoresDict[date] = rowScore
            dateCounts[date] = 1;
            date = date.replace(day=1)
            flooredSentimentScoresDict[date] = rowScore
            flooredDateCounts[date] = 1

    for date, scoreSum in sentimentScoresDict.iteritems():
        averageScores[date] = scoreSum / dateCounts[date]

    i = 1
    for flooredDate, scoreSum in flooredSentimentScoresDict.iteritems():
        flooredAverageScores[flooredDate] = scoreSum / flooredDateCounts[flooredDate]
        i = i + 1
        print i


    return averageScores.keys(), averageScores.values(), flooredAverageScores.keys(), flooredAverageScores.values()


def sentiment1(row, included_columns):
    content = list(row[i] for i in included_columns)
    wiki = TextBlob(content[1])
    return wiki.sentiment.polarity


def plotPolynomials(dates,scores,projectName):
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


    pyplot.plot(x, y, 'o', x_new, y_new2, '.', x_new, y_new3, '-', x_new,y_new4, '--')
    pylab.title(projectName)
    pyplot.show()


def convertDatesToPassedDays(dates):
    minDate = min(dates)
    passedDays = []

    for date in dates:
        passedDays.append(abs((date - minDate).days))
    return passedDays

def execute_crossValidation(dir):
    mypath = os.path.dirname(__file__)
    trainDataPath = os.path.join(mypath, dir)
    trainDataFiles = [f for f in os.listdir(trainDataPath) if os.path.isfile(os.path.join(trainDataPath, f))]

    labels = []
    scores = []
    for file in trainDataFiles:
        with open(os.path.join(mypath, dir+'/') + file) as trainingFile:
            reader = csv.reader(trainingFile, delimiter=',')
            i = 0
            #for each tweet in file
            for row in reader:
                #if it's either positive or negative
                    #add the tweet to corpus
                    score = TextBlob(unicode(row[5], errors='ignore')).sentiment.polarity

                    if(score>0):
                        scores.append(1)
                    elif(score==0.0):scores.append(2)
                    else:
                        scores.append(0)
                    #add positive or negative label
                    if (row[0] == "0"):
                        labels.append(0)
                    elif(row[0] == "2"):labels.append(2)
                    elif (row[0] == "4"):
                        labels.append(1)

                    i = i + 1
                    if (i % 10000 == 0):
                        print i;

        trainingFile.close()

    labels = np.array(labels)
    scores = np.array(scores)
    print "Accuracy of Textblob sentiment is: " + str((sum(labels == scores)*1.0)/len(scores))

if __name__ == "__main__":
    main(sys.argv)

reload(sys)
sys.setdefaultencoding('utf8')


