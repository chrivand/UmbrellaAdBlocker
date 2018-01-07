# NOTE: This is an EXAMPLE function that can be used to schedule the Ad Blocker to refresh at intervals. 
import time 
import sys
# import AdBlocker function from main AdBlocker script
from AdBlocker import AdBlocker


# configure interval to refresh the AdBlocker (in seconds, 3600s = 1h, 86400s = 1d)
interval = 86400

# user feedback
sys.stdout.write("\n")
sys.stdout.write("Ad Blocker will be refreshed every %d seconds. Please use ctrl-C to exit.\n" %interval)
sys.stdout.write("\n")

# interval loop, unless keyboard interrupt
try:
    while True:
    	AdBlocker()
    	sys.stdout.write("\n")
    	sys.stdout.write("Ad Blocker updated!\n")
    	sys.stdout.write("\n")
    	time.sleep(interval)
# handle keyboard interrupt
except (KeyboardInterrupt, SystemExit):
    sys.stdout.write("\n")
    sys.stdout.write("\n")
    sys.stdout.write("Exiting... Ad Blocker will not be automatically refreshed anymore.\n")
    sys.stdout.write("\n")
    sys.stdout.flush()
    pass

