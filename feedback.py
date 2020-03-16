import pandas as pd
import csv
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

def feedback(mode,topic,rowno,onclick):

	threshold = -3

	if(topic in Basics_lis and mode == 'Book'):
		csvfile = 'Basics.csv'
	elif(topic in HR_lis and mode == 'Book'):
		csvfile = 'HR.csv'
	elif(topic in MM_lis and mode == 'Book'):
		csvfile = 'MM.csv'
	else:
		csvfile = 'KB.csv'
	
	df = pd.read_csv(csvfile, index_col=False)

	if(onclick == 1):
		p = df['Score'].values
		p[rowno] = str(int(p[rowno])+1)
	else:
		p = df['Score'].values
		p[rowno] = str(int(p[rowno])-1)

	df['Score'] = p
	Index_label = df[df['Score']<-2].index.tolist()
	 
	df = df.drop(df.index[Index_label[0]])
	Index_label.pop(0)
	
	for i in Index_label:
		i = i-1
		df = df.drop(df.index[i])
	df = df.sort_values(by='Score', ascending=False)
	#print(df)
	df.to_csv(csvfile, index=False)


	
feedback('Book','Behaviour',0,1)
