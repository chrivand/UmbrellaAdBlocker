#import necessary libraries and functions
import simplejson as json
import requests
from config import Config
import time
import sys
import urllib2
from AddBlockerFunctions import progressbar 

#create global variables 
# two sets to hold domains, one with domains already in Umbrella, the other with domains from Ads DB
l_umbrella =[] 
l_ads  =[]

# import file with API call URL's and customer key
f = file('AddBlocker.cfg')
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

#create list of Addblock domains from Ads DB
Url = cfg.addurl
r = requests.get(Url)
for line in r.iter_lines():
    if (line[0:1] is '0'):
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

# COMMENT
Header = {'Content-type': 'application/json', 'Accept': 'application/json'}
Url = cfg.eventurl+'?customerKey='+cfg.custkey

i = 1
for line in progressbar(dom_add,"Adding:   ",50):
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
    # Ruzie  met requests voor de post.. Even oldscool
    
    #req = requests.post(Url, data = json.dumps(data), {'Content-type': 'application/json', 'Accept': 'application/json'})


    req = urllib2.Request(Url, json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
   ## print i," uit ",len(dom_add), line,"\r"
    try:
        response = urllib2.urlopen(req)
##  `  except (RuntimeError, TypeError, NameError):
    except: 
        for i in progressbar(range(10),"failing    "+line,50):
       time.sleep(1)
    pass 
    i+= 1 