from stackapi import StackAPI,StackAPIError
from datetime import date,datetime
import nltk
import sys
import json
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf8')

def main(argv):
    [dbHandle,conn] = connectToDb()

    try:
        SITE = StackAPI('stackoverflow')
        SITE.max_pages = 1;
        questions = SITE.fetch(
                        'questions',
                        fromdate=date(2012, 5, 8),  # year,month,day
                        todate=date(2016, 4, 15),
                        tagged='django',
                        filter='withbody',
                        sort='creation'
                    )
        j = 0
        print json.dumps(questions)
        print len(questions['items'])
        #while(questions['has_more']):
        for question in questions['items']:
            print question['title']
            print datetime.fromtimestamp(int(question['creation_date'])).strftime('%Y-%m-%d')
            #print question['body']

            #nouns = extractNouns(question['body'] + question['title'])
            #saveQuestion()

            '''questions = SITE.fetch(
                'questions',
                fromdate=date(2012, 5, 8),  # year,month,day
                todate=date(2016, 4, 15),
                tagged='django',
                filter='withbody'
            )
    j = j +1
    print 'pages' + str(j)
    print 'questions' + str(i)'''


    except StackAPIError as e:
        print("   Error URL: {}".format(e.url))
        print("   Error Code: {}".format(e.code))
        print("   Error Error: {}".format(e.error))
        print("   Error Message: {}".format(e.message))

def saveQuestion():
    print 'saved'

def extractNouns(titleAndBody):
    # function to test if something is a noun
    is_noun = lambda pos: pos[:2] == 'NN'
    tokenized = nltk.word_tokenize(titleAndBody)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
    return nouns

def connectToDb():
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="root",
                           db="oss_issues")
    conn.set_character_set('utf8')

    handle = conn.cursor()
    handle.execute('SET NAMES utf8;')
    handle.execute('SET CHARACTER SET utf8;')
    handle.execute('SET character_set_connection=utf8;')
    return [handle,conn]


if __name__ == "__main__":
    main(sys.argv)

reload(sys)
sys.setdefaultencoding('utf8')


