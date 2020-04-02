import numpy 
import matplotlib.pyplot as plt
from keras.layers import LSTM
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

numpy.random.seed(7)
# load the dataset for RNN

dataframe = read_csv('HRData.csv', usecols=[4], engine='python')
datasetlist = dataframe.values
datasetlist = datasetlist.astype('float32')
#rows, column = datasetlist.shape
datasets = datasetlist[0:3]

#load the dataset for ANN
df = read_csv('HRData.csv', usecols=[0,1,2,3,5], engine='python')
datasetlist1 = df.values
datasetlist1 = datasetlist1.astype('float32')
dataset1 = datasetlist1[0:3,:]

look_back = 1
# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):

	dataX, dataY = [], []	
	for i in range(len(dataset)-1):
		a = dataset[i:(i+look_back),0]
		dataX.append(a)
		dataY.append(dataset[i + look_back,0])
	return numpy.array(dataX), numpy.array(dataY)

# create and compile the LSTM network
model = Sequential()
model.add(LSTM(4, input_shape=(1,look_back)))
model.add(Dense(1, activation='relu'))
model.add(Activation('softmax'))

epochs = 100
learning_rate = 0.5
decay_rate = learning_rate/epochs
momentum = 0.5
sgd = SGD(lr=learning_rate,momentum=momentum,decay=decay_rate,nesterov=False)
model.compile(loss='mean_squared_error', optimizer='sgd')


#create and compile ANN network
model1 = Sequential([
    	Dense(32, activation='relu', input_shape=(4,)),   #changed to (1,) from (4,)
    	Dense(32, activation='relu'),
    	Dense(1, activation='sigmoid'),
	])

model1.compile(optimizer='adam',
        loss='mse',
        metrics=['accuracy'])

iterno=3

while(iterno < 989):
	datasets = numpy.append(datasets,[datasetlist[iterno]], axis=0)
	dataset = datasets
	#dataset.astype('float32')
	print("---------Next data----------")
	#print(dataset)
	# normalize the dataset
	scaler = MinMaxScaler(feature_range=(0, 1))
	dataset = scaler.fit_transform(dataset)

	# split into train and test sets
	train_size = int(len(dataset) * 0.5)
	test_size = len(dataset) - train_size
	train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

	# reshape into X=t and Y=t+1
	
	trainX, trainY = create_dataset(train, look_back)
	testX, testY = create_dataset(test, look_back)
	#print(trainX.shape)
	# reshape input to be [samples, time steps, features]
	trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
	testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

	trainY = numpy.reshape(trainY, (-1,1))
	testY = numpy.reshape(testY, (-1,1))

	model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)
	# make predictions
	trainPredict = model.predict(trainX)
	testPredict = model.predict(testX)

	# invert predictions

	trainPredict = scaler.inverse_transform(trainPredict)
	trainY = scaler.inverse_transform(trainY)
	testPredict = scaler.inverse_transform(testPredict)
	testY = scaler.inverse_transform(testY)

	print("Learning rate is:")
	print(testPredict[len(testPredict)-1])
	#no_rows = len(dataset)
	print("-----------------RNN done!----------------------")

	if(testPredict[len(testPredict)-1][0] >= 0.9):
		testPredict[len(testPredict)-1][0] = (datasets[iterno] + datasets[iterno-1]+ datasets[iterno-2])/3
	elif(testPredict[len(testPredict)-1][0] < 0.1):
		testPredict[len(testPredict)-1][0] = (datasets[iterno] + datasets[iterno-1])/3
	elif(math.isnan(testPredict[len(testPredict)-1][0]) == True):
		testPredict[len(testPredict)-1][0] = datasets[iterno]

	print("-------------Time for ANN---------------")

	datasets[iterno] = testPredict[len(testPredict)-1][0]

	f = open('HRData.csv','r')
	r = csv.reader(f) # Check if you can save computation here
	lines = list(r)
	lines[iterno+1][3] = testPredict[len(testPredict)-1][0]
	f.close()
	f = open('HRData.csv','w')
	writer = csv.writer(f)
	writer.writerows(lines)
	f.close()
	
	
	#print(datasetlist1)
	#dataset1 = numpy.array([[datasetlist1[0,:]],datasetlist1[1,:],datasetlist1[2,:]])
	#print(dataset1)
	#print(dataset1.shape)

	dataset1 = numpy.append(dataset1,[datasetlist1[iterno,:]], axis=0)

	print("------------Get ready for action-------------")

	X = dataset1[:,0:4]
	Y = dataset1[:,4]

	min_max_scaler = preprocessing.MinMaxScaler()
	X_scale = min_max_scaler.fit_transform(X)

	X_train, X_v_test, Y_train, Y_v_test = train_test_split(X_scale, Y, test_size=0.5)
	#print("Y_v_test")
	#print(Y_v_test)
	#X_val, X_test, Y_val, Y_test = train_test_split(X_v_test, Y_v_test, test_size=0.5)
	testingsize = len(X_v_test)
	X_val,X_test = X_v_test[:testingsize-1],X_v_test[testingsize-1]
	Y_val,Y_test = Y_v_test[:testingsize-1],Y_v_test[testingsize-1]
	#append_list_as_row('newinput.csv', row_contents)

	history = model1.fit(X_train, Y_train,
          batch_size=1, epochs=100,
          validation_data=(X_val, Y_val))

	toPredict = X[len(dataset1)-1]

	toPredict = numpy.reshape(toPredict, (1,4,))


	Ynew = model1.predict(toPredict)
	#print(Ynew)

	if(Ynew[0][0] > 0.9):
		Ynew[0][0] = (Y[iterno-1]+Y[iterno-2]+Y[iterno-3])/3
	elif(Ynew[0][0] < 0.5):
		Ynew[0][0] = (Y[iterno-1]+Y[iterno-2])/3
	elif(math.isnan(Ynew[0][0]) == True):
		Ynew[0][0] = Y[iterno-1]

	print("Output")
	print(Ynew[0][0])

	dataset1[iterno][4] = Ynew[0][0]

	print("---------------ANN done--------------")

	f = open('HRData.csv','r')
	r = csv.reader(f) # Check if you can save computation here
	lines1 = list(r)
	lines1[iterno+1][5] = Ynew[0][0]
	lines1[iterno+2][4] = Ynew[0][0]
	f.close()
	f = open('HRData.csv','w')
	writer = csv.writer(f)
	writer.writerows(lines1)
	f.close()
	iterno = iterno+1

model.save('HR_RNN.h5')
model1.save('HR_ANN.h5')

#saved_model = pickle.dumps(model)
# print("Enter the new set of parameters")
# Time = input()
# Level = input()
# Mode = input()
# Rate = Ynew



# acc = model.evaluate(X_test, Y_test)[1]
# print(acc)
	
	


