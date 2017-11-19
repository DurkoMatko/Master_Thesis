from os import listdir,system
from dateutil import parser
from os.path import isfile, join
import os
import datetime

def perdelta(start, end, delta):
	result = []
	curr = start
	while curr < end:
		result.append(curr)
		curr += delta
	return result

DAY_INTERVAL = 2
TWEETS_PER_RELEASE = 30

#set where to find release dates files
mypath = os.path.join(os.path.dirname(__file__), 'releaseDates')
releaseDatefiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

#loop release date files
for oneFile in releaseDatefiles:

	#get framework name
	frameworkName = oneFile.replace(".txt","")
	if(frameworkName=='ruby on rails'): frameworkName='rubyonrails';
	print frameworkName

	with open(os.path.join(os.path.dirname(__file__), 'releaseDates/') + oneFile) as releaseDatesFile:
		#read lines of the file
		content = releaseDatesFile.read().splitlines()

		# parse dates
		dates = []
		for line in content:
			dates.append(parser.parse(line.split(" ", 1)[0]).date())

		#create list of of dates incremented by week
		searchDates = perdelta(min(dates),max(dates),delta=datetime.timedelta(weeks=1))

		lineNum = 0;
		# execute terminal call for each releaseDate
		for releaseDate in searchDates:
			try:
				nextRelease = searchDates[lineNum + 1]
			except:  # break loop if already reached last release
				break;

			#find mid-point date between 2 releases
			#releaseDate = datetime.datetime.strptime(releaseDate, "%Y-%m-%d").date()
			print releaseDate
			#nextRelease = datetime.datetime.strptime(nextRelease, "%Y-%m-%d").date()
			betweenReleases = releaseDate + (nextRelease - releaseDate)/2

			#calculate bounds
			fromDate = betweenReleases - datetime.timedelta(days=DAY_INTERVAL)
			toDate = betweenReleases + datetime.timedelta(days=DAY_INTERVAL)

			#build console command to call Tweet miner
			miningConsoleCommand = "python Exporter.py --querysearch '" + frameworkName + "' --since " + str(fromDate) + " --until " + str(toDate)  + " --lang " + "en" + " --maxtweets " + str(TWEETS_PER_RELEASE) + " --output='" + frameworkName + ".csv" + "'"

			#execute the command
			system(miningConsoleCommand)
			lineNum = lineNum + 1

print("Finished")