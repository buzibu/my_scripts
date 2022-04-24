from selenium import webdriver
import pickle

driver = webdriver.Firefox()
driver.get('http://facebook.com')

foo = input()

pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))