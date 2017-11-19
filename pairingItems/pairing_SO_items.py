import string
from nltk.corpus import stopwords
import nltk, re
import sys
import json
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf8')

def main(argv):
    SUCCESS_THRESHOLD = 0.5
    [dbHandle,conn] = connectToDb()

    projects = [
        # 'https://api.github.com/repos/django/django',
        #'angularjs',
        #'bootstrap',
        #'node',
        #'bower',
        #'gulp',
        #'rails',
        #'vuejs',
        'emberjs',
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
        so_dict = getStackQuestions(dbHandle=dbHandle,project=project)
        print "Number of bugs:" + str(len(bugs_dict))
        print "Number of questions:" + str(len(so_dict))

        for (so_id,so_item) in so_dict.iteritems():
            for (git_id, git_issue) in bugs_dict.iteritems():
                commonNouns = list(set(so_item[0]) & set(git_issue[0]))
                if len(commonNouns) >= len(git_issue[0])*SUCCESS_THRESHOLD and len(git_issue[0])>4:
                    if git_issue[1] != '' and "#" not in git_issue[1]:
                        print '--------------------------------------------------------------'
                        print '--------------------------------------------------------------'
                        #print 'Git Issue:' + '\n' + git_issue[1]
                        #print 'Stack:' + '\n' + so_item[1]
                        print commonNouns
                        #print '\n'
                        #print '\n'

        print "Done"

def getStackQuestions(dbHandle,project):
    sql = "Select question_id,title,body from so_questions where project='" + project + "'"
    # Execute the SQL command and fetch all the rows in a list of lists.
    dbHandle.execute(sql)
    so_items = dbHandle.fetchall()

    so_dict = dict()
    for so_item in so_items:
        # add tuple (nouns,questionText) and question id to dictionary
        title = unicode(so_item[1])
        body = preprocessStackBody(unicode(so_item[2]))
        so_dict[int(so_item[0])] = (getNouns(title + " "+ body), title + " "+ body)

    return so_dict

def preprocessStackBody(questionBody):
    #remove code snippets - re.sub('<code>.*?</code>', '', questionBody) doesn't work
    #while there is opening and closing tag, replace the text among them
    while('<code>' in questionBody and '</code>' in questionBody ):
        start = questionBody.index('<code>')
        end = questionBody.index('</code>')
        #if indexes don't make sense
        if start > end:
            break
        #get code within <pre><code> ... </pre></code>
        code = questionBody[start-len('<pre>'):end+len('</code></pre>')]
        questionBody = questionBody.replace(code,'')

    #get rid of links
    questionBody = re.sub('<a href=.*?</a>', '', questionBody)

    return questionBody

def getGitIssues(dbHandle,project):
    sql = "Select number,title,description from just_bugs where project='" + project + "'"
    # Execute the SQL command and fetch all the rows in a list of lists.
    dbHandle.execute(sql)
    results = dbHandle.fetchall()

    bugs_dict = dict()
    for res in results:
        title = unicode(res[1])
        description = unicode(res[2])
        # add tuple (nouns,description) and bug id to dictionary
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


