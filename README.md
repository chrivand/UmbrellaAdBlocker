# Ad Blocker on Umbrella

This is a Ad Blocker built on Cisco Umbrella.

## Getting Started with the Installation

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Please follow the below steps.

### Umbrella Dashboard:
1. Settings 
3. Integrations 
5. + 
6. <insert name> 
8. create 
9. click on integration 
10. enable 
11. copy paste key (behind “https://s-platform.api.opendns.com/1.0/events?customerKey=“) 
12. hit save
13. Policies
14. Create new policy
15. Click next
16. Click drop down menu for security settings
17. Add new setting
18. Give name and click create
19. Check boxes Malware, Newly Seen Domains, Command and Control,  Phishing, Potentially Harmful + the new integration AddBlocker
20. Click next
21. Set content filtering to custom and click next
22. Click next for apply destination list
23. Edit the block page so that you know when the AddBlocker policy has been enforced.

### Github:
1. Download zip file from Github
2. Add key to AddBlocker.cfg

### Terminal

Some libraries are needed to be installed, in order for the code to work. Please use the below method to do so on your terminal:

```
1. Change directory to folder “addblocker-master” (cd <path to folder>)
2. Execute python file (python Addblocker.py)
3. If necessary install necessary libraries:
* sudo pip install --upgrade pip
* sudo pip install simplejson
* sudo pip install config
* sudo pip install <other libraries>
```

## Built With

* [Source Progress bar](https://gist.github.com/kennethreitz/450592)
* [Source Ad URL’s](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts)
* [Original Source AddBlocker](https://github.com/bartjanm/addblocker)
* [Umbrella Dashboard](https://dashboard.umbrella.com)
* [Frozen set](https://www.python-course.eu/sets_frozensets.php)

## Authors

* Bart Jan Menkveld 
* Christopher van der Made

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



