import os 
from selenium import webdriver

options = webdriver.FirefoxOptions()
options.add_argument("-profile")
options.add_argument("/home/sicheng1806/script/python/ttdweb/firefox_config")
brower = webdriver.Firefox(options=options)

brower.get('http://localhost:8000')

assert 'Django' in brower.title