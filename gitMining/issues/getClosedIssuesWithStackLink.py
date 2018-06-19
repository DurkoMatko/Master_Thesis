from urllib2 import urlopen, Request
import json
import sys
import string
import MySQLdb
from stackapi import StackAPI,StackAPIError

reload(sys)
sys.setdefaultencoding('utf8')

def main(argv):
    token = "1b86fc5a9b316652471f6b124dcafb91d405ad0f"
    [dbHandle,conn] = connectToDb()

    oss_projects = [
        'https://api.github.com/repos/django/django',
        #'https://api.github.com/repos/angular/angular.js',
        #'https://api.github.com/repos/twbs/bootstrap',
        #'https://api.github.com/repos/bower/bower',
        #'https://api.github.com/repos/gulpjs/gulp',
        #'https://api.github.com/repos/rails/rails',
        #'https://api.github.com/repos/nodejs/node',
        #'https://api.github.com/repos/vuejs/vue'
        #'https://api.github.com/repos/emberjs/ember.js'
        #'https://api.github.com/repos/aurelia/framework',
        #'https://api.github.com/repos/ethereum/go-ethereum',
        #'https://api.github.com/repos/bitcoin/bitcoin',
        #'https://api.github.com/repos/ripple/rippled',
        #'https://api.github.com/repos/dashpay/dash'
        #'https://api.github.com/repos/litecoin-project/litecoin'
        ]


    for project in oss_projects:        #getIssues(project,dbHandle, conn, token)
        getBugs(project,dbHandle, conn, token)


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

def appendIssueToQuery(issue,pageNum,project):
    stringToReturn = '(' + "'" + issue['title'] + "'," + "'" + str(issue['number']) + "'," + "'" + issue['created_at'][0:(issue['created_at'].rfind('T'))] + "'," + "'" + issue['closed_at'][0:(issue['closed_at'].rfind('T'))] + "'," + "'" + issue['body'] + "'," + "'" + str(issue['labels']) + "'," + "'" + project + "')"

    if(pageNum==1):
        return stringToReturn
    return ', ' + stringToReturn

def getBugs(projectUri,dbHandle,conn,token):
    # get index of last slash
    lastSlashIndex = projectUri.rfind('/') + 1
    projectName = projectUri[lastSlashIndex:]
    if(projectName=='vue'): projectName='vue.js';
    if (projectName == 'framework'): projectName = 'aurelia';
    if (projectName == 'go-ethereum'): projectName = 'ethereum';
    if (projectName == 'rippled'): projectName = 'ripple';
    if (projectName == 'node'): projectName = 'node.js';
    print projectName

    pageNum = 1
    # request info about OSS project
    request = Request(projectUri + '/issues?state=closed&per_page=100&page=' + str(pageNum))
    request.add_header('Authorization', 'token %s' % token)
    project = urlopen(request).read()
    issues = json.loads(project)

    while (issues):
        # for each tag(release) of current OSS project
        for issue in issues:
            #convert labels to comma-separated string
            labelsList= [label['name'] for label in issue['labels']]
            labelsString = "; ".join(labelsList)

            #don't save
            #if django issue title doesn't refer to some bug number using #number format
            if(projectName=='django' and '#' not in issue['title']):
                continue;
            #if bootstrap issue isn't flagged as chosen
            if (projectName == 'bootstrap' and not any(lbl in labelsString for lbl in ['v3','v4','css','browser bug'])):
                continue;
            # if angular issue isn't flagged as bug
            if (projectName == 'angular.js' and not any(lbl in labelsString for lbl in ['type: bug'])):
                continue;
            # if gulp or bower issue isn't flagged as bug
            if ((projectName == 'gulp' or
                 projectName == 'bower') and not any(lbl in labelsString for lbl in ['bug'])):
                continue;
            if ((projectName == 'ember.js') and not any(lbl in labelsString for lbl in ['Bug'])):
                continue;
            if ((projectName == 'vue.js') and not any(lbl in labelsString for lbl in ['bug','browser quirks','1.x','2.x'])):
                continue;
            if ((projectName == 'aurelia') and not any(lbl in labelsString for lbl in ['bug','enhancement'])):
                continue;
            if ((projectName == 'node.js') and not any(lbl in labelsString for lbl in ['confirmed-bug','errors','http','install'])):
                continue;
            if ((projectName == 'ethereum') and not any(lbl in labelsString for lbl in ['bug','need fix','core','enhancement'])):
                continue;
            if ((projectName == 'bitcoin') and not any(lbl in labelsString for lbl in ['bug','mining','Data corruption','Priority High'])):
                continue;
            #dash, ripple, litecoin have small amount of issues so no need to filter them

            request2 = Request(issue['comments_url'])
            request2.add_header('Authorization', 'token %s' % token)
            commentsStr = urlopen(request2).read()
            comments = json.loads(commentsStr)
            for comm in comments:
                lookingFor = 'stackoverflow.com/questions/'
                if lookingFor in comm['body']:
                    index = comm['body'].find(lookingFor) + len(lookingFor)
                    sub = comm['body'][index:]
                    so_question_id = sub[0:sub.find('/')]

                    SITE = StackAPI('stackoverflow')
                    SITE.max_pages = 1;
                    questions = SITE.fetch('/questions/{ids}', ids=[int(so_question_id)], filter='withbody')
                    print issue['number']
                    saveMatch(dbHandle,conn,questions['items'][0], issue, projectName)
                    break;

        pageNum = pageNum + 1
        request = Request(projectUri + '/issues?state=closed&per_page=100&page=' + str(pageNum))
        request.add_header('Authorization', 'token %s' % token)
        project = urlopen(request).read()
        issues = json.loads(project)

def saveMatch(dbHandle, conn, so_question, git_issue, project):
    dbHandle.execute(
        """INSERT INTO oss_issues.git_so_matches (so_id,git_id,so_title,git_title,so_body,git_body,git_project,so_tags) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
        (so_question['question_id'],
		 git_issue['number'],
		 so_question['title'],
		 git_issue['title'],
		 so_question['body'],
		 git_issue['body'],
         "".join(l.lower() for l in project if l not in string.punctuation),
	     ';'.join(so_question['tags'])
         # project name in lowercase without punctiation
         ))
    conn.commit()

if __name__ == "__main__":
    main(sys.argv)

reload(sys)
sys.setdefaultencoding('utf8')


