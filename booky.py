import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://openlibrary.org/search?q=human+resource&mode=ebooks&m=edit&has_fulltext=true"
html = urlopen(url)

#soup = BeautifulSoup(html, 'lxml')
soup = BeautifulSoup(html)
type(soup)

# Get the title
title = soup.title
print(title)

text = soup.get_text()

c1 = []
c2 = []

all_links = soup.find_all('a', class_="results", itemprop="name")
for link in all_links:
    c1.append(link.get_text())
    c2.append(link.get("href"))

Link = c1
Description = c2
dict = {'Link' : Link, 'Description' : Description}    
df = pd.DataFrame(dict)
df.to_csv('book.csv')






