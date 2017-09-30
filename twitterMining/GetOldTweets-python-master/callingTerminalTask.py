from os import listdir,system
from os.path import isfile, join
import os
import datetime

DAY_INTERVAL = 10

#set where to find release dates files
print(os.path.dirname(__file__))
mypath = os.path.join(os.path.dirname(__file__), 'releaseDates')
releaseDatefiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

#loop release date files
for oneFile in releaseDatefiles:

	#get framework name
	frameworkName = oneFile.replace(".txt","")
	print frameworkName

	with open(os.path.join(os.path.dirname(__file__), 'releaseDates/') + oneFile) as releaseDatesFile:
		#read lines of the file
		content = releaseDatesFile.read().splitlines() 

		#execute terminal call for each releaseDate
		for line in content:

			#strip the line to get releaseDate and version
			releaseDate = line.split(" ",1)[0]
			version = line.split(" ",1)[1]
			version = version[1:len(version)-1]

			#create date object
			releaseDate = datetime.datetime.strptime(releaseDate, "%Y-%m-%d").date()

			#calculate bounds
			beforeRelease = releaseDate - datetime.timedelta(days=DAY_INTERVAL)
			afterRelease = releaseDate + datetime.timedelta(days=DAY_INTERVAL)

			#build console command to call Tweet miner
			#miningConsoleCommand = "python Exporter.py --querysearch '" + frameworkName + " AND " + version + "' --since " + str(releaseDate) + " --until " + str(afterRelease) + " --maxtweets 1000 --output='" + frameworkName + "_" + str(releaseDate) + ".csv" + "'"
			#miningConsoleCommand = "python Exporter.py --querysearch '" + frameworkName + " AND " + version + "' --since " + str(releaseDate) + " --maxtweets 1000 --output='" + frameworkName + "_" + str(releaseDate) + ".csv" + "'"
			print afterRelease;
			miningConsoleCommand = "python Exporter.py --querysearch '" + frameworkName + " AND " + version + "' --since " + str(releaseDate) + " --until " + str(afterRelease) + " --output='" + frameworkName + "_" + str(releaseDate) + ".csv" + "'"
			#miningConsoleCommand = "python Exporter.py --querysearch '" + frameworkName + " " + version + "' --since " + str(releaseDate) + " --until " + str(afterRelease) + " --maxtweets 1000 --output='" + frameworkName + "_" + str(releaseDate) + ".csv" + "'"

			#execute the command
			system(miningConsoleCommand)

print("done")