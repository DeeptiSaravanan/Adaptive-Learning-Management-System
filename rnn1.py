
# LSTM for international airline passengers problem with regression framing
import numpy
import matplotlib.pyplot as plt
from pandas import read_csv
import math
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

numpy.random.seed(7)
# load the dataset
#dataframe = read_csv('newinput.csv', usecols=[3], engine='python')
dataframe = read_csv('newinput.csv', engine='python')
dataset = dataframe.values
dataset = dataset.astype('float32')

# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)
#print(len(dataset))
# split into train and test sets
train_size = int(len(dataset) * 0.5)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]
#print(train.shape)
# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):

	dataX, dataY = [], []	
	#print(len(dataset))
	#for i in range(len(dataset)-look_back-1):
	for i in range(len(dataset)-1):
		#print(dataset)
		a = dataset[i:(i+look_back), :]
		#print(a.shape)
		dataX.append(a)
		dataY.append(dataset[i + look_back, :])
		#print("next")
		#print(dataX)
		#print(dataY)
	return numpy.array(dataX), numpy.array(dataY)

# reshape into X=t and Y=t+1
look_back = 1
trainX, trainY = create_dataset(train)
testX, testY = create_dataset(test, look_back)
#print(trainX.shape)
# reshape input to be [samples, time steps, features]
trainX = numpy.reshape(trainX, (trainX.shape[0], 1, trainX.shape[2]))
testX = numpy.reshape(testX, (testX.shape[0], 1, testX.shape[2]))
print(trainX.shape)
print(testX.shape)
# create and fit the LSTM network
model = Sequential()
#model.add(LSTM(4, input_shape=(1, look_back)))
model.add(LSTM(4, input_shape=(look_back,4)))
model.add(Dense(4))
model.compile(loss='mean_squared_logarithmic_error', optimizer='adam')
model.fit(trainX, trainY, epochs=10, batch_size=1, verbose=2)

# make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)
#trainY = numpy.reshape(trainY, (trainY.shape[0], 1, trainY.shape[1]*trainY.shape[2]))
# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform(trainY)
testPredict = scaler.inverse_transform(testPredict)
testY = scaler.inverse_transform(testY)

print(trainY)
print('\n')
print(testY)
print('\n')
print(testPredict)
print("Learning rate is:")
print(testPredict[len(testPredict)-1][3])


