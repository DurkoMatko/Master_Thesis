from stackapi import StackAPI,StackAPIError
from datetime import date,datetime
import nltk
import sys
import json
import MySQLdb
import string

reload(sys)
sys.setdefaultencoding('utf8')

def main(argv):
    [dbHandle,conn] = connectToDb()

    projects = [
        # 'https://api.github.com/repos/django/django',
        #'angularjs',
        #'bootstrap',   #no stack overflow tag
        #'node.js',
        #'bower',
        #'gulp',
        #'ruby-on-rails',
        #'vue.js',
        #'ember.js',
        'aurelia',
        #'go-ethereum',
        'ethereum',
        #'bitcoin',
        #'rippled',  #no stack overflow tag
        #'dash',    #no stack overflow tag
        #'litecoin'
    ]

    for project in projects:
        print project
        try:
            page=1
            SITE = StackAPI('stackoverflow')
            SITE.max_pages = 1;
            while True:
                questions = SITE.fetch(
                    'questions',
                    fromdate=date(2012, 5, 8),  # year,month,day
                    todate=date(2016, 4, 15),
                    tagged=project,
                    filter='withbody',
                    sort='creation',
                    page=page
                )
                print len(questions['items'])
                for question in questions['items']:
                    #print question['title']
                    #print datetime.fromtimestamp(int(question['creation_date'])).strftime('%Y-%m-%d')
                    if project == 'go-ethereum': project = 'ethereum'
                    saveQuestion(dbHandle=dbHandle, conn=conn, question=question, project=project)

                page = page + 1
                if page == 11 or not questions['has_more']:
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
         "".join(l.lower() for l in project if l not in string.punctuation)
         # project name in lowercase without punctiation
         ))
    conn.commit()

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


