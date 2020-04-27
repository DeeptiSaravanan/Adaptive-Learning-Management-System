import numpy as np
import pandas as pd
import csv

def row_no(userid):
	rowno = 1
	df = pd.read_csv("lr.csv", usecols=['Userid'], engine='python')
	dataset = df.values
	dataset = dataset.astype('float32')
	for i in dataset:
		if i == userid:
			break
		rowno = rowno + 1
	return rowno

def diag_fail(userid, level):  
	
	df = pd.read_csv("lr.csv", usecols=['Userid','current_rate'], engine='python')
	dataset = df.values
	dataset = dataset.astype('float32')

	df1 = pd.read_csv("lr.csv", usecols=[level], engine='python')
	dataset1 = df1.values
	dataset1 = dataset1.astype('float32')

	val=0
	count=0

	rowno = row_no(userid)
	
	rates = dataset[rowno-1]

	#print(dataset1)

	for i in dataset1:
        	if(i!=0):
            		val = val + i
            		count = count+1

	if(count == 0 ):
		new_th = rates[1] + 0.05

	else:
		th = val/count
		new_th = th[0]

	if(new_th <= rates[1]):
		new_th = rates[1] + 0.05
		
	
	f = open('lr.csv','r')
	r = csv.reader(f) # Check if you can save computation here
	lines = list(r)		
	lines[rowno][2] = new_th
	f.close()
	f = open('lr.csv','w')
	writer = csv.writer(f)
	writer.writerows(lines)
	f.close()
	
def diag_pass(userid, level, score):
	
	df = pd.read_csv("lr.csv", usecols=['current_rate',level], engine='python')
	dataset = df.values
	dataset = dataset.astype('float32')
	#print(df)
	maxscore = 100
	rowno = row_no(userid)
	curr = dataset[rowno][0]
	#print(curr)
	#print('\n')
	val = curr * score
	val = val/maxscore
	#print(val)

	f = open('lr.csv','r')
	r = csv.reader(f) # Check if you can save computation here
	lines = list(r)	
	#print(lines)
	#col = df.columns[df.columns.str.contains(level)]
	#col = "'" + level + "'"	
	#print(col)
	#print(lines[0])
	col = 0
	col1 = 0
	for i in lines[0]:
		if(i == level):
			break
		col = col+1
	for j in lines[0]:
		if(j=='Threshold'):
			break
		col1 = col1+1
	lines[rowno][col] = val
	if(level=='Controlling' or level=='Evaluation' or level=='Behaviour' or level=='Trends'):
		lines[rowno][col1] = 0.2
	#f.close()
	f = open('lr.csv','w')
	writer = csv.writer(f)
	writer.writerows(lines)
	f.close()

#diag_fail(1,'Trends')
#diag_pass(1, 'Trends', 100)
	

