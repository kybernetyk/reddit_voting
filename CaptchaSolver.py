import time
import subprocess

class CaptchaSolver:
	def __init__ (self):
		pass

	def solve_from_url(self, url):
		print "CaptchaSolver solves url: " + url
		cap_res = subprocess.check_output(("./captcha_solver.sh " + url), shell=True)
		print "solved captcha: " + cap_res
		return cap_res.strip().rstrip()

	def solve_from_file(self, path):
		pass
