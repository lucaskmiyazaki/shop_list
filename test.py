from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

PATH = "/home/lucas/projects/selenium/chromedriver.exe"

word = input("digite a comida:")
driver = webdriver.Chrome(PATH)
driver.get("http://google.com")

search = driver.find_element_by_xpath("//input[@type='text']")
search.send_keys(word + "\n")

links = driver.find_elements_by_tag_name('a')
urls = []

for link in links:
    url = link.get_attribute('href')
    if type(url) == str and re.match(".*tudogostoso", url):
        driver.get(url)
        break

body = driver.find_elements_by_class_name("p-ingredient")
for topic in body:
    ingredient = topic.text
    print(ingredient)
    qtd = re.search('(?P<qtd>\d*\/?\d*)', ingredient)
    ing = re.search('(?P<ing>.*)', ingredient)
    if qtd: 
        print(qtd.group('qtd'))
        temp = re.search('\d*(?P<ing>.*)', ingredient)
        if temp: ing = temp
    unit = re.search('\d*\/?\d*(?P<unit>.*?)de', ingredient)
    if unit and not ('(' in unit.group('unit') and ')' not in unit.group('unit')): 
        print(unit.group('unit'))
        temp = re.search('\d*.*?de(?P<ing>.*)', ingredient)
        if temp: ing = temp
    if ing: 
        ingredient = ing.group('ing')
        obs = re.search('\((?P<obs>.*?)\)', ingredient)
        if obs:
            print(obs.group('obs'))
            ing = re.search('(?P<ing>.*?)\(.*?\)', ingredient)
        print(ing.group('ing'))


