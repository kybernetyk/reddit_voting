#!/usr/bin/env python
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys


class RedditSession:
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
				print ".",
				sys.stdout.flush()
				if cookie['name'] == u'reddit_session':
					print "ok"
					return True
				time.sleep(1)
				seconds += 1
				if seconds >= 10:
					print "couldn't log in!"
					return False
		return False #never reached

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
		return True
	
	def quit_browser(self):
		self.driver.quit()

def main():
	credentials = open(".credentials", "r").read()
	creds_arry = credentials.strip().split()
	username = creds_arry[0]
	password = creds_arry[1]
	
	rs = RedditSession("http://www.reddit.com")
	success = rs.login(username, password)
	if not success: 
		print "login failed!"
		return

	success = rs.downvote_submission("http://www.reddit.com/r/apple/comments/xvbb1/conan_obriens_take_on_the_samsungapple_lawsuit/")
	if not success:
		print "vote failed"
		return


if __name__ == "__main__":
	main()
