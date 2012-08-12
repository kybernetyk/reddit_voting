= Reddit Voting Suite =
Let's have fun with reddit :3


Dependencies: python 2.7, selenium webdriver, firefox, running tor @ localhost:9050

    pip install selenium

= How To Run =

== Setup Tor ==
The scripts await tor running with the tor socks proxy listening on localhost:9050. You can change these settings inside the *_test.py scripts.

== Setup Captcha Cracking ==
Get a de-captcher.com account and put your login credentials into a file called .decaptcher
See more inside captcha_solver.sh

== Account Creator Script ==
run ./creator_test.py to create some accounts. this script needs a list of <username> <password>\n accounts to create in a file called tocreate.txt

== Voting Script ==
edit vote_test.py to set the voting parameters.
This script awaits a file ".credentials" in its working directory. This file has to contain your reddit username and password:

    username password

= Limitations =
Reddit has some pretty interesting spam/bot detection. If you'd want to run this in 'production' you should probably fake user agents, make fake comments with the created accounts, get a huge list of proxies (tor won't be enough for more than a dozen accounts!) and reverse their fake vote detection (as bloom filter are the new hipster-shit and reddit is run by hippster douches I'd look into this). 

I have no intention to continue work on this as I just wanted to fuck up a guy ... and I was successful. So my work is done here.

License GPL3
(c) Leon Szpilewski
leon.szpilewski@gmail.com
http://jsz.github.com
