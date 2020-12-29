from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import csv
import re

PATH = "/home/lucas/projects/selenium/chromedriver.exe"

class Food:
  def __init__(self, dish_name):
    keywords = dish_name.split()
    search_name = ''
    for word in keywords: 
      if search_name == '': 
        search_name += word
        main_word = word
      else: search_name += '+' + word

    search_page = requests.get("https://www.tudogostoso.com.br/busca?q=%s"%search_name)
    search_soup = BeautifulSoup(search_page.text, 'html.parser')
    search_text = str(search_soup)
    reg_ex = re.search('<a\sclass=.*href="(?P<endpoint>.*%s.*html)"'%main_word, search_text)
    if not reg_ex:
      self.raw_lines = [] 
      return 
    endpoint = reg_ex.group("endpoint")
    url = "https://www.tudogostoso.com.br" + endpoint
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    soup_lines = soup.find_all('span', attrs={'class':'p-ingredient'})
    lines = []
    for line in soup_lines: lines.append(line.text)
    self.raw_lines = lines

  def auto_sep(self, i):
    ingredient = self.raw_lines[i]
    print('\n' + ingredient)
    qtd = re.search('(?P<qtd>(\d.{0,7})?\d)', ingredient)
    ing = re.search('(?P<ing>.*)', ingredient)
    obs = None
    if qtd:
        #print(qtd.group('qtd'))
        qtd = qtd.group('qtd').strip()
        temp = re.search('(\d.{0,7})?\d(?P<ing>.*)', ingredient)
        if temp: ing = temp
    else:
      temp = re.search('(?P<ing>.*)\s(?P<qtd>.\sgosto)', ingredient)
      if temp:
        qtd = temp.group('qtd').strip()
        ing = temp.group('ing').strip()
        return qtd, None, ing, obs
      else: return None, None, None, None
    unit = re.search('(\d.{0,7})?\d(?P<unit>.*?)\sde\s', ingredient)
    if unit and not ('(' in unit.group('unit') and ')' not in unit.group('unit')):
        #print(unit.group('unit'))
        unit = unit.group('unit').strip()
        temp = re.search('\d*.*?\sde\s(?P<ing>.*)', ingredient)
        if temp: ing = temp
    if ing:
        ingredient = ing.group('ing')
        obs = re.search('\((?P<obs>.*?)\)', ingredient)
        if obs:
            #print(obs.group('obs'))
            obs = obs.group('obs').strip()
            ing = re.search('(?P<ing>.*?)\(.*?\)', ingredient)
        #print(ing.group('ing'))
        ing = ing.group('ing').strip()
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

  def separator(self, csvfile):
    for i in range(len(self.raw_lines)):
      sep = self.auto_sep(i)
      resp = input("qtd: %s\nunit: %s\ning: %s\nobs: %s"%sep)
      if resp == '0':
        sep = self.manual_sep(i)
      print("qtd: %s\nunit: %s\ning: %s\nobs: %s"%sep)
      qtd, unit, ing, obs = sep
      spamwriter = csv.writer(csvfile, delimiter=';')
      spamwriter.writerow([qtd, unit, ing, obs])

f = open("training.txt", 'r')
with open('menu.csv', 'w+') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=';')
  spamwriter.writerow(['qtd', 'unit', 'ing', 'obs'])
  for line in f:
    dish = Food(line)
    dish.separator(csvfile)

