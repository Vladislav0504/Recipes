from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import json
import re

#Считывание html
URL = 'https://www.bbcgoodfood.com/recipes/meatball-black-bean-chilli' 
resp = urlopen(URL)
html = resp.read().decode('utf8')
soup = BeautifulSoup(html, 'html.parser')

#Название блюда и имя автора
recipe_name = soup.find('h1', class_='header__title heading-1')
person_name = soup.find('a', rel="author")

#Рейтинг
mark_finding = soup.find_all('span', class_="sr-only")
mark = ''
for elem in mark_finding:
  if re.match(r'Rating:+', elem.text) != None:
  	mark = elem.text
  	break
ratings = soup.find('span', class_="rating__count-text body-copy-small")

#Общее описание
preparation_and_cooking_time = soup.find_all('time')
preparation_time = preparation_and_cooking_time[0].text
cooking_time = preparation_and_cooking_time[1].text
description_finding = soup.find_all('div', class_="icon-with-text__children")
description = tuple(elem.text for elem in description_finding[1:])
general_information = soup.find('meta', {'name': "og:description"})['content']

#Состав
nutrition_finding = soup.find('table')
nutrition = ['' for i in range(16)]
i = 0
for td in nutrition_finding.find_all('td'):
  nutrition[i] = td.text
  i += 1

#Рецепт
Recipes = {
'Name': recipe_name.text, 
'Author': person_name.text,
'Mark': mark,
'Rating': ratings.text,
'General description': [{'Preparation time': preparation_time, 'Cooking time': cooking_time}, {'Description': description}, general_information],
'Nutrition: Per serving': [{nutrition[i]: nutrition[i + 1] for i in range(0, 16, 2)}]}
print(json.dumps(Recipes).replace("\\u00a0", ' '))