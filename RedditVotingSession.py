#!/usr/bin/env python
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys

class RedditVotingSession:
	def __init__ (self, url, proxy="", proxy_port= -1):
		fp = webdriver.FirefoxProfile()
		use_proxy = (len(proxy) > 0 and proxy_port != -1)
		if use_proxy:	
			# Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
			fp.set_preference("network.proxy.type", 1)
			#socks (tor) proxy:
			fp.set_preference("network.proxy.socks", proxy)
			fp.set_preference("network.proxy.socks_port", proxy_port)
			""" use this for http proxy:
			fp.set_preference("network.proxy.http", PROXY_HOST)
			fp.set_preference("network.proxy.http_port", PROXY_PORT)
			fp.set_preference("network.proxy.ftp", PROXY_HOST)
			fp.set_preference("network.proxy.ftp_port", PROXY_PORT)
			fp.set_preference("network.proxy.ssl", PROXY_HOST)
			fp.set_preference("network.proxy.ssl_port", PROXY_PORT)
			"""
			fp.set_preference("network.proxy.no_proxies_on", "") 			
		self.driver = webdriver.Firefox(fp)
		self.driver.implicitly_wait(10)	#wait up to 10 seconds for dom objects to appear
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

	def downvote_comment(self, url):
		""" seel upvote comment """
		print "downvoting comment: " + url
		self.driver.get(url)
		down_arrow = self.driver.find_elements_by_class_name("arrow")[3]
		if self.is_downvoted(down_arrow):
			print "Already downvoted!"
			return False
		down_arrow.click()
		return True
	
	def quit_browser(self):
		self.driver.quit()
