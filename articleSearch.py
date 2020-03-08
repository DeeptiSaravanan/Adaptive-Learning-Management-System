import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import operator
stopwords=stopwords.words('english')

urls = []
urls.append("https://www.investopedia.com")
urls.append("https://www.tutorialspoint.com/management_principles/index.htm")
urls.append("https://www.tutorialspoint.com/marketing_management/index.htm")
urls.append("https://www.tutorialspoint.com/human_resource_management/index.htm")
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
	# print(tfidf_vect.get_feature_names())
	# print(vect_model)

	search_string=clean_string(text)
	search_tfidf=tfidf_vect.transform([search_string])

	# print(search_tfidf)

	csim_arr=cosine_similarity(vect_model, search_tfidf)
	csim=csim_arr.tolist()
	sim_dic = dict(zip(links,csim))
	sim_dic_key= dict(zip(keywords,csim))
	# print(sim_dic)
	sorted_sim_dic = sorted(sim_dic.items(), key=operator.itemgetter(1),reverse=True)
	sorted_sim_dic_key = sorted(sim_dic_key.items(), key=operator.itemgetter(1),reverse=True)
	# print(sorted_sim_dic)

	result=[]
	count=1
	for item in sorted_sim_dic:
		if count>5:
			break
		result.append(item)
		count=count+1

	print([row[0] for row in result])

	count1=1
	for item in sorted_sim_dic_key:
		if count1>5:
			break
		print(item)
		count1=count1+1




# iter=0 
# for i in cosine_similarity(vect_model, search_tfidf):
# 	if i[0]>0:
# 		print(links[iter])
# 	iter=iter+1



# print(cosine_similarity)
# def Asearch(keyword):
