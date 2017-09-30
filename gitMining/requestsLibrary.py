import requests
from github import Github
import json
import sys


reload(sys)
sys.setdefaultencoding('utf8')

def main(argv):
	g = Github("DurkoMatko", "Pipkoneviem59")
	for repo in g.get_user().get_repos():
		print repo.name

	oss_projects = ['https://api.github.com/repos/django/django'] #,'https://api.github.com/repos/angular/angular.js','https://api.github.com/repos/twbs/bootstrap','https://api.github.com/repos/nodejs/node'

	f = open('releaseDates.txt', 'w')
	alreadyOne = 0

	for projectUri in oss_projects:
		project = requests.get(projectUri + "/git/refs/tags")
		print project
		if(project.ok):
			tags = json.loads(project.text or project.content)
			for tag in tags:
				#if (alreadyOne == 24):
				#	sys.exit("Error message")

				got_object = tag['object']
				detailedUrl = got_object['url']
				detailedUrlContent = requests.get(detailedUrl)
				print detailedUrlContent 
				print got_object
				if(detailedUrlContent.ok):
					repoReleaseDetails = json.loads(detailedUrlContent.text or detailedUrlContent.content)
					tagger = repoReleaseDetails['tagger']
					releaseDate = tagger['date']
					print releaseDate
					f.write(releaseDate + '\n')
					alreadyOne = alreadyOne + 1


	f.close()

			#releases = repoItem['releases_url'].replace("{/id}", "/tags")
			#print releases
			#tags = requests.get(releases)
			#tagsItem = json.loads(tags.text or tags.content)
			#print tagsItem


if __name__ == "__main__":
    main(sys.argv)


reload(sys)
sys.setdefaultencoding('utf8')