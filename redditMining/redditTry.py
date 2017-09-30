import praw
from datetime import datetime, timedelta,date

reddit = praw.Reddit(client_id='2Zt6cZveu6aeyg',
                     client_secret='AxBo-tVOdpzL-XcxCx94j6hr-nU',
                     user_agent='tutorialBotByMartinko',
                     username='nitramdurcek',
                     password='pipkoneviem')

reddit.read_only = True
i=1
for submission in reddit.subreddit('jquery').hot(limit=600):
	posted = datetime.utcfromtimestamp(submission.created_utc).date()
	beforeRelease = date(2016, 6, 8)
	afterRelease = date(2016, 6, 30)
	if(posted > beforeRelease and posted<afterRelease):
		print(posted)
		print(submission.title.encode('utf-8').strip())
		submission.comments.replace_more()
		print(len(submission.comments))
	

