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

    projects = ['angularjs']

    for project in projects:
        try:
            SITE = StackAPI('stackoverflow')
            SITE.max_pages = 1;
            questions = SITE.fetch(
                            'questions',
                            fromdate=date(2012, 5, 8),  # year,month,day
                            todate=date(2016, 4, 15),
                            tagged=project,
                            filter='withbody',
                            sort='creation'
                        )
            j = 0
            print json.dumps(questions)
            print len(questions['items'])
            while(questions['has_more']):
                for question in questions['items']:
                    #print question['title']
                    #print datetime.fromtimestamp(int(question['creation_date'])).strftime('%Y-%m-%d')
                    saveQuestion(dbHandle=dbHandle, conn=conn, question=question, project=project)

                j = j + 1
                if j == 10:
                    break;

        except StackAPIError as e:
            print("   Error URL: {}".format(e.url))
            print("   Error Code: {}".format(e.code))
            print("   Error Error: {}".format(e.error))
            print("   Error Message: {}".format(e.message))

def saveQuestion(dbHandle, conn, question, project):
    dbHandle.execute(
        """INSERT INTO oss_issues.so_questions (question_id,title,creation_date,tags,body,project) VALUES (%s,%s,from_unixtime(%s),%s,%s,%s)""",
        (question['question_id'],
         question['title'],
         question['creation_date'],
         ';'.join(question['tags']),
         question['body'],
         project
         ))
    conn.commit()
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


