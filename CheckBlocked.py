import simplejson as json
import requests
from config import Config

l_odns =[] 
l_add  =[]
f = file('AddBlocker.cfg')
cfg = Config(f)
# Create a list of all urls in Opendns integration
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
#create list of Addblock URLS
Url = cfg.addurl
r = requests.get(Url)
for line in r.iter_lines() :
    if (line[0:1] is '0') :
        l_add.append(line[8:])
l_add_js = frozenset(json.loads(json.dumps(l_add)))
l_odns_js = frozenset(json.loads(json.dumps(l_odns)))
dom_remove = l_odns_js - l_add_js
dom_add = l_add_js - l_odns_js
print 'domains in addlist ' ,len(l_add_js)
print 'domains being blocked ',len(l_odns_js)
print 'domains to be removed from odns ',len(dom_remove)
print 'domains to be added to odns ' , len(dom_add)
