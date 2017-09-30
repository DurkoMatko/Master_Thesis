# get Facebook access token from environment variable
# Facebook Graph API Example in Python
# by James Thornton, http://jamesthornton.com

# Facebook API Docs
# https://developers.facebook.com/docs/graph-api/using-graph-api#reading

# Get Your Facebook Access Token Here...
# https://developers.facebook.com/tools/explorer/145634995501895/?method=GET&path=me

# Before running this script...
# Set your Facebook Access Token as an environment variable in your terminal:
# $ export ACCESS_TOKEN={YOUR ACCESS TOKEN}

# To download this script, use the curl command...
# $ curl -O https://gist.githubusercontent.com/espeed/11114604/raw/a233d14604ea44f9d29af02cd2768b91caaad7af/fbme.py

# To run this script, use the python command to execute the script in your terminal...
# $ python fbme.py

import os
import json
import urllib
import pprint

# get Facebook access token from environment variable

if "FACEBOOK_ACCESS_TOKEN" in os.environ:
	print os.environ["FACEBOOK_ACCESS_TOKEN"]
	ACCESS_TOKEN = os.environ["FACEBOOK_ACCESS_TOKEN"]


	# build the URL for the API endpoint
	host = "https://graph.facebook.com"
	path = "/me"
	params = urllib.urlencode({"access_token": ACCESS_TOKEN})

	url = "{host}{path}?{params}".format(host=host, path=path, params=params)

	# open the URL and read the response
	resp = urllib.urlopen(url).read()

	# convert the returned JSON string to a Python datatype 
	me = json.loads(resp)

	# display the result
	pprint.pprint(me)