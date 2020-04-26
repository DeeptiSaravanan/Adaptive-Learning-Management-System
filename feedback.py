import pandas as pd
import csv

def valpass(): #Function to obtain syllabus information
	
	import syllabus as s

	Basics_lis = []
	HR_lis = []
	MM_lis = []

	
	for r in s.Dict1.values():
		for t in r:
			Basics_lis.append(t.name)
	for r in s.Dict2.values():
		for t in r:
			HR_lis.append(t.name)
	for r in s.Dict3.values():
		for t in r:
			MM_lis.append(t.name)

	return Basics_lis,HR_lis,MM_lis

def feedback(mode,topic,title,onclick): #Main Function to be called!

	Basics_lis,HR_lis,MM_lis = valpass()
	
	threshold = -3

	if(topic in Basics_lis and mode == 'Book'):
		csvfile = 'BM_books.csv'
	elif(topic in HR_lis and mode == 'Book'):
		csvfile = 'HR_books.csv'
	elif(topic in MM_lis and mode == 'Book'):
		csvfile = 'MM_books.csv'
	else:
		csvfile = 'KB.csv'
	
	df = pd.read_csv(csvfile, index_col=False)
	t = df['Description'].values
	p = df['Score'].values
	k=0
	for titles in t:
		if(titles == title):
			rowno = k
			break
		else:
			k = k+1

	if(onclick == 1):
		p[rowno] = str(int(p[rowno])+1)
	else:
		p[rowno] = str(int(p[rowno])-1)

	df['Score'] = p
	Index_label = df[df['Score']<-2].index.tolist()
	#print(Index_label)
	
	if len(Index_label) != 0:
		df = df.drop(df.index[Index_label[0]])
		Index_label.pop(0)
			
		for i in Index_label:
			i = i-1
			df = df.drop(df.index[i])
	df = df.sort_values(by='Score', ascending=False)
	#print(df)
	df.to_csv(csvfile, index=False)

feedback('Article','Behaviour','Brand Management',1)
