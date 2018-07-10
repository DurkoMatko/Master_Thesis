from urllib2 import urlopen, Request
import json
import sys
import urllib2
import re

reload(sys)
sys.setdefaultencoding('utf8')

def main(argv):

	oss_projects_git_ui_navigation = dict()
	oss_projects_git_ui_navigation['https://api.github.com/repos/angular/angular.js']= "https://github.com/angular/angular.js/releases/tag/"
	oss_projects_git_ui_navigation['https://api.github.com/repos/nodejs/node'] = "https://github.com/nodejs/node/releases/tag/"
	oss_projects_git_ui_navigation['https://api.github.com/repos/vuejs/vue'] = "https://github.com/vuejs/vue/releases/tag/"
	oss_projects_git_ui_navigation['https://api.github.com/repos/emberjs/ember.js'] = "https://github.com/emberjs/ember.js/releases/tag/"
	oss_projects_git_ui_navigation['https://api.github.com/repos/laravel/laravel'] = "https://github.com/laravel/laravel/releases/tag/"
	oss_projects_git_ui_navigation['https://api.github.com/repos/cakephp/cakephp'] = "https://github.com/cakephp/cakephp/releases/tag/"
	oss_projects_git_ui_navigation['https://api.github.com/repos/symfony/symfony'] = "https://github.com/symfony/symfony/releases/tag/"
	oss_projects_git_ui_navigation['https://api.github.com/repos/bower/bower'] = "https://github.com/bower/bower/releases/tag/"
	oss_projects_git_ui_navigation['https://api.github.com/repos/gulpjs/gulp'] = "https://github.com/gulpjs/gulp/releases/tag/"



	oss_projects = [
		#'https://api.github.com/repos/django/django',
		#'https://api.github.com/repos/angular/angular.js',
		#'https://api.github.com/repos/twbs/bootstrap',
		#'https://api.github.com/repos/nodejs/node',
		#'https://api.github.com/repos/bower/bower',
		'https://api.github.com/repos/gulpjs/gulp',
		#'https://api.github.com/repos/rails/rails',
		#'https://api.github.com/repos/vuejs/vue',
		#'https://api.github.com/repos/emberjs/ember.js',
		#'https://api.github.com/repos/aurelia/framework',
		#'https://api.github.com/repos/ethereum/go-ethereum',
		#'https://api.github.com/repos/bitcoin/bitcoin',
		#'https://api.github.com/repos/ripple/rippled',
		#'https://api.github.com/repos/dashpay/dash'
		#'https://api.github.com/repos/litecoin-project/litecoin'
		#'https://api.github.com/repos/monero-project/monero'
		#'https://api.github.com/repos/laravel/laravel'
		#'https://api.github.com/repos/symfony/symfony'
		#'https://api.github.com/repos/yiisoft/yii'
		#'https://api.github.com/repos/cakephp/cakephp'
	]
	token = "1b86fc5a9b316652471f6b124dcafb91d405ad0f"

	for projectUri in oss_projects:
		#get index of last slash
		lastSlashIndex = projectUri.rfind('/') + 1
		#create and open txt file with name of currently examined OSS project
		f = open('./releaseDates/' + projectUri[lastSlashIndex:] + '_commits.txt', 'w')
		
		#request info about OSS project
		request = Request(projectUri + "/git/refs/tags")
		request.add_header('Authorization', 'token %s' % token)
		project = urlopen(request).read()
		tags = json.loads(project)

		#for each tag(release) of current OSS project
		for tag in tags:
			version = tag['ref']
			got_object = tag['object']
			detailedUrl = got_object['url']

			#request details of particular release
			request = Request(detailedUrl)
			request.add_header('Authorization', 'token %s' % token)

			#get the person responsible for the release
			repoReleaseDetails = json.loads(urlopen(request).read())
			if 'tagger' in repoReleaseDetails:
				tagger = repoReleaseDetails['tagger']
			elif 'author' in repoReleaseDetails:
				tagger = repoReleaseDetails['author']
			else:
				tagger = repoReleaseDetails['committer']

			#get the date of the particular release
			releaseDate = tagger['date']
			#strip time from the date
			justDate = releaseDate[0:(releaseDate.rfind('T'))]
			print justDate
			versionParsed = version.replace("refs/tags/", "")

			#crawling git and getting number of commits
			try:
				urlToOpen = oss_projects_git_ui_navigation[projectUri] + versionParsed
				response = urllib2.urlopen(urlToOpen)
				page_source = response.read()
				numberOfCommits = getCommitsOfRelease(page_source, versionParsed)
				f.write(justDate + " (" + versionParsed + ") " + numberOfCommits + "\n")
			except urllib2.HTTPError:
				f.write(justDate + " (" + versionParsed + ") 0\n")


		#close file for current OSS project 	
		f.close()

def getCommitsOfRelease(page_source, versionParsed):
	searchText = "/compare/" + versionParsed + "...dev"
	commitsIndex = page_source.find(searchText)
	if commitsIndex == -1:
		searchText = "/compare/" + versionParsed + "...master"
		commitsIndex = page_source.find(searchText)
	if commitsIndex == -1:
		searchText = "/compare/" + versionParsed + "...beta"
		commitsIndex = page_source.find(searchText)
	arr = re.findall(r'\d+', page_source[commitsIndex + len(searchText):commitsIndex + len(searchText) + 30])
	if (len(arr) > 1):
		numberOfCommits = arr[1]
	else:
		numberOfCommits = arr[0]
	print numberOfCommits
	return numberOfCommits

if __name__ == "__main__":
    main(sys.argv)


reload(sys)
sys.setdefaultencoding('utf8')
