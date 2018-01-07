# NOTE: this script is for testing purposes to print the domains (GET requests only)

import simplejson as json
import requests
from config import Config

# testing function
l_odns =[] 
l_ads  =[]
f = file('AdBlocker.cfg')
cfg = Config(f)
# Create a list of all urls in Umbrella integration
Url = cfg.domainurl+'?customerKey='+cfg.custkey
while True:
    r = requests.get(Url)
    JsonFile = r.json()
    JsonFile = r.json()
    for row in JsonFile["data"]:
        test = row["name"]
        l_odns.append(row["name"])
    if bool(JsonFile["meta"]["next"]) :
        Url = JsonFile["meta"]["next"]
    else:    
        break

#create list of AdBlock URLS
Url = cfg.addurl
r = requests.get(Url)
for line in r.iter_lines() :
    if (line[0:1] is '0') :
        l_ads.append(line[8:])
l_ads_js = frozenset(json.loads(json.dumps(l_ads)))
l_umbrella_js = frozenset(json.loads(json.dumps(l_odns)))
dom_remove = l_umbrella_js - l_ads_js
dom_add = l_ads_js - l_umbrella_js
print 'domains in addlist ' ,len(l_ads_js)
print 'domains being blocked ',len(l_umbrella_js)
print 'domains to be removed from umbrella ',len(dom_remove)
print 'domains to be added to umbrella ' , len(dom_add)
