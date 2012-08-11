#!/usr/bin/env python
from RedditAccountCreator import RedditAccountCreator

username = "amigahenry"
password = "warbird"
email = "leon@fluxforge.com"

def main():
	print "starting creation ..."
	creator = RedditAccountCreator("http://www.reddit.com")
	success = creator.create_account(username, password, email)
	if success:
		print "created: " + username + "|" + password + "|" + email
	else:
		print "creation failed"

if __name__ == "__main__":
    main()
