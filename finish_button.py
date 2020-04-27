import pandas as pd
import csv

def coursefind(unit):

	import syllabus as s

	for r in s.Dict1.values():
		for t in r:
			if (t.name == unit):
				course = 'Basics'
			else:
				for r in s.Dict2.values():
					for t in r:
						if (t.name == unit):
							course = 'HR'
						else:
							course = 'MM'
	return course	

def nncsv(time,mode,level,unit):
	course = coursefind(unit)

	f = open(course+'_Data.csv','r')
	r = csv.reader(f)
	lines1 = list(r)
	lines1.append(['0','0','0','0','0','0'])
	rows = len(lines1)
	lines1[rows-1][0] = time
	lines1[rows-1][1] = mode
	lines1[rows-1][2] = level
	lines1[rows-1][4] = lines1[rows-2][5]
	f.close()
	f = open(course+'_Data.csv','w')
	writer = csv.writer(f)
	writer.writerows(lines1)
	f.close()
	
	return course

def calc(userid,unit,time,mode,level): #returns 1 if current rate > threshold, else returns 0 ----> main function to be called

	course = nncsv(time,mode,level,unit)

	import final_nn as n
	
	curr_rate = n.lrcalculation(course) 

	#Current rate update in lr.csv
	df = pd.read_csv("lr.csv", usecols=['Userid','current_rate','Threshold'], engine='python')
	dataset = df.values
	dataset = dataset.astype('float32')
	rowno = 0
	for i in dataset:
		if(i[0] == userid):
			break
		rowno = rowno + 1
	
	dataset[rowno][1] = str(curr_rate)
	p = df['current_rate']
	p[rowno] = str(curr_rate)
	df['current_rate'] = p
	df.to_csv("lr.csv",index=False)

	

	userids, rate, threshold = dataset[rowno]

	if (rate < threshold):
		ret = 0
	else:
		ret = 1

	return ret
	
calc(2,"Boom",9,0.3,0.6)
