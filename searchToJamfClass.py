# Populate students into a class from the usernames of an advanced search
# No need to determine who was in the class as the full member list is loaded each time 
# since there is no add/remove function in the Jamf API
# Authored by Brad Schmidt on 2/7/2018

import requests # Please install/acquire requests. 
import logging
import os

# Update for your environment 
# JSS User Account with access to: 
#   Advanced Mobile Device Search - Read
#   Classes - Read, Update
#   Mobile Devices - Read
#   Users - Read
JSS_USERNAME = 'API_USER' 
JSS_PASSWORD = 'potato'
JSS_URL = 'https://jss.example.com:8443' # Please include the port number

SEARCH_ID = 1 # Advanced Search ID
CLASS_ID = 1 # Create class beforehand with desired teachers

# --- You should not need to edit below this line ---
# Some light logging
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=SITE_ROOT + "/results.log",
					level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)

# Get list of usernames from advanced search 
r = requests.get(JSS_URL + '/JSSResource/advancedmobiledevicesearches/id/' + str(SEARCH_ID), 
	headers={'Accept': 'application/json'}, 
	auth=(JSS_USERNAME,JSS_PASSWORD))

if r.status_code == 200:
	logging.info('Received results from Advanced Search')
else:
	logging.error('Did not receive results')
	exit(1)

# Extract search results	
results = r.json()['advanced_mobile_device_search']['mobile_devices']

# Format for XML <student>username</student>
students = ''
for user in results:
	students = students + '<student>' + user['Username'] + '</student>'
	
# Build the XML
classXML = '<class><students>{}</students></class>'.format(students)

# Submit the PUT request to update the class 
r = requests.put(JSS_URL + '/JSSResource/classes/id/' + str(CLASS_ID), 
	data=classXML, headers={'Content-Type': 'application/xml'}, 
	auth=(JSS_USERNAME,JSS_PASSWORD))

if r.status_code == 201:
	logging.info('Updated the class successfully')
else:
	logging.error('Update Failed')
	exit(1)


