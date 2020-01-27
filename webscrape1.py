import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
url = "https://www.investopedia.com"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
type(soup)
title = soup.title
print(title)
all_links = soup.find_all('a')
links=[]
keywords=[]

for link in all_links:
    links.append(link.get("href"))
    temp=link.get_text()
    temp=temp.strip("\n")
    keywords.append(temp)

dictionary = dict(zip(links,keywords))
df=pd.DataFrame(list(dictionary.items()),columns=['Link','Description'])
df.to_csv("KB.csv",index=False)