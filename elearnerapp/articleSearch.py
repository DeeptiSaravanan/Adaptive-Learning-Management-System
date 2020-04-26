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


df=pd.read_csv('ArticleKB.csv')
keywords=df['Description'].astype(str).values.tolist()
links=df['Link'].astype(str).values.tolist()

def clean_string(text):
	text=''.join([word for word in text if word not in string.punctuation])
	text=text.lower()
	text=' '.join([word for word in text.split() if word not in stopwords and len(word)>2 and word!='nan'])
	return text

def Asearch(subject,unit):
	cleaned = list(map(clean_string,keywords))
	tfidf_vect = TfidfVectorizer()
	vect_model = tfidf_vect.fit_transform(cleaned)
	result=[]
	final_links=[]
	titles=[]
	if subject=="BM":
		iterable = s.Dict1.values()
	elif subject=="HR":
		iterable=s.Dict2.values()
	elif subject=="MM":
		iterable=s.Dict3.values()

	title_map={'Introduction':'Introduction','Planning':'Planning','Organising':'Organising','Directing':'Directing','Controlling':'Controlling','Perspectives':'Perspectives','BestFit':'BestFit','Introduction to Marketing':'Intro_marketing', 'Training':'Training', 'EmpInterest':'EmpInterest','Marketing Strategy':'Strategy', 'Marketing Mix Decisions':'MixDecisions','Evaluation':'Evaluation','Buyer Behaviour':'Behaviour','Marketing Research and Trends in Marketing':'Trends'}
	unit=title_map[unit]
	for r in iterable:
		for t in r:
			if t.name==unit:
			 for text in t.topics:
			 	search_string=clean_string(text)
			 	search_tfidf=tfidf_vect.transform([search_string])

			 	csim_arr=cosine_similarity(vect_model, search_tfidf)
			 	csim=csim_arr.tolist()
			 	sim_dic = dict(zip(links,csim))
			 	sim_dic_key= dict(zip(keywords,csim))
			 	sorted_sim_dic = sorted(sim_dic.items(), key=operator.itemgetter(1),reverse=True)
			 	sorted_sim_dic_key = sorted(sim_dic_key.items(), key=operator.itemgetter(1),reverse=True)

			 	for item,value in sorted_sim_dic:
			 		if value[0]<0.7:
			 			break
			 		final_links.append(item)

			 	for item,value in sorted_sim_dic_key:
			 		if value[0]<0.7:
			 			break
			 		titles.append(item)


	return dict(zip(final_links,titles))
	

	

# Asearch("MM","Strategy")