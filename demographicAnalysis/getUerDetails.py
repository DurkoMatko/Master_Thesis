import tweepy,os,csv

auth = tweepy.OAuthHandler("zzzpwKuwGyls73SOKqL47upvH", "smd6wmph00nLSdDaASpEU4Pr1lwSr7jhUFvFCaC66zdAbBx7PO")
auth.set_access_token("827898364217982976-9e4EabQIFOMHmxuVSMiBShbp6xG4iNH", "vkIRpveBVnZh1yu8vzEOCHBi1e2DuopziwudsoZbGjZYv")
api = tweepy.API(auth,wait_on_rate_limit=True)


mypath = os.path.dirname(__file__)
tweetFilesPath = os.path.join(mypath, 'tweets_To_Analyze')
tweetFiles = [f for f in os.listdir(tweetFilesPath) if os.path.isfile(os.path.join(tweetFilesPath, f))]

# analyze each tweets file
for file in tweetFiles:
	with open(os.path.join(tweetFilesPath, file)) as csvFile:
		reader = csv.reader(csvFile, delimiter=';')
		i = 0
		for row in reader:
			i=i+1
			if row[4] == "text":
				continue
			user = api.get_user(row[0])
			print user.name
			if user.geo_enabled:
				print user.location
			if i == 100:
				break;

