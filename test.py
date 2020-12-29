from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

PATH = "/home/lucas/projects/selenium/chromedriver.exe"

class Menu:
    def __init__(self, word):
        #word = input("digite a comida:")
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
        self.raw_lines = []
        for topic in body:
            line = topic.text
            self.raw_lines.append(line)

    def auto_sep(self, i):
        ingredient = self.raw_lines[i]
        #print(ingredient)
        qtd = re.search('(?P<qtd>\d*\/?\d*)', ingredient)
        ing = re.search('(?P<ing>.*)', ingredient)
        obs = None
        if qtd: 
            #print(qtd.group('qtd'))
            temp = re.search('\d*(?P<ing>.*)', ingredient)
            if temp: ing = temp
        unit = re.search('\d*\/?\d*(?P<unit>.*?)de', ingredient)
        if unit and not ('(' in unit.group('unit') and ')' not in unit.group('unit')): 
            #print(unit.group('unit'))
            temp = re.search('\d*.*?de(?P<ing>.*)', ingredient)
            if temp: ing = temp
        if ing: 
            ingredient = ing.group('ing')
            obs = re.search('\((?P<obs>.*?)\)', ingredient)
            if obs:
                #print(obs.group('obs'))
                ing = re.search('(?P<ing>.*?)\(.*?\)', ingredient)
            #print(ing.group('ing'))
        return qtd, unit, ing, obs

    def manual_sep(self, i):
        line = self.raw_lines[i]
        qtd = ''
        unit = ''
        ing = ''
        obs = ''
        for word in line.split():
            cat = input(word)
            if cat == '1':
                if qtd == '': qtd += word
                else: qtd += ' ' + word
            elif cat == '2':
                if unit == '': unit += word
                else: unit += ' ' + word
            elif cat == '3':
                if ing == '': ing += word
                else: ing += ' ' + word
            elif cat == '4':
                if obs == '': obs += word
                else: obs += ' ' + word
        return qtd, unit, ing, obs

    def separator(self):
        for i in range(len(self.raw_lines)):
            sep = self.auto_sep(i)
            resp = input("qtd: %s\nunit: %s\ning: %s\nobs: %s"%sep)
            if resp == '0':
                sep = self.manual_sep(i)
            print(sep)
            qtd, unit, ing, obs = sep

f = open("training.txt", 'r')
for line in f:
    menu = Menu(line)
    menu.separator()
