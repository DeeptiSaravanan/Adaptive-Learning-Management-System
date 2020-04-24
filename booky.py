import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from urllib.request import urlopen
from bs4 import BeautifulSoup


dff = pd.DataFrame()

def bsearch(i):
	search = []

	if (i.find("Basics") != -1):
		url = "https://openlibrary.org/search?q=fundamentals+of+management&mode=everything&page=3"
		df = material(url)
		#print(df.head())
		df = dff.append(df)
	elif (i.find("Human") != -1):
		url = "https://openlibrary.org/search?q=fundamentals+of+human+resource+management&mode=everything"
		df = material(url)
		df = dff.append(df)
	elif (i.find("Marketing") != -1):
		url = "https://openlibrary.org/search?q=marketing+management&mode=everything&page=5"
		df = material(url)
		df = dff.append(df)
	else:
		print("Error")
		
	return df


def material(url):

	Link = []
	Description = []
	Author = []
	
	url = url	
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
	c3 = []

	all_links = soup.find_all('a', class_="results", itemprop="name")
	for link in all_links:
    		c1.append(link.get_text())
    		c2.append(link.get("href"))
	
	authorlink = soup.find_all('a', class_="results", itemprop="author")
	for link in authorlink:
		c3.append(link.get_text())

	#for div in soup.findAll('div', {'class': 'title'}):
	#    a = div.find('a')
	#    c1.append(a.attrs['href'])
	#    c2.append(a.get_text())

	Link.append(c1)
	Description.append(c2)
	Author.append(c3)
	dict = {'Link' : Link, 'Description' : Description, 'Author' : Author}
	df = pd.DataFrame(dict)
	print(df)
	return df
	
bsearch("Human")




