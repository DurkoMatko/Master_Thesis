import praw,os
from dateutil import parser
import calendar
import datetime
import csv,sys

reload(sys)
sys.setdefaultencoding('utf8')

def perdelta(start, end, delta):
	result = []
	curr = start
	while curr < end:
		result.append(curr)
		curr += delta
	return result

def main(argv):
	reddit = praw.Reddit(client_id='2Zt6cZveu6aeyg',
						 client_secret='AxBo-tVOdpzL-XcxCx94j6hr-nU',
						 user_agent='tutorialBotByMartinko',
						 username='nitramdurcek',
						 password='pipkoneviem')

	reddit.read_only = True

	redditGitPairs = dict();
	redditGitPairs['django'] = 'django/django';
	redditGitPairs['node'] = 'nodejs/node';
	redditGitPairs['angular'] = 'angular/angular';
	redditGitPairs['bower'] = 'bower';
	redditGitPairs['gulp'] = 'gulpjs/gulp';
	redditGitPairs['rubyonrails'] = 'rails/rails';
	redditGitPairs['vuejs'] = 'vuejs/vue';
	redditGitPairs['emberjs'] = 'emberjs/ember.js';
	redditGitPairs['aureliajs'] = 'aurelia/framework';
	redditGitPairs['ethereum'] = 'ethereum/go-ethereum';
	redditGitPairs['bitcoin'] = 'bitcoin/bitcoin';
	redditGitPairs['litecoin'] = 'litecoin/litecoin';
	# 'rippled',  #no stack overflow tag
	# 'dash',    #no stack overflow tag
	# 'bootstrap',   #no stack overflow tag

	for redditName, gitName in redditGitPairs.iteritems():
		# open release date file
		with open(os.path.join(os.path.dirname(__file__), 'releaseDates/') + redditName + '.txt') as releaseDatesFile:
			with open(redditName+'.csv', 'w') as csvfile:
				fieldnames = ['date', 'discussion', 'issue_comment', 'subreddit']
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
				writer.writeheader()

				content = releaseDatesFile.read().splitlines()
				# parse dates
				dates = []
				for line in content:
					dates.append(parser.parse(line.split(" ", 1)[0]).date())

				# create list of of dates incremented by week
				searchDates = perdelta(min(dates), max(dates), delta=datetime.timedelta(weeks=1))
				for idx,releaseDate in enumerate(searchDates):
					try:
						nextRelease = searchDates[idx + 1]
						#print "Between " + str(releaseDate) + " and " + str(nextRelease)
					except:  # break loop if already reached last release
						break;

					for submission in reddit.subreddit(redditName).submissions(calendar.timegm(releaseDate.timetuple()),calendar.timegm(nextRelease.timetuple()) ):
						posted = datetime.datetime.utcfromtimestamp(submission.created_utc)
						submission.comments.replace_more()
						issueRelated = False
						wholeDiscussion = submission.title.encode('utf-8').strip() + ' '
						for comment in submission.comments:
							issueRelated = issueRelated or (gitName + '/issues') in comment.body
							wholeDiscussion += comment.body + ' '

						if issueRelated:
							writer.writerow({'date': posted, 'discussion': wholeDiscussion, 'issue_comment': issueRelated, 'subreddit': redditName})

					print str(releaseDate) + redditName

		csvfile.close()
		releaseDatesFile.close()

if __name__ == "__main__":
    main(sys.argv)

reload(sys)
sys.setdefaultencoding('utf8')
