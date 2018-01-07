# NOTE: more functions can be added below that can be imported in the main python script

import time 
import sys

# function for progress bar (source in README file)
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

# NOTE: This is an EXAMPLE function that can be used to schedule the Ad Blocker to refresh at intervals.
def intervalScheduler(function, interval):
    # configure interval to refresh the AdBlocker (in seconds, 3600s = 1h, 86400s = 1d)
    setInterval = interval
    AdBlocker = function

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
            time.sleep(setInterval)
    # handle keyboard interrupt
    except (KeyboardInterrupt, SystemExit):
        sys.stdout.write("\n")
        sys.stdout.write("\n")
        sys.stdout.write("Exiting... Ad Blocker will not be automatically refreshed anymore.\n")
        sys.stdout.write("\n")
        sys.stdout.flush()
        pass
