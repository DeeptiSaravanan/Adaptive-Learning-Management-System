import numpy 
import matplotlib.pyplot as plt
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_squared_log_error
from pandas import read_csv
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Activation, BatchNormalization
import math
from math import sqrt
from keras.optimizers import SGD
from keras.optimizers import Adam
import csv
import tensorflow as tf
import os

def lrcalculation(course):

	numpy.random.seed(7)
	# load the dataset
	dataframe = read_csv(course+"_Data.csv", usecols=[4], engine='python')
	datasetlist = dataframe.values
	rows, column = datasetlist.shape
	datasetlist = datasetlist.astype('float32')
	dataset = datasetlist[0:rows-1]

	# normalize the dataset
	scaler = MinMaxScaler(feature_range=(0, 1))
	dataset = scaler.fit_transform(dataset)

	# split into train and test sets
	train_size = int(len(dataset) * 0.5)
	test_size = len(dataset) - train_size
	train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

	# convert an array of values into a dataset matrix
	def create_dataset(dataset, look_back=1):

		dataX, dataY = [], []	
		for i in range(len(dataset)-1):
			a = dataset[i:(i+look_back),0]
			dataX.append(a)
			dataY.append(dataset[i + look_back,0])
		return numpy.array(dataX), numpy.array(dataY)

	# reshape into X=t and Y=t+1
	look_back = 1
	trainX, trainY = create_dataset(train, look_back)
	testX, testY = create_dataset(test, look_back)

	# reshape input to be [samples, time steps, features]
	trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
	testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

	trainY = numpy.reshape(trainY, (-1,1))
	testY = numpy.reshape(testY, (-1,1))

	model = tf.keras.models.load_model(course+"_RNN.h5", compile=False) #added compile=False and the next line

	model.compile(loss='mean_squared_error', optimizer='sgd')
	model.fit(trainX, trainY, epochs=10, batch_size=32, verbose=2)
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
	no_rows = len(datasetlist)

	f = open(course+'_Data.csv','r')
	r = csv.reader(f) # Check if you can save computation here
	lines = list(r)
	lines[no_rows][3] = testPredict[len(testPredict)-1][0]
	f.close()
	f = open(course+'_Data.csv','w')
	writer = csv.writer(f)
	writer.writerows(lines)
	f.close()

	df = pd.read_csv(course+'_Data.csv', usecols=[0,1,2,3,5], engine='python')
	datasetlist1 = df.values
	datasetlist1 = datasetlist1.astype('float32')
	dataset1 = datasetlist1[0:rows-1,:]
	no_rows = len(datasetlist1)

	X = dataset1[:,0:4]
	Y = dataset1[:,4]

	X_train, X_v_test, Y_train, Y_v_test = train_test_split(X, Y, test_size=0.5)
	testingsize = len(X_v_test)
	X_val,X_test = X_v_test[:testingsize-1],X_v_test[testingsize-1]
	Y_val,Y_test = Y_v_test[:testingsize-1],Y_v_test[testingsize-1]

	model1 = tf.keras.models.load_model(course+"_ANN.h5",compile=False)
	model1.compile(loss='mean_squared_error', optimizer='Adam')

	history = model1.fit(X_train, Y_train,
          	batch_size=32, epochs=10,
          	validation_data=(X_val, Y_val))

	toPredict = datasetlist1[no_rows-1,0:4]

	toPredict = numpy.reshape(toPredict, (1,4,))


	Ynew = model1.predict(toPredict)
	print(Ynew[0][0])


	f = open(course+'_Data.csv','r')
	r = csv.reader(f) # Check if you can save computation here
	lines = list(r)
	lines[no_rows][5] = Ynew[0][0]
	f.close()
	f = open(course+'_Data.csv','w')
	writer = csv.writer(f)
	writer.writerows(lines)
	f.close()
	
	#if os.path.exists(course+'_RNN.model'):
	#	os.remove(course+'_RNN.model')

	#if os.path.exists(course+"_ANN.model"):
	#	os.remove(course+"_ANN.model")

	#tf.keras.models.save_model(model, course+"_RNN.model", overwrite=True, include_optimizer=True, save_format=None, signatures=None, options=None)

	model.save(course+'_RNN.h5')
	model1.save(course+'_ANN.h5')

	return Ynew[0][0]


lrcalculation("BM")