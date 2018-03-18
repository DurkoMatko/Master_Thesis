import string
from nltk.corpus import stopwords
import nltk, re
import sys
import json
import MySQLdb
import os, csv

reload(sys)
sys.setdefaultencoding('utf8')

def main(argv):
    SUCCESS_THRESHOLD = 0.5
    [dbHandle,conn] = connectToDb()

    projects = [
        # 'https://api.github.com/repos/django/django',
        #'angularjs',
        #'bootstrap',
        'nodejs',
        #'bower',
        #'gulp',
        #'rails',
        #'vuejs',
        #'emberjs',
        #'framework',
        #'ethereum',
        #'bitcoin',
        #'rippled',
        #'dash'
        #'litecoin'
    ]

    for project in projects:
        #get Git bugs (issues) and SO question from database
        bugs_dict = getGitIssues(dbHandle=dbHandle,project=project)
        reddit_dict = getRedditDialogues(project=project)
        print "Number of bugs:" + str(len(bugs_dict))
        print "Number of questions:" + str(len(reddit_dict))

        for (rddt_id,rddt_item) in reddit_dict.iteritems():
            for (git_id, git_issue) in bugs_dict.iteritems():
                commonNouns = list(set(rddt_item[0]) & set(git_issue[0]))
                if len(commonNouns) >= len(git_issue[0])*SUCCESS_THRESHOLD and len(git_issue[0])>4:
                    if git_issue[1] != '' and "#" not in git_issue[1]:
                        print '--------------------------------------------------------------'
                        print '--------------------------------------------------------------'
                        print 'Git Issue:' + '\n' + git_issue[1]
                        print 'Stack:' + '\n' + rddt_item[1]
                        print commonNouns
                        print '\n'
                        print '\n'

        print "Done"

def getRedditDialogues(project):
    # set where to find tweets to analyze
    mypath = os.path.dirname(__file__)
    redditFilesPath = os.path.join(mypath, 'issueComments')

    rddt_dict = dict();

    with open(os.path.join(redditFilesPath, project + '.csv')) as csvFile:
        reader = csv.reader(csvFile, delimiter=';');
        reader.next();
        for row in reader:
            title = unicode(row[1])
            allComments = unicode(row[2])
            issueComment = unicode(row[3])
            # add tuple (nouns,description) and to dictionary - key is bug id
            rddt_dict[title] = (getNouns(title + " " + allComments), title + " " + allComments)
    return rddt_dict


def getGitIssues(dbHandle,project):
    sql = "Select number,title,description from just_bugs where project='" + project + "'"
    # Execute the SQL command and fetch all the rows in a list of lists.
    dbHandle.execute(sql)
    results = dbHandle.fetchall()

    bugs_dict = dict()
    for res in results:
        title = unicode(res[1])
        description = unicode(res[2])
        # add tuple (nouns,description) and to dictionary - key is bug id
        bugs_dict[int(res[0])] = (getNouns(title + " " + description), title + " " + description)

    return bugs_dict

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

def getNouns(text):
    # stopwords + punctuation set
    stop = stopwords.words('english') + list(string.punctuation)
    # tokenize text
    tokenized = nltk.word_tokenize(text)
    # extract just nouns and save them in lowercase
    nouns = [word.lower() for (word, pos) in nltk.pos_tag(tokenized) if (pos[:2] == 'NN' and word not in stop and len(word) > 3)]
    #remove duplicates
    nouns = list(set(nouns))
    return nouns

if __name__ == "__main__":
    main(sys.argv)

reload(sys)
sys.setdefaultencoding('utf8')


