from selenium import webdriver
#import time

class RedditAccountCreator:
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
        self.driver.implicitly_wait(10)    #wait up to 10 seconds for dom objects to appear
        self.driver.get(url)

    def create_account(self, username, password, email):
        pass
