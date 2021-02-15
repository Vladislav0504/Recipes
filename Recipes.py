from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import json
import re

#Считывание html
URL = input() 
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
  if td.text != 'low in' and td.text != 'high in' and td.text != '':
  	nutrition[i] = td.text
  	i += 1

#Ингредиенты и инструкция
recipe_finding = soup.find('div', class_="row recipe__instructions")
ingredients = []
steps = {}
ind = 1
for li in recipe_finding.find_all('li'):
  if re.match(r'STEP ' + str(ind), li.text) == None and ind == 1:
  	ingredients.append(li.text)
  else:
  	ind += 1
  	steps['STEP ' + str(ind - 1)] = [li.text.replace('STEP ' + str(ind - 1), '')]

#Дополнительно
addition_finding = soup.find('div', class_="highlight-box__content editor-content")
ind = False
addition = {}
if addition_finding != None:
  ind = True
  text = addition_finding.text.replace('\n', '').split('\r')
  for i in range(0, len(text), 2):
  	addition[text[i]] = (text[i + 1])
  addition.pop('')

#Рецепт
Recipe = {
'Name': recipe_name.text, 
'Author': person_name.text,
'Mark': mark,
'Rating': ratings.text,
'General description': [{'Preparation time': preparation_time, 'Cooking time': cooking_time}, {'Description': description}, general_information],
'Nutrition: Per serving': {nutrition[i]: nutrition[i + 1] for i in range(0, 16, 2)},
'Ingredients': ingredients,
'Method': steps}

if ind == True:
  Recipe['RECIPE TIPS'] = addition

Recipe = re.sub(r'\\u00a0', ' ', json.dumps(Recipe))
Recipe = re.sub(r'\\u00bd', '1/2', Recipe)
Recipe = re.sub(r'\\u00bc', '1/4', Recipe)
Recipe = re.sub(r'\\u2013', '-', Recipe)
print(Recipe)