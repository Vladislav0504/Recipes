from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup
import json
import re

URL = 'https://www.bbcgoodfood.com/recipes/meatball-black-bean-chilli' 
resp = urlopen(URL) # скачиваем файл
html = resp.read().decode('utf8') # считываем содержимое
soup = BeautifulSoup(html, 'html.parser') # делаем суп

recipe_name = soup.find('h1', class_='header__title heading-1')
person_name = soup.find('a', rel="author")

mark_finding = soup.find_all('span', class_="sr-only")
mark = ''
for elem in mark_finding:
  if re.match(r'Rating:+', elem.text) != None:
  	mark = elem.text
  	break
ratings = soup.find('span', class_="rating__count-text body-copy-small")

Recipes = {
'Name': recipe_name.text, 
'Author': person_name.text,
'Mark': mark,
'Rating': ratings.text}
print(json.dumps(Recipes))