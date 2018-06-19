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
import matplotlib.pyplot as plt
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

def getRedditDialogueAndComment(project):
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
            rddt_dict[title] = (allComments, issueComment)
    return rddt_dict


def getGitBugs(dbHandle,project):
    if project == 'angular': project = 'angularjs'
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


#calculates similarity between Stack question and its own issue it's talking about
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

def compareSimilarityOfOwnIssue_CommentVsDiscussion(redditGitPairs,similarityChecker):
	GIT_URI = 'https://api.github.com/repos/'
	similarityCommentSum = 0.0
	similarityDiscussionSum = 0.0
	similarityCount = 0
	commentSimilarities = list()
	commentsLength = list()
	discussionSimilarities = list()
	discussionLength = list()
	for redditName, gitUrl in redditGitPairs.iteritems():
		reddit_dict = getRedditDialogueAndComment(redditName)
		for redditTitle, redditDiscussionAndComment in reddit_dict.iteritems():
			if gitUrl + '/issues' in redditDiscussionAndComment[1]:
				m = re.findall('issues/' + r'\d+', redditDiscussionAndComment[1])
				issueNumber = m[0][m[0].find('/'):]

				request = Request(GIT_URI + gitUrl + '/issues' + issueNumber)
				request.add_header('Authorization', 'token %s' % gitToken)
				response = urlopen(request).read()
				requestedIssue = json.loads(response)
				similarity = similarityChecker.getSimilarity(requestedIssue['body'], redditDiscussionAndComment[1])
				if isNotNan(similarity):
					commentSimilarities.append(similarity)
					commentsLength.append(len(redditDiscussionAndComment[1]))
					similarityCommentSum += similarity
					similarityCount += 1
				similarity = similarityChecker.getSimilarity(requestedIssue['body'], redditDiscussionAndComment[0])
				if isNotNan(similarity):
					discussionSimilarities.append(similarity)
					discussionLength.append(len(redditDiscussionAndComment[0]))
					similarityDiscussionSum += similarity

		print "Done " + redditName
		#print "similarityCommentAverage: " + str(float(float(similarityCommentSum) / float(similarityCount)))
		#print "similarityDiscussionAverage: " + str(float(float(similarityDiscussionSum) / float(similarityCount)))

		similarityCommentSum = 0.0
		similarityDiscussionSum = 0.0
		similarityCount = 0

	print "Done "
	#print "similarityCommentAverage: " + str(float(float(similarityCommentSum) / float(similarityCount)))
	#print "similarityDiscussionAverage: " + str(float(float(similarityDiscussionSum) / float(similarityCount)))
	print "similarityCommentsList: " + str(commentSimilarities)
	print "similarityDiscussionList: " + str(discussionSimilarities)

	showSimilarityVsLengthRelationship(commentsLength,commentSimilarities)


# indexOfIssue = redditDiscussionAndComment[1].find(gitUrl+'/issues')
			# startIndex = redditDiscussionAndComment[1][:indexOfIssue].rfind(' ')

def showSimilarityVsLengthRelationship(length,similarityScore):
	plt.plot(length, similarityScore, 'o')
	plt.title("Relationship between similarity score and length of comment")
	plt.ylabel('Similarity')
	plt.xlabel('Comment length')
	plt.show()

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

	redditGitPairs = dict();
	# stackGitPairs['django'] = 'django/django';
	redditGitPairs['nodejs'] = 'nodejs/node';
	redditGitPairs['angularjs'] = 'angular/angular';
	redditGitPairs['vuejs'] = 'vuejs/vue';
	redditGitPairs['emberjs'] = 'emberjs/ember.js';

	for redditName, gitUrl in redditGitPairs.iteritems():
		reddit_dict = getRedditDialogues(redditName)
		bugs_dict = getGitBugs(dbHandle=dbHandle, project=gitUrl.split('/')[0])
		print redditName
		print "Number of bugs:" + str(len(bugs_dict))
		print "Number of questions:" + str(len(reddit_dict))

		#calculateAverageSimilarity(social_medium_dict=reddit_dict, bugs_dict=bugs_dict, similarityChecker=nltk_similarity_checker)


	#COMPARING SIMILARITY OF THE ISSUE COMMENT AND THE REST OF THE THREAD
	#compareSimilarityOfOwnIssue_CommentVsDiscussion(redditGitPairs=redditGitPairs, similarityChecker=nltk_similarity_checker)
	
