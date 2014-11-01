
#---UPDATES-------------------------------------------------
# - Moved API keys into assets.
#-----------------------------------------------------------

import oauth2 as oauth
import json, sys, re
import time, csv
from datetime import datetime
from keys import *


#PROMPT SEARCH TERMS / VOLUME
print ' TWEET FETCH (RESTING API)'
print ' ================================='
searchTerm          = raw_input (' * What are your search terms? ')
desired_max_count   = input     (' * How many tweets do you want? ')
geoflag             = raw_input (' * Do you need geo coordinates? (YES or NO) ')

pingtime = datetime.now().strftime('%H%M - ')
searchTerm = re.sub(r'#',"%23", searchTerm)

#COUNT CYCLES
MAX_RESULTS_FROM_TWITTER = 100
loopcount = desired_max_count / MAX_RESULTS_FROM_TWITTER


#NOTIFY USER, PAUSE
print '\n ---------------------------------'
print ' * ' + str(loopcount) + ' SETS IN DESIRED FETCH QUEUE'
print ' * STARTING IN (2) SECONDS.'
time.sleep(2)


#CREATE THE URL
def makeurl(searchterm, max_id=0) :
    baseurl = "https://api.twitter.com/1.1/search/tweets.json"
    count = "100"
    if max_id == 0:
        url = baseurl + '?q=' + searchterm + '&' \
              + 'count=' + count    
    else:
        url = baseurl + '?q=' + searchterm + '&' \
              + 'max_id=' + str(max_id) + '&' \
              + 'count=' + count    
    return url 
url = makeurl(searchTerm)


# OAUTH / CLIENT AUTH
token = oauth.Token(token_key, token_secret)
consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer, token)


if (geoflag == 'YES') or (geoflag == 'yes') or (geoflag == 'y') or (geoflag == 'Y'):
    
    # GEO OUTPUT LOOP
    localfile = open((pingtime + 'fetch.csv'),'w')
    print '\n ---------------------------------'
    for i in range(loopcount):
        header, contents = client.request(url, method="GET")
        data = json.loads(contents)
        print ' * FETCH #' + str(i+1) + ' | SUCCESS!'
        results = len(data['statuses'])  
        
        for j in range(results):
            if data['statuses'][j]['coordinates'] != None : #COORDS MUST EXIST
                tweet= data['statuses'][j]['text']
                date = data['statuses'][j]['created_at']
                user = data['statuses'][j]['user']['screen_name']

                coords = data['statuses'][j]['coordinates'].values()[1] #COORDS DATA
                lng = coords[0]
                lat = coords[1]
                
                tweet = re.sub(r'\n\n',"", tweet) #REMOVE NEWLINES
                tweet = re.sub(r'\n',"", tweet)
                
                tweet= tweet.encode('ascii', 'ignore')
                date = date.encode('ascii', 'ignore')
                user = user.encode('ascii', 'ignore')

                localfile.write(date+','+str(lat)+','+str(lng)+',@'+user+','+tweet+','+'\n');

        if results < 100:
            break

        next_id = data['statuses'][results - 1]['id']
        url = makeurl(searchTerm, next_id)

    localfile.close()
    print '\n ================================='
    print ' OUTPUT WRITE COMPLETE'


else:

    # NON-GEO OUTPUT LOOP
    localfile = open((pingtime + 'fetch.csv'),'w')
    print '\n ---------------------------------'
    for i in range(loopcount):
        header, contents = client.request(url, method="GET")
        data = json.loads(contents)
        print ' * FETCH #' + str(i+1) + ' | SUCCESS!'
        results = len(data['statuses'])  
        
        for j in range(results):
            tweet= data['statuses'][j]['text']
            date = data['statuses'][j]['created_at']
            user = data['statuses'][j]['user']['screen_name']
                
            tweet = re.sub(r'\n\n',"", tweet)
            tweet = re.sub(r'\n',"", tweet)
                
            tweet= tweet.encode('ascii', 'ignore')
            date = date.encode('ascii', 'ignore')
            user = user.encode('ascii', 'ignore')

            localfile.write(date+',@'+user+','+tweet+','+'\n');

    if results < 100:
        pass

    next_id = data['statuses'][results - 1]['id']
    url = makeurl(searchTerm, next_id)

    localfile.close()
    print '\n ================================='
    print ' OUTPUT WRITE COMPLETE'
