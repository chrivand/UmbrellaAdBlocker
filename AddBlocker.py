import simplejson as json
import requests
from config import Config
import time
import sys
import urllib2

def progressbar(it, prefix = "", size = 60):
    count = len(it)
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i, count))
        sys.stdout.flush()
    
    _show(0)
    for i, item in enumerate(it):
        yield item
        _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()

l_odns =[] 
l_add  =[]
f = file('AddBlocker.cfg')
cfg = Config(f)
# Create a list of all urls in Opendns integration
Url = cfg.domainurl+'?customerKey='+cfg.custkey
while True:
    r = requests.get(Url)
##    JsonFile = r.json()
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


for line in progressbar(dom_remove,"removing: ", 50):
    Url = cfg.domainurl+'?customerKey='+cfg.custkey+'&where[name]='+line
    r = requests.delete(Url) 
    print(line)

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
