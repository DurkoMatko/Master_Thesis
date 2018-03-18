from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
import nltk
import MySQLdb
import string
import os
import csv
import sys
import re
from urllib2 import urlopen, Request
import json
from Nltk_Similarity_Checker.Nltk_Similarity_Checker import Nltk_Similarity_Checker

reload(sys)
sys.setdefaultencoding('utf8')

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

def getRedditDialogues(project):
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
            #rddt_dict[title] = (getNouns(title + " " + allComments), title + " " + allComments)
            rddt_dict[title] = (getNouns(issueComment), issueComment)
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

#gets stack questions talking just about their issues
def getStackQuestionsAboutOwnIssues(dbHandle, project = None):
    if project == None:
        sql = "SELECT question_id, body, project FROM oss_issues.so_questions where body like '%/issues%' and body like CONCAT('%/',project,'/%')"
    else:
        sql = "SELECT question_id, body, project FROM oss_issues.so_questions where body like '%" + project + "/issues/%'"

    dbHandle.execute(sql)
    results = dbHandle.fetchall()

    bugs_dict = dict()
    for res in results:
        body = unicode(res[1])
        #body = preprocessStackBody(body)
        # add tuple (nouns,description) and to dictionary - key is bug id
        bugs_dict[int(res[0])] = (getNouns(body), body)

    return bugs_dict


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

def isNotNan(num):
	return num == num

def calculateAverageSimilarity(social_medium_dict,bugs_dict, similarityChecker):
	similaritySum = 0.0
	combinations = 0
	for (social_medium_id, social_medium_item) in social_medium_dict.iteritems():
		for (git_id, git_issue) in bugs_dict.iteritems():
			similarity = similarityChecker.getSimilarity(social_medium_item[1], git_issue[1])
			if isNotNan(similarity):
				similaritySum += similarity
				combinations += 1

	print "Done"
	print "SimilaritySum:" + str(similaritySum)
	print "similarityAverage: " + str(float(float(similaritySum) / float(combinations)))
	print "combinations:" + str(combinations)


#calculates similarity between Stack question and the issue its own issue it's talking about
def calcSimilarityBetweenIssueStackQuestionAndItsIssue(dbHandle, stackGitPairs, gitToken, similarityChecker):
	sql = "SELECT question_id, body, project FROM oss_issues.so_questions where body like '%/issues%' and body like CONCAT('%/',project,'/%')"

	GIT_URI = 'https://api.github.com/repos/'

	dbHandle.execute(sql)
	results = dbHandle.fetchall()

	similaritySum = 0
	similarityCount = 0

	for res in results:
		body = unicode(res[1])
		m = re.findall('issues/'+ r'\d+', body)
		if len(m) != 0:
			issueNumber = m[0][m[0].find('/'):]
			project = unicode(res[2])
			print project + '-' + issueNumber
			if issueNumber!='/887':
				#now get the issue from git
				if project == 'nodejs': project = 'node.js'
				elif project == 'ruby-on-rails': project = 'rubyonrails'
				elif project == 'vuejs': project = 'vue.js'
				elif project == 'emberjs': project = 'ember.js'

				request = Request(GIT_URI + stackGitPairs[project] + '/issues' + issueNumber)
				request.add_header('Authorization', 'token %s' % gitToken)
				response = urlopen(request).read()
				requestedIssue = json.loads(response)
				similarity = similarityChecker.getSimilarity(requestedIssue['body'], body)
				if isNotNan(similarity):
					similaritySum += similarity
					similarityCount += 1

	print 'Average similarity of own issue related questions is: ' + str(similaritySum/similarityCount)


if __name__ == '__main__':
	gitToken = "1b86fc5a9b316652471f6b124dcafb91d405ad0f"
	[dbHandle, conn] = connectToDb()

	nltk_similarity_checker = Nltk_Similarity_Checker()

	stackGitPairs = dict();
	#stackGitPairs['django'] = 'django/django';
	stackGitPairs['node.js'] = 'nodejs/node';
	stackGitPairs['angularjs'] = 'angular/angular';
	stackGitPairs['bower'] = 'bower/bower';
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

	'''similaritySum = 0.0
	combinations = 0
	maxSimilarity = 0.0
	for stackName, gitUrl in stackGitPairs.iteritems():
		bugs_dict = getGitIssues(dbHandle=dbHandle, project=gitUrl.split('/')[0])
		social_medium_dict = getStackQuestionsAboutOwnIssues(dbHandle=dbHandle, project=gitUrl)
		print gitUrl
		print "Number of bugs:" + str(len(bugs_dict))
		print "Number of questions:" + str(len(social_medium_dict))

		#calculateAverageSimilarity(social_medium_dict=social_medium_dict, bugs_dict=bugs_dict, similarityChecker=nltk_similarity_checker)
	'''

	calcSimilarityBetweenIssueStackQuestionAndItsIssue(dbHandle=dbHandle, stackGitPairs=stackGitPairs, gitToken=gitToken, similarityChecker=nltk_similarity_checker)