from selenium import webdriver
from CaptchaSolver import CaptchaSolver
import sys
import time

class RedditAccountCreator:
	def __init__ (self, url, proxy="", proxy_port= -1):
		self.url = url
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
		self.driver.implicitly_wait(10)    #wait up to 10 seconds for dom objects to appear
		self.driver.get(url)

	def did_errors_occur(self):
		errors = self.driver.find_elements_by_class_name('error')
		found_err = False
		for error in errors:
			if len(error.text):
				print "error: " + error.text 
				found_err = True
		return found_err

	
	def set_field_with_id_to_value(self, field_id, value):
		field = self.driver.find_element_by_id(field_id)
		field.click()
		field.send_keys(value)

	def create_account(self, username, password, email):
		self.driver.get(self.url)
		reglink = self.driver.find_element_by_link_text('login or register')
		reglink.click()
		cap_image = self.driver.find_element_by_class_name('capimage')
		seconds = 0
		while True:
			cap_url = cap_image.get_attribute('src')
			if not 'kill.png' in cap_url:
				break
			time.sleep(1)
			seconds += 1
			if seconds > 15:
				print "Captcha Image retrieve timeout ..."
				return False
		print "captcha image url: " + cap_url 
		solver = CaptchaSolver()
		solved_captcha = solver.solve_from_url(cap_url)
		self.set_field_with_id_to_value('user_reg', username)
		self.set_field_with_id_to_value('email_reg', email)
		self.set_field_with_id_to_value('passwd_reg', password)
		self.set_field_with_id_to_value('passwd2_reg', password)
		self.set_field_with_id_to_value('captcha_', solved_captcha)
		button = self.driver.find_element_by_class_name('button')
		button.click()
		print "checking for errors:"
		time.sleep(5)
		if self.did_errors_occur():
			print "errors occured ..."
			return False
		seconds = 0
		print "waiting for success ...",
		while True:
			cookies = self.driver.get_cookies()
			for cookie in cookies:
				if cookie['name'] == u'reddit_session':
					print "ok created"
					return True
			print ".", 	
			sys.stdout.flush()
			time.sleep(1)
			seconds += 1
			if seconds >= 25:
				print "couldn't create account!"
				return False
		return False #never reached
	
	def quit_browser(self):
		self.driver.quit()

def main():
    pass

if __name__ == "__main__":
    main();
