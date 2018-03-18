from stackapi import StackAPI,StackAPIError
from datetime import date,datetime
import nltk
import sys
import json
import MySQLdb
import string

reload(sys)
sys.setdefaultencoding('utf8')

############# API THROTTLE PROBLEM !!!!!!!!!!! #######################
def main(argv):
    [dbHandle,conn] = connectToDb()

    stackGitPairs = dict();
    stackGitPairs['django'] = 'django/django';
    stackGitPairs['node.js'] = 'nodejs/node';
    stackGitPairs['angularjs'] = 'angular/angular';
    stackGitPairs['bower'] = 'bower';
    stackGitPairs['gulp'] = 'gulpjs/gulp';
    stackGitPairs['ruby-on-rails'] = 'rails/rails';
    stackGitPairs['vue.js'] = 'vuejs/vue';
    stackGitPairs['ember.js'] = 'emberjs/ember.js';
    stackGitPairs['aurelia'] = 'aurelia/framework';
    stackGitPairs['ethereum'] = 'ethereum/go-ethereum';
    stackGitPairs['bitcoin'] = 'bitcoin/bitcoin';
    stackGitPairs['litecoin'] = 'litecoin/litecoin';
    # 'rippled',  #no stack overflow tag
    # 'dash',    #no stack overflow tag
    # 'bootstrap',   #no stack overflow tag


    for stackName, gitName in stackGitPairs.iteritems():
        print stackName
        try:
            page=5
            commentCount = 0
            SITE = StackAPI('stackoverflow')
            SITE.max_pages = 1;
            while True:
                questions = SITE.fetch(
                    'questions',
                    fromdate=date(2012, 5, 8),  # year,month,day
                    todate=date(2016, 4, 15),
                    tagged=stackName,
                    filter='withbody',
                    sort='creation',
                    page=page
                )
                print len(questions['items'])
                for question in questions['items']:
                    #print question['title']
                    #print datetime.fromtimestamp(int(question['creation_date'])).strftime('%Y-%m-%d')
                    answers = SITE.fetch('questions/' + str(question['question_id']) + '/answers',
                                         min=10,
                                         sort='votes',
                                         filter='withbody')
                    for answer in answers['items']:
                        commentCount += 1
                        if gitName + '/issues' in answer['body']:
                            saveComment(dbHandle=dbHandle, conn=conn, answer=answer, question_id=question['question_id'], project=stackName)

                page = page + 1
                if page == 11 or not questions['has_more']:
                    break;

            print 'answer count:' + str(commentCount)

        except StackAPIError as e:
            print("   Error URL: {}".format(e.url))
            print("   Error Code: {}".format(e.code))
            print("   Error Error: {}".format(e.error))
            print("   Error Message: {}".format(e.message))

def saveComment(dbHandle, conn, answer, question_id, project):
    dbHandle.execute(
        """INSERT INTO oss_issues.so_issue_comments (question_id,comment_id,comment_body,project) VALUES (%s,%s,%s,%s)""",
        (question_id,
         answer['answer_id'],
         answer['body'],
         "".join(l.lower() for l in project if l not in string.punctuation)
         # project name in lowercase without punctiation
         ))
    conn.commit()

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


