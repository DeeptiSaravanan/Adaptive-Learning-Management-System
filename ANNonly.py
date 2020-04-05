import numpy 
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from pandas import read_csv
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Activation
import math
from keras.optimizers import SGD
import csv
import pickle

numpy.random.seed(3)
import numpy 
import matplotlib.pyplot as plt
from keras.layers import GRU
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from pandas import read_csv
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Activation
import math
from keras.optimizers import SGD
from keras.optimizers import Adam
import csv
import pickle

numpy.random.seed(7)

#load the dataset for ANN
df1 = read_csv('MM_Data.csv', usecols=[0,1,2,3,5], engine='python') 
datasetlist1 = df1.values
datasetlist1 = datasetlist1.astype('float32')
dataset1 = datasetlist1[0:52,:]

# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):

	dataX, dataY = [], []	
	for i in range(len(dataset)-1):
		a = dataset[i:(i+look_back),0]
		dataX.append(a)
		dataY.append(dataset[i + look_back,0])
	return numpy.array(dataX), numpy.array(dataY)

#create and compile ANN network
adam = Adam(lr=0.01)

model1 = Sequential([
    	Dense(32, activation='relu', input_shape=(4,)),   #changed to (1,) from (4,)
    	Dense(32, activation='relu'),
    	Dense(1, activation='sigmoid'),
	])


model1.compile(optimizer='adam',
        loss='mae',
        metrics=['accuracy'])

iterno=52

dataframe = read_csv("MM_Data.csv", usecols=[4], engine='python').values
target1 = read_csv("MM_Data.csv", usecols=[3], engine='python').values
rows,col = dataframe.shape
#print(rows)
while(iterno < rows-1):

	print("----------Regression---------------")
	
	# rows,col = target1.shape
	# print(rows) rows gives 989
	df = dataframe[0:iterno]
	target = target1[0:iterno]
	#print(df)
	#print(target)

	X = df
	y = target

	lm = linear_model.LinearRegression()
	model = lm.fit(X,y)

	pred = numpy.reshape(dataframe[iterno], (dataframe[iterno].shape[0], 1))
	predictions = lm.predict(pred)

	target1[iterno] = predictions[0][0]
	datasetlist1[iterno][3] = predictions[0][0]
	print(predictions[0][0])
	f = open('MM_Data.csv','r')
	r = csv.reader(f) 
	lines1 = list(r)
	lines1[iterno+1][3] = predictions[0][0] #Changed from lines[iterno]
	f.close()
	f = open('MM_Data.csv','w')
	writer = csv.writer(f)
	writer.writerows(lines1)
	f.close()

	print("-------------Time for ANN---------------")

	dataset1 = numpy.append(dataset1,[datasetlist1[iterno,:]], axis=0)

	X = dataset1[0:iterno,0:4] 
	#print(X)
	Y = dataset1[0:iterno,4]
	#print(Y)


	X_train, X_v_test, Y_train, Y_v_test = train_test_split(X, Y, test_size=0.5)
	
	testingsize = len(X_v_test)
	X_val,X_test = X_v_test[:testingsize-1],X_v_test[testingsize-1]
	Y_val,Y_test = Y_v_test[:testingsize-1],Y_v_test[testingsize-1]
	

	history = model1.fit(X_train, Y_train,
          batch_size=32, epochs=10,
          validation_data=(X_val, Y_val))

	toPredict = dataset1[len(dataset1)-1,0:4]  

	toPredict = numpy.reshape(toPredict, (1,4,))


	Ynew = model1.predict(toPredict)

	print("Output")
	print(Ynew[0][0])

	dataset1[iterno][4] = Ynew[0][0]
	dataframe[iterno+1] = Ynew[0][0]

	print("---------------ANN done--------------")

	f = open('MM_Data.csv','r')
	r = csv.reader(f) # Check if you can save computation here
	#row = len(list(r))
	#print(r)
	#if(iterno+3 > row):
	#	r=numpy.append(r,numpy.array([0,0,0,0,0,0]))
	lines1 = list(r)
	row = len(lines1)
	#print(lines1)
	#print(lines1)
	#print(len(lines1))
	if(iterno+3 > row):
		lines1.append(['0','0','0','0','0','0'])
	lines1[iterno+1][5] = Ynew[0][0] #ERROR here.
	lines1[iterno+2][4] = Ynew[0][0]
	f.close()
	f = open('MM_Data.csv','w')
	writer = csv.writer(f)
	writer.writerows(lines1)
	f.close()
	
	iterno = iterno+1
	#count = count + 1
	#if count == 2:
	#	break
	

#model.save('MM_RNN.h5')
model1.save('MM.h5')
print("-------------Model Saved!---------------")






