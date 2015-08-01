from selenium import webdriver


browser = webdriver.Firefox()
browser.get('http://piratelocal.com')
assert 'Django' in browser.title