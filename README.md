# AdBlocker on Umbrella

This is an Ad Blocker built on Cisco Umbrella. Please be aware that this script is a proof of concept to show how the Umbrella Enforcement API works. We do not intend to create a production version API integration or Ad Blocker. 

## Getting Started with the Installation

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Please follow the below steps. There is an extensive lab guide written for DevNet learling labs. Please send a message for more information, or check out the [Cisco DevNet](https://developer.cisco.com) website.

### Umbrella Dashboard:
1. Settings 
2. Integrations 
3. " + " 
4. " < insert name > "
5. Create 
6. Click on integration 
7. Enable 
8. Copy paste key (behind “https://s-platform.api.opendns.com/1.0/events?customerKey=“) 
9. Hit save
10. Policies
11. Create new policy
12. Click next
13. Click drop down menu for security settings
14. Add new setting
15. Give name and click create
16. Check boxes Malware, Newly Seen Domains, Command and Control,  Phishing, Potentially Harmful + the new integration AdBlocker
17. Click next
18. Set content filtering to custom and click next
19. Click next for apply destination list
20. Edit the block page so that you know when the AdBlocker policy has been enforced.

### Github:
1. Open a terminal window and run the following commands:
```
    $  mkdir AdBlocker
    $  cd AdBlocker
    $  git clone https://github.com/chrivand/UmbrellaAdBlocker.git
```

### Terminal

Some libraries are needed to be installed, in order for the code to work. Please use the below method to do so on your terminal:

```
1. If necessary, hange directory to folder “AdBlocker” (cd <path to folder>)
2. Execute python file (python Adblocker.py)
3. If necessary install necessary libraries:
	$ sudo pip install --upgrade pip
	$ sudo pip install simplejson
	$ sudo pip install config
	$ sudo pip install <other libraries>
```

## Built With

* [Source Progress bar](https://gist.github.com/kennethreitz/450592)
* [Source Ad URL’s](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts)
* [Original Source AdBlocker](https://github.com/bartjanm/addblocker)
* [Umbrella Dashboard](https://dashboard.umbrella.com)
* [Frozen Set](https://www.python-course.eu/sets_frozensets.php)
* [Umrella API Documentation](https://docs.umbrella.com/developer/enforcement-api/)

## Authors

* Bart Jan Menkveld 
* Christopher van der Made

## License

This project is licensed - see the [LICENSE](LICENSE) file for details



