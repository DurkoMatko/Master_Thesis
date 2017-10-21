import os, csv, sys
from textblob import TextBlob
import matplotlib.pyplot as plt
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

    #analyze each tweets file
    for file in tweetFiles:
        with open(os.path.join(tweetFilesPath,file)) as csvFile:
           reader = csv.reader(csvFile, delimiter=';')

           dates,scores, flooredDates, flooredScores = getDatesAndScores1(reader)
           dates = convertDatesToPassedDays(dates)
           plotPolynomials(dates,scores,csvFile)
           flooredDates = convertDatesToPassedDays(flooredDates)
           plotPolynomials(flooredDates, flooredScores,csvFile)

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

    separator = ' '

    for row in reader:
        rowScore = sentiment1(row, included_cols);
        if (rowScore == 0 or row[4] == 'text'):
            continue;

        date = parser.parse(row[1].split(separator, 1)[0]).date()

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


    plt.plot(x, y, 'o', x_new, y_new2, '.', x_new, y_new3, '-', x_new,y_new4, '--')
    pylab.title(projectName.name)
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


