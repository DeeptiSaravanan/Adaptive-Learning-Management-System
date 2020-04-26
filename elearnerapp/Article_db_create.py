import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import operator
import syllabus as s
stopwords=stopwords.words('english')

urls = []
urls.append("http://www.economicsdiscussion.net/marketing-management/what-is-marketing-management/31788")
urls.append("http://www.economicsdiscussion.net/human-resource-management/role-of-human-resource-management/31737")
urls.append("http://www.economicsdiscussion.net/human-resource-management/definition-of-human-resource-management/31830")
urls.append("http://www.economicsdiscussion.net/human-resource-management/recruitment-and-selection-process/31594")
urls.append("https://www.tutorialspoint.com/management_principles/index.htm")
urls.append("https://www.tutorialspoint.com/marketing_management/index.htm")
urls.append("https://www.tutorialspoint.com/human_resource_management/index.htm")
urls.append("https://www.tutorialspoint.com/recruitment_and_selection/index.htm")
urls.append("https://www.managementstudyguide.com/all-subjects.htm")

dictionary={}
for url in urls:
	req=Request(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
	html = urlopen(req).read()
	soup = BeautifulSoup(html, 'lxml')
	all_links = soup.find_all('a')

	for link in all_links:
	    if link.get("href"):

	    	if link.get("href").startswith("/"):
	    	    if url.startswith("https://www.tutorialspoint.com"):
	    	    	lk = "/".join(url.split("/")[:-2])+link.get("href")
	    	    	kw = link.get_text().strip('\n')
	    	    	dictionary[lk]=kw

	    	    elif url.startswith("http://www.economicsdiscussion.net"):
	    	    	lk = "/".join(url.split("/")[:-1])+link.get("href")
	    	    	kw = link.get_text().strip('\n')
	    	    	dictionary[lk]=kw

	    	elif link.get("href").startswith('#'):
	    	    	lk = "/".join(url.split("/")[:-1])+'/'+link.get("href")[1:]
	    	    	kw = link.get_text().strip('\n')
	    	    	dictionary[lk]=kw

	    	elif link.get("href").startswith("http"):
	    	    	kw= link.get_text().strip('\n')
	    	    	lk=link.get("href")
	    	    	dictionary[lk]=kw

	    	else:
	    	    if url.startswith("https://www.managementstudyguide.com"):
	    	    	lk = "/".join(url.split("/")[:-1])+'/'+link.get("href")
	    	    	kw = link.get_text().strip('\n')
	    	    	dictionary[lk]=kw
    	    	

	   
df=pd.DataFrame(list(dictionary.items()),columns=['Link','Description'])
df.to_csv("ArticleKB.csv",index=False)