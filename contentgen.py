import pandas as pd
import csv
from youtube import Ysearch

def congen(course,unit,preference):

	if(preference == 'video'):
		vgen(unit)
	elif(preference == 'article'):
		agen(unit)
	else:
		bgen(course)

def vgen(unit):
	Ysearch(unit)

def agen(unit):
	return 0	
	

def bgen(course):
	
	if(course == 'Basics of Management'):  #Whatever is the coursename mentioned in the webpage
		f = open('Basics.csv','r')
		reader = csv.reader(f)
		next(reader, None)
		df = pd.DataFrame.from_records(reader)
		x = df[0].values
		print(x)

	elif(course == 'Human Resouce Management'):
		f = open('HR.csv','r')
		reader = csv.reader(f)
		next(reader, None)
		df = pd.DataFrame.from_records(reader)
		x = df[0].values
		print(x)
	else:
		f = open('MM.csv','r')
		reader = csv.reader(f)
		next(reader, None)
		df = pd.DataFrame.from_records(reader)
		x = df[0].values
		print(x)

#bgen("Marketing Management")
#vgen("Market Segmentation")	
	
