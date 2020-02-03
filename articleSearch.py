import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from checkUpdate import getHash
urls = []
urls.append("https://www.investopedia.com")
urls.append("https://www.tutorialspoint.com")
urls.append("https://www.managementstudyguide.com")

links=[]
keywords=[]
for url in urls:
	print(url)
	html = urlopen(url)
	soup = BeautifulSoup(html, 'lxml')
	all_links = soup.find_all('a')

	for link in all_links:
	    links.append(link.get("href"))
	    temp=link.get_text()
	    temp=temp.strip("\n")
	    keywords.append(temp)
	

dictionary = dict(zip(links,keywords))
df=pd.DataFrame(list(dictionary.items()),columns=['Link','Description'])
df.to_csv("KB.csv",index=False)

def Asearch(keyword):
