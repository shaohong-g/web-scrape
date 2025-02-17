
import random
from fake_useragent import UserAgent
from proxy_randomizer import RegisteredProviders
from proxy_randomizer.proxy import Anonymity

class Proxies:
    def __init__(self, preload=False, from_env=False, annoymous=False):
        initial_list = []
        self.proxy_list = []
        self.useragent = None
        self.rp = None

        if from_env:
            initial_list.append(self.get_proxy_from_env())
        else:
            initial_list.extend(self.get_proxy_from_library(annoymous))
        self.proxy_list = initial_list

        if preload:
            self.preload_and_test()

    def get_proxy_ip(self):
        if len(self.proxy_list) == 0:
            raise Exception("No Proxy found!")
        return random.choice(self.proxy_list)

    def get_proxy_useragent(self):
        if self.useragent is None:
            self.useragent = UserAgent(browsers=['Chrome'])
        return self.useragent.random # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    def preload_and_test(self):
        pass    

    def get_proxy_from_env(self, env_file=".env"):
        from dotenv import dotenv_values
        config = dotenv_values(env_file)
        return config["PROXY_URL"]
    def get_proxy_from_library(self, annoymous=False):
        rp = RegisteredProviders()
        rp.parse_providers()
        self.rp = rp
        # print(f"proxy: {rp.get_random_proxy()}")
        targeted_proxies = list(filter(lambda proxy: proxy.anonymity == Anonymity.ANONYMOUS, rp.proxies)) if annoymous else rp.proxies
        return list(map(lambda x: f"http://{x.ip_address}:{x.port}", targeted_proxies))
