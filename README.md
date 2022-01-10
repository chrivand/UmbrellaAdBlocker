# AdBlocker on Umbrella

This is an Ad Blocker built on Cisco Umbrella. Please be aware that this script is a proof of concept to show how the Umbrella Enforcement API works. We do not intend to create a production version API integration or Ad Blocker. 

## Getting Started with the Installation

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Please follow the below steps. There is an extensive lab guide written for DevNet learning labs. Please send a message for more information, or check out the [Cisco DevNet](https://developer.cisco.com) website.

### Umbrella Dashboard:
1. Policies
2. Policy Components
3. Integrations 
4. " + " 
5. " < insert name > "
6. Create 
7. Click on integration 
8. Enable 
9. Copy paste key (behind “https://s-platform.api.opendns.com/1.0/events?customerKey=“) 
10. Hit save
11. Policies
12. Create new policy
13. Click next
14. Click drop down menu for security settings
15. Add new setting
16. Give name and click create
17. Check boxes Malware, Newly Seen Domains, Command and Control,  Phishing, Potentially Harmful + the new integration AdBlocker
18. Click next
19. Set content filtering to custom and click next
20. Click next for apply destination list
21. Edit the block page so that you know when the AdBlocker policy has been enforced.

### Github:
1. Open a terminal window and run the following commands:
```
    $  mkdir AdBlocker
    $  cd AdBlocker
    $  git clone https://github.com/briansak/UmbrellaAdBlocker.git
```

### Terminal

Some libraries are needed to be installed, in order for the code to work. Please use the below method to do so on your terminal:

```
1. If necessary, change directory to folder “AdBlocker” (cd <path to folder>)
2. Execute python file (python Adblocker.py)
3. If necessary install necessary libraries:
	$ sudo pip install --upgrade pip
	$ sudo pip install simplejson
	$ sudo pip install requests
	$ sudo pip install pyaml
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
* Brian Sak

## License

This project is licensed - see the [LICENSE](LICENSE) file for details



