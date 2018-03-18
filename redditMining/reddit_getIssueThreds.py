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

	subreddits = [#'angularjs',
				  #'RaiBlocks'
				  #'aureliajs',
				  #'bootstrap',
				  #'emberjs',
				  #'node',
				  #'vuejs',
				  #'django',
				  #'ethereum',
				  #'litecoin',
				  #'ripple',
				  #'bitcoin'
				]

	for sbrdt in subreddits:
		# open release date file
		with open(os.path.join(os.path.dirname(__file__), 'releaseDates/') + sbrdt + '.txt') as releaseDatesFile:
			with open(sbrdt+'.csv', 'w') as csvfile:
				fieldnames = ['date', 'submission_text', 'comments_text', 'issue_comment', 'subreddit']
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

					count = 0
					issueCount = 0
					for submission in reddit.subreddit(sbrdt).submissions(calendar.timegm(releaseDate.timetuple()),calendar.timegm(nextRelease.timetuple()) ):
						posted = datetime.datetime.utcfromtimestamp(submission.created_utc)
						submission.comments.replace_more()
						commentsText = ''
						issueComm = ''
						writer.writerow({'date': posted, 'submission_text': submission.title.encode('utf-8').strip(),
										 'comments_text': commentsText, 'issue_comment': issueComm, 'subreddit': sbrdt})

						count = count + 1
						if count == 50:
							break;

					print str(releaseDate) + sbrdt

				print issueCount

		csvfile.close()
		releaseDatesFile.close()

if __name__ == "__main__":
    main(sys.argv)

reload(sys)
sys.setdefaultencoding('utf8')
