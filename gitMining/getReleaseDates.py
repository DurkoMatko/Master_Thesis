from urllib2 import urlopen, Request
from github import Github
import json
import sys


reload(sys)
sys.setdefaultencoding('utf8')

def main(argv):
	oss_projects = ['https://api.github.com/repos/django/django','https://api.github.com/repos/angluar/angular.js']
	token = "1b86fc5a9b316652471f6b124dcafb91d405ad0f"

	for projectUri in oss_projects:
		#get index of last slash
		lastSlashIndex = projectUri.rfind('/') + 1
		#create and open txt file with name of currently examined OSS project
		f = open('./releaseDates/' + projectUri[lastSlashIndex:] + '.txt', 'w')
		
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
			f.write(justDate + " (" + version.replace("refs/tags/", "") + ")\n")

		#close file for current OSS project 	
		f.close()

if __name__ == "__main__":
    main(sys.argv)


reload(sys)
sys.setdefaultencoding('utf8')
