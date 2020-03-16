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
stopwords=stopwords.words('english')

# urls = []
# urls.append("http://www.economicsdiscussion.net/marketing-management/what-is-marketing-management/31788")
# urls.append("http://www.economicsdiscussion.net/human-resource-management/role-of-human-resource-management/31737")
# urls.append("http://www.economicsdiscussion.net/human-resource-management/definition-of-human-resource-management/31830")
# urls.append("http://www.economicsdiscussion.net/human-resource-management/recruitment-and-selection-process/31594")
# urls.append("https://www.tutorialspoint.com/management_principles/index.htm")
# urls.append("https://www.tutorialspoint.com/marketing_management/index.htm")
# urls.append("https://www.tutorialspoint.com/human_resource_management/index.htm")
# urls.append("https://www.tutorialspoint.com/recruitment_and_selection/index.htm")
# urls.append("https://www.managementstudyguide.com/all-subjects.htm")

# links=[]
# keywords=[]
# for url in urls:
# 	print(url)
# 	req=Request(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
# 	html = urlopen(req).read()
# 	soup = BeautifulSoup(html, 'lxml')
# 	all_links = soup.find_all('a')

# 	for link in all_links:
# 	    if link.get("href"):
# 	    	if link.get("href").startswith("/"):
# 	    	    if url.startswith("https://www.tutorialspoint.com"):
# 	    	    	# print("/".join(url.split("/")[:-2])+link.get("href"))
# 	    	    	lk = "/".join(url.split("/")[:-2])+link.get("href")
# 	    	    	links.append(lk)
# 	    	    elif url.startswith("http://www.economicsdiscussion.net"):
# 	    	    	# print("/".join(url.split("/")[:-2])+link.get("href"))
# 	    	    	lk = "/".join(url.split("/")[:-1])+link.get("href")
# 	    	    	links.append(lk)
# 	    	    elif url.startswith("https://www.managementstudyguide.com"):
# 	    	    	# print("/".join(url.split("/")[:-2])+link.get("href"))
# 	    	    	lk = "/".join(url.split("/")[:-1])+link.get("href")
# 	    	    	links.append(lk)

# 	    	else:
# 	    	    links.append(link.get("href"))
# 	    	temp=link.get_text()
# 	    	temp=temp.strip("\n")
# 	    	keywords.append(temp)
	   
	    
	

# dictionary = dict(zip(links,keywords))
# df=pd.DataFrame(list(dictionary.items()),columns=['Link','Description'])
# df.to_csv("KB.csv",index=False)
df=pd.read_csv('KB.csv')
keywords=df['Description'].astype(str).values.tolist()
links=df['Link'].astype(str).values.tolist()

def clean_string(text):
	text=''.join([word for word in text if word not in string.punctuation])
	text=text.lower()
	text=' '.join([word for word in text.split() if word not in stopwords and len(word)>2 and word!='nan'])
	return text

def Asearch(text):
	cleaned = list(map(clean_string,keywords))
	tfidf_vect = TfidfVectorizer()
	vect_model = tfidf_vect.fit_transform(cleaned)

	search_string=clean_string(text)
	search_tfidf=tfidf_vect.transform([search_string])

	csim_arr=cosine_similarity(vect_model, search_tfidf)
	csim=csim_arr.tolist()
	sim_dic = dict(zip(links,csim))
	sim_dic_key= dict(zip(keywords,csim))
	sorted_sim_dic = sorted(sim_dic.items(), key=operator.itemgetter(1),reverse=True)
	sorted_sim_dic_key = sorted(sim_dic_key.items(), key=operator.itemgetter(1),reverse=True)

	result=[]
	final_links=[]
	titles=[]
	count=1
	for item in sorted_sim_dic:
		if count>5:
			break
		result.append(item)
		count=count+1

	for row in result:
		final_links.append(row[0])

	count1=1
	for item,value in sorted_sim_dic_key:
		if count1>5:
			break
		# print(item)
		titles.append(item)
		count1=count1+1
	# print(final_links)
	# print(titles)
	return dict(zip(final_links,titles))


# Asearch("planning")