#import necessary libraries and functions
import simplejson as json
import requests
from config import Config
import time
import sys
from datetime import datetime
# additional functions can be imported from external python script (i.e. AdBlockerFunctions.py)
from AdBlockerFunctions import progressbar, intervalScheduler

# two sets to hold domains, one with domains already in Umbrella, the other with domains from Ads DB
l_umbrella =[] 
l_ads  =[]

# import file with API call URL's and customer key (file is in .gitignore)
f = file('AdBlocker.cfg')
cfg = Config(f)

# create function of entire Ad Blocker code, so that it can be called iteratively (e.g by the scheduler)
def AdBlocker():

    # GET REQUEST: append the set with all domains that are already present in the Umbrella integration by doing GET requests 
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

    # GET REQUEST: append the set for AdBlock domains from Ads DB by doing GET request
    Url = cfg.addurl
    r = requests.get(Url)

    # NOTE: this is the for-loop needed for the full production version (comment lines for DevNet session)
    for line in r.iter_lines():
        # lines in Ads DB with domains, start with 0.0.0.0 ...
        if (line[0:1] is '0'):
            # they 9th character is the first of the domain, e.g.: 0.0.0.0 tracking.klickthru.com
            l_ads.append(line[8:])

    ## NOTE: this is the for-loop needed for the DevNet session (comment lines for full production version)
    ## index is used to stop iteration after 250 domains
    #for index, line in enumerate(r.iter_lines()):
    #    if (index == 279):
    #        break
        ## lines in Ads DB with domains, start with 0.0.0.0 ...
    #    elif (line[0:1] is '0'):
            ## they 9th character is the first of the domain, e.g.: 0.0.0.0 tracking.klickthru.com
    #        l_ads.append(line[8:])

    # create two frozensets to hold domains: frozensets are used for performance, and since we had to make sure both are in equal form this was chosen.
    l_ads_js = frozenset(json.loads(json.dumps(l_ads)))
    l_umbrella_js = frozenset(json.loads(json.dumps(l_umbrella)))

    # compare the two frozensets and create two new lists, one for domains to be removed, and one for domains to be added to Umbrella 
    dom_remove = l_umbrella_js - l_ads_js
    dom_add = l_ads_js - l_umbrella_js

    # check if dom_remove is not empty    
    if dom_remove:
        # give feedback to user and add line break for more overview
        sys.stdout.write("\n")
        sys.stdout.write("Unnecessary domains will be removed now:\n")
        sys.stdout.write("\n")
        # DELETE REQUEST: deleting URL's that are in Umbrella, which are not in de Ads DB anymore 
        for line in progressbar(dom_remove,"removing: ", 50):
            Url = cfg.domainurl+'?customerKey='+cfg.custkey+'&where[name]='+line
            r = requests.delete(Url) 
            print(line)
        # give feedback to user
        sys.stdout.write("\n")
        sys.stdout.write("Unnecessary domains have been removed!\n")

    # create header for post request to add new Ad Domains to Umbrella
    Header = {'Content-type': 'application/json', 'Accept': 'application/json'}
    Url = cfg.eventurl+'?customerKey='+cfg.custkey

    # iterate variable used in comming for loop 
    # i = 1 # (bartjanm-patch-1: DELETE)
    # time for AlertTime and EventTime when domains are added to Umbrella
    time = datetime.now().isoformat()

    # check if dom_add is not empty    
    if dom_add:
        # give feedback to user and add line break for more overview
        sys.stdout.write("\n")
        sys.stdout.write("New domains will be added now:\n")
        sys.stdout.write("\n")
        # loop through domains that need to be added and create Event that can be sent with POST request (according to Umbrella API docummentation)
        for line in progressbar(dom_add,"Adding:   ",50):
            # NOTE: Although this information MUST be provided when using the API, not all of it is utilized in the destination lists within Umbrella
            data = {
            "alertTime": time + "Z",
            "deviceId": "ba6a59f4-e692-4724-ba36-c28132c761de",
            "deviceVersion": "13.7a",
            "dstDomain": line,
            "dstUrl": "http://" + line + "/",
            "eventTime": time + "Z",
            "protocolVersion": "1.0a",
            "providerName": "Security Platform"
            }
            
            # POST REQUEST: post request ensembly
            req = requests.post(Url, data=json.dumps(data), headers={'Content-type': 'application/json', 'Accept': 'application/json'})
            
            # error handling 
            try:
                # if true then the request was HTTP 200, so successful 
                req.status_code == requests.codes.ok
                
            # if request fails then sleep
            except: 
                for i in progressbar(range(10),"failed to add: "+line,50):
                    time.sleep(1)
            pass 
            # i+= 1 # (bartjanm-patch-1: DELETE)

    # give feedback to user and add line break for more overview
    sys.stdout.write("\n")  
    sys.stdout.write("Congratulations, the AdBlocker has been updated!\n")

# call the AdBlocker function so that it gets executed in this file, 
try:
    # comment out if using the intervalScheduler for automatic refreshing
    AdBlocker()
    
    # uncomment when using the intervalScheduler for automatic refreshing
    #intervalScheduler(AdBlocker, 86400)
except (KeyboardInterrupt, SystemExit):
    sys.stdout.write("\n")
    sys.stdout.write("\n")
    sys.stdout.write("Exiting...\n")
    sys.stdout.write("\n")
    sys.stdout.flush()
    pass

# end of script