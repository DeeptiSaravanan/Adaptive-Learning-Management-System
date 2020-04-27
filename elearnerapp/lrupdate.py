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

def diag_fail(userid,unit):
	idlist = []
	df = pd.read_csv("lr.csv", usecols=['Userid','current_rate',unit], engine='python')
	dataset = df.values
	dataset = dataset.astype('float32')
	val=0
	count=0
	for i in dataset[1]:
			if i:
					val = val + i
					count = count+1
	if count==0:
		count=1
		curr = dataset[rowno][1]
		val=score*curr

	


	new_th = val/count

	rowno = row_no(userid)
	f = open('lr.csv','r')
	r = csv.reader(f) # Check if you can save computation here
	lines = list(r)		
	lines[rowno][2] = new_th
	f.close()
	f = open('lr.csv','w')
	writer = csv.writer(f)
	writer.writerows(lines)
	f.close()
	
def diag_pass(userid, unit, score):
	
	df = pd.read_csv("lr.csv", usecols=['current_rate',unit], engine='python')
	dataset = df.values
	dataset = dataset.astype('float32')

	rowno = row_no(userid)
	curr = dataset[rowno][1] #Changed it to [rowno][1]
	val = curr * score/100

	

	f = open('lr.csv','r')
	r = csv.reader(f) # Check if you can save computation here
	lines = list(r)	
	#print(lines)
	col = df.columns[df.columns.str.contains(level)]
	#col = "'" + level + "'"	
	#print(col)
	#print(lines[0])
	col = 0
	for i in lines[0]:
		if i == level:
			break
		col = col+1
	lines[rowno][col] = val
	#f.close()
	f = open('lr.csv','w')
	writer = csv.writer(f)
	writer.writerows(lines)
	f.close()

#diag_pass(2,'BH',80)
# diag_fail(2)

	

