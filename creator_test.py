#!/usr/bin/env python
PROXY_HOST = "localhost"
PROXY_PORT = 9050

from RedditAccountCreator import RedditAccountCreator
from TorCycler import TorCycler


def main():
	#let's create a list of account names
	"""f = open("wordlist.txt", "r")
	for i in range(0,100): 
		word1 = f.readline().strip().rstrip()
		word2 = f.readline().strip().rstrip()
		word3 = f.readline().strip().rstrip()
		username = word3 + word1
		password = word2
		f.readline()
		print word1+""+word3 + " " + word2
	return"""
	credentials = open("tocreate.txt", "r").readlines()
	accounts = []
	for line in credentials:
		creds_arry = line.strip().split()
		if len(creds_arry) < 2:
			continue
		username = creds_arry[0]
		password = creds_arry[1]
		accounts.append({'username' : username, 'password' : password})
	
	print "starting account creation ..."
	results_file = open("created.txt", "a")
	tor_cycler = TorCycler()
	for account in accounts:
		tor_cycler.cycle()
		creator = RedditAccountCreator("http://www.reddit.com", PROXY_HOST, PROXY_PORT)
		username = account['username']
		password = account['password']
		email = ""
		print "creating " + username + "|" + password
		success = creator.create_account(username, password, "")
		if success:
			print "created account: " + username + "|" + password + "|" + email
			print "adding to database ..."
			results_file.write(username + " " + password + "\n")
			results_file.flush()
			creator.quit_browser()
		else:
			print "account creation failed"
	results_file.close()
if __name__ == "__main__":
    main()
