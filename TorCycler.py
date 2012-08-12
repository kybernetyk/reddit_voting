import sys
import os
import time
import subprocess

class TorCycler:
	def __init__ (self):
		self.used_ips = {}

	def cycle(self):
		sleeptime = 5
		conscutive_fails = 0
		while True:
			sys.stderr.write("*** cycling tor exit node ***\n")
			os.system("killall -HUP tor")
			sys.stderr.write("*** sleeping %i sec ***\n" % (sleeptime))
			time.sleep(sleeptime)
			my_ip = self.dump_current_ip()
			if my_ip not in self.used_ips:
				self.used_ips[my_ip] = time.time()
				return
			tme = self.used_ips[my_ip]
			if time.time() - tme > 600:
				self.used_ips[my_ip] = time.time()
				return
			conscutive_fails += 1
			if conscutive_fails > 3:
				sys.stderr.write("*** ips are repeating. sleeping for 20 minutes ... ***")
				time.sleep(1200)
		return

	def dump_current_ip(self):
		sys.stderr.write("*** retrieving current IP ***\n")
		my_ip = subprocess.check_output("torify curl http://icanhazip.com", shell=True)
		sys.stderr.write("*** current IP: %s ***\n" % (my_ip.strip()))
		return my_ip
