#!/usr/bin/env python
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys

vote_url = 'http://www.reddit.com/r/programming/comments/xw4jg/some_performance_tweaks/c5q4dn4'
vote_type = 'comment'
vote_direction = 'up'

class RedditVotingSession:
	def __init__ (self, url):
		self.driver = webdriver.Firefox()
		self.driver.get(url)

	def login(self, username, password):
		""" will try to log in to reddit. if login doesn't succeed within
		10 seconds it will time out """
		print "logging in ...",
		loginForm = self.driver.find_element_by_id("login_login-main")
		inputName = self.driver.find_element_by_name("user")
		inputPass = self.driver.find_element_by_name("passwd")
		inputName.send_keys(username)
		inputPass.send_keys(password)
		loginForm.submit()
		#now wait for login
		seconds = 0
		while True:
			cookies = self.driver.get_cookies()
			for cookie in cookies:
				if cookie['name'] == u'reddit_session':
					print "ok"
					return True
			print ".",	
			sys.stdout.flush()
			time.sleep(1)
			seconds += 1
			if seconds >= 10:
				print "couldn't log in!"
				return False
		return False #never reached

	def logout(self):
		print "logging out ...",
		logoutForm = self.driver.find_element_by_class_name("logout")
		logoutForm.submit()
		seconds = 0
		while True:
			print ".",
			sys.stdout.flush()
			stop = True
			cookies = self.driver.get_cookies()
			for cookie in cookies:
				if cookie['name'] == u'reddit_session':
					stop = False	
			if stop:
				break
			time.sleep(1)
			seconds += 1
			if seconds > 10:
				print "couldn't log out!"
				return False
		print "ok"
		return True
					

	def is_upvoted(self, arrow_element):
		""" checks if the backgreound sprite is the orange upvoted button
		i hope this works with custome reddit themes ... """
		bpos = arrow_element.value_of_css_property('background-position')
		if bpos == u'-96px -612px':
			return True
		return False

	def upvote_submission(self, url):
		""" upvotes a submission """
		print "upvoting submission: " + url
		self.driver.get(url)
		up_arrow = self.driver.find_elements_by_class_name("arrow")[0]
		if self.is_upvoted(up_arrow):
			print "Already upvoted!"
			return False
		up_arrow.click()
		time.sleep(1)
		return True
	
	def upvote_comment(self, url):
		""" upvotes a comment. url must be the 'permalink' comment url """
		print "upvoting comment: " + url
		self.driver.get(url)
		up_arrow = self.driver.find_elements_by_class_name("arrow")[2] #first 2 arrows are for the submission
		if self.is_upvoted(up_arrow):
			print "Already upvoted!"
			return False
		up_arrow.click()
		time.sleep(1)
		return True

	def is_downvoted(self, arrow_element):
		""" checks wether a given down arrow is 'clicked' """
		bpos = arrow_element.value_of_css_property('background-position')
		if bpos == u'-64px -612px':
			return True
		return False

	def downvote_submission(self, url):
		""" downvotes a given submission """
		print "downvoting submission: " + url
		self.driver.get(url)
		down_arrow = self.driver.find_elements_by_class_name("arrow")[1]
		if self.is_downvoted(down_arrow):
			print "Already downvoted!"
			return False
		down_arrow.click()
		time.sleep(1)
		return True

	def downvote_comment(self, url):
		""" seel upvote comment """
		print "downvoting comment: " + url
		self.driver.get(url)
		down_arrow = self.driver.find_elements_by_class_name("arrow")[3]
		if self.is_downvoted(down_arrow):
			print "Already downvoted!"
			return False
		down_arrow.click()
		time.sleep(1)
		return True
	
	def quit_browser(self):
		self.driver.quit()

def main():
	credentials = open(".credentials", "r").readlines()
	accounts = []
	for line in credentials:
		creds_arry = line.strip().split()
		if len(creds_arry) < 2:
			continue
		username = creds_arry[0]
		password = creds_arry[1]
		accounts.append({'username' : username, 'password' : password})
	
	rs = RedditVotingSession("http://www.reddit.com")
	for account in accounts:
		success = rs.login(account['username'], account['password'])
		if not success: 
			print "login failed for user: " + account['username']
			continue
		time.sleep(1)	
		if vote_type == 'submission':
			if vote_direction == 'up':
				success = rs.upvote_submission(vote_url)
			if vote_direction == 'down':
				success = rs.downvote_submission(vote_url)
		if vote_type == 'comment':
			if vote_direction == 'up':
				success == rs.upvote_comment(vote_url)
			if vote_direction == 'down':
				success == rs.downvote_comment(vote_url)
		if success:
			print "vote succeeded for user " + account['username']
		else:
			print "vote failed for user " + account['username']
		rs.logout()

if __name__ == "__main__":
	main()
