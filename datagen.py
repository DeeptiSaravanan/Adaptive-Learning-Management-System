import random
from random import gauss
import csv
import pandas as pd
from sklearn import preprocessing
import numpy as np

random.seed(50)

def timebook():
	c=0
	value = []

	while(c < 1000):
		for _ in range(50,180):
			values = round(gauss(115, 50))
			if(values > 0  and values < 181):
				value.append(values)
			c = c+1
	
#50-90, 91-130, 131-180	

	with open('randata_book.csv','w') as outfile:
		outfile.write('Time')
		outfile.write('\n')
		for v in value:
			outfile.write(str(v))
			outfile.write('\n')
	
	f = open('randata_book.csv','r')
	reader = csv.reader(f)
	next(reader, None)
	df = pd.DataFrame.from_records(reader)
	x = df[0].values.astype(float)
	y = []
	
	for val in x:
		if(val>49 and val<91):
			y.append('0.3')
		elif(val>89 and val<131):
			y.append('0.6')
		else:
			y.append('0.9')

	df[1] = pd.DataFrame(y)
	df.to_csv('randata_book.csv')

def timevideo():
	c=0
	value = []

	while(c < 1000):
		for _ in range(9,60):
			values = round(gauss(35, 15))
			if(values > 5  and values < 75):
				value.append(values)
				c = c+1


	with open('randata_video.csv','w') as outfile:
		outfile.write('Time')
		outfile.write('\n')
		for v in value:
			outfile.write(str(v))
			outfile.write('\n')

def timearticle():
	c=0
	value = []

	while(c < 1000):
		for _ in range(5,20):
			values = round(gauss(5, 10))
			if(values > 3  and values < 20):
				value.append(values)
				c = c+1


	with open('randata_article.csv','w') as outfile:
		outfile.write('Time')
		outfile.write('\n')
		for v in value:
			outfile.write(str(v))
			outfile.write('\n')

#5-10,11-15,16-20

	f = open('randata_article.csv','r')
	reader = csv.reader(f)
	next(reader, None)
	df = pd.DataFrame.from_records(reader)
	x = df[0].values.astype(float)
	y = []
	
	for val in x:
		if(val>4 and val<11):
			y.append('0.3')
		elif(val>10 and val<16):
			y.append('0.6')
		else:
			y.append('0.9')

	df[1] = pd.DataFrame(y)
	df.to_csv('randata_article.csv')

#timebook()
#timevideo()
#timearticle()

def learning_rate(csvfile):
	rowlist = []
	sum_e=0
	sum_m = 0
	sum_h = 0
	c1=0
	c2 = 0
	c3 = 0
	with open(csvfile,'r') as infile:
		reader = csv.reader(infile)
		next(reader, None)
		for row in reader:
			rowlist.append(row)
	infile.close()
	
				
	for r in rowlist:
		#print(r)
		if(r[1] == '0.3'):
			#print("easy")
			sum_e = sum_e+ float(r[0])
			c1 = c1 + 1
		elif(r[1] == '0.6'):
			sum_m = sum_m + float(r[0])
			c2 = c2 + 1
		else:
			sum_h = sum_h + float(r[0])
			c3 = c3 + 1
	timeavg_e = sum_e/c1
	timeavg_m = sum_m/c2
	timeavg_h = sum_h/c3
	for r in rowlist:
		if( r[1] == 0.3):
			lr = (timeavg_e * float(r[2])) / float(r[0])
			r[3] = lr
		elif(r[1] == 0.6):
			lr = (timeavg_m * float(r[2])) / float(r[0])
			r[3] = lr
		else:
			lr = (timeavg_h * float(r[2])) / float(r[0])
			r[3] = lr
		
	
	f = open(csvfile,'w')
	writer = csv.writer(f)
	writer.writerows(rowlist)
	f.close()

def normalise(csvfile):
	f = open(csvfile,'r')
	reader = csv.reader(f)
	df = pd.DataFrame.from_records(reader)	
	#print(df)
	#print(df[3].values.astype(float))
	x = df[3].values.astype(float)
	x = np.reshape(x, (-1, 1))
	#print(x.shape)
	min_max_scaler = preprocessing.MinMaxScaler()
	x_scaled = min_max_scaler.fit_transform(x)
	x_scaled = x_scaled * 100
	for val in x_scaled:
		if(val[0]>1):
			val[0]=1
	df[3] = pd.DataFrame(x_scaled)
	#print(df)
	
	df.to_csv(csvfile)

def datasplit(csvfile,newcsvfile):
	f = open(csvfile,'r')
	reader = csv.reader(f)
	df = pd.DataFrame.from_records(reader)
	#print(df)
	c=len(df.index)
	new_df = df[1:round(c/3)]
	#new_df.to_csv(newcsvfile, index=False)
	new_df.to_csv(newcsvfile, mode='a', header=False, index=False)

#datasplit("randata_article.csv","BasicsData.csv")
#timevideo()
#learning_rate('randata_book.csv')
#normalise('randata_book.csv')
