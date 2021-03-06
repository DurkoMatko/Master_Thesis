from os import listdir,system
from os.path import isfile, join
import os
import datetime

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

		# sort dates
		sortedReleaseDates = []
		for line in content:
			sortedReleaseDates.append(line.split(" ", 1)[0])
		sortedReleaseDates.sort()

		lineNum = 0;
		# execute terminal call for each releaseDate
		for releaseDate in sortedReleaseDates:
			try:
				nextRelease = sortedReleaseDates[lineNum + 1]
			except:  # break loop if already reached last release
				break;

			#find mid-point date between 2 releases
			releaseDate = datetime.datetime.strptime(releaseDate, "%Y-%m-%d").date()
			print releaseDate
			nextRelease = datetime.datetime.strptime(nextRelease, "%Y-%m-%d").date()
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