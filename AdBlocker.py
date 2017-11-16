#import necessary libraries and functions
import simplejson as json
import requests
from config import Config
import time
import sys
from AdBlockerFunctions import progressbar 
#OLD import urllib2

#create global variables 
# two sets to hold domains, one with domains already in Umbrella, the other with domains from Ads DB
l_umbrella =[] 
l_ads  =[]

# import file with API call URL's and customer key (file is in .gitignore)
f = file('AdBlocker.cfg')
cfg = Config(f)

# Create a set of all domains in Umbrella integration
Url = cfg.domainurl+'?customerKey='+cfg.custkey
while True:
    r = requests.get(Url)
    JsonFile = r.json()
    for row in JsonFile["data"]:
        l_umbrella.append(row["name"])
    if bool(JsonFile["meta"]["next"]):
        Url = JsonFile["meta"]["next"]
    else:    
        break

#create list of AdBlock domains from Ads DB
Url = cfg.addurl
r = requests.get(Url)
for line in r.iter_lines():
    # lines in Ads DB with domains, start with 0.0.0.0 ...
    if (line[0:1] is '0'):
        # they 9th character is the first of the domain, e.g.: 0.0.0.0 tracking.klickthru.com
        l_ads.append(line[8:])

# creat two frozensets to hold domains 
l_ads_js = frozenset(json.loads(json.dumps(l_ads)))
l_umbrella_js = frozenset(json.loads(json.dumps(l_umbrella)))

# compare the two lists and create two new lists, one for domains to be removed, and one for domains to be added to Umbrella 
dom_remove = l_umbrella_js - l_ads_js
dom_add = l_ads_js - l_umbrella_js

# check if dom_remove is not empty    
if dom_remove:
    # deleting URL's that are in Umbrella, which are not in de Ads DB anymore 
    for line in progressbar(dom_remove,"removing: ", 50):
        Url = cfg.domainurl+'?customerKey='+cfg.custkey+'&where[name]='+line
        r = requests.delete(Url) 
        print(line)

# create header for post request to add new Ad Domains to Umbrella
Header = {'Content-type': 'application/json', 'Accept': 'application/json'}
Url = cfg.eventurl+'?customerKey='+cfg.custkey

# create post request data according to Umbrella API docummentation
i = 1
for line in progressbar(dom_add,"Adding:   ",50):
    # Although this information MUST be provided when using the API, not all of it is utilized in the destination lists within Umbrella
    data = {
    "alertTime": "2013-02-08T11:14:26.0Z",
    "deviceId": "ba6a59f4-e692-4724-ba36-c28132c761de",
    "deviceVersion": "13.7a",
    "dstDomain": line,
    "dstUrl": "http://" + line + "/",
    "eventTime": "2013-02-08T09:30:26.0Z",
    "protocolVersion": "1.0a",
    "providerName": "Security Platform"
    }
    
    # post request ensembly
    req = requests.post(Url, data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'application/json'})


    #OLD req = urllib2.Request(Url, json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
    #OLD print i," uit ",len(dom_add), line,"\r"
    
    # error handling 
    try:
        # if true then the request was HTTP 200, so successful 
        req.status_code == requests.codes.ok
        
        #OLD response = urllib2.urlopen(req)
    #OLD except (RuntimeError, TypeError, NameError):
    
    # if request fails then sleep
    except: 
        for i in progressbar(range(10),"failed to add: "+line,50):
            time.sleep(1)
    pass 
    i+= 1 
