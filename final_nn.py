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

numpy.random.seed(7)
# load the dataset
dataframe = read_csv('newinput.csv', usecols=[4], engine='python')
dataset = dataframe.values
dataset = dataset.astype('float32')

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

# create and fit the LSTM network
model = Sequential()
model.add(LSTM(4, input_shape=(1,look_back)))
model.add(Dense(1, activation='relu'))
model.add(Activation('softmax'))

epochs = 10
learning_rate = 0.5
decay_rate = learning_rate/epochs
momentum = 0.5
sgd = SGD(lr=learning_rate,momentum=momentum,decay=decay_rate,nesterov=False)
model.compile(loss='mean_squared_error', optimizer='sgd')
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
no_rows = len(dataset)

f = open('newinput.csv','r')
r = csv.reader(f) # Check if you can save computation here
lines = list(r)
lines[no_rows][4] = testPredict[len(testPredict)-1][0]
f.close()
f = open('newinput.csv','w')
writer = csv.writer(f)
writer.writerows(lines)
f.close()

df = pd.DataFrame(columns=['Time','Level','Mode','NewRate'])
df = pd.read_csv('newinput.csv', engine='python')
dataset = df.values

X = dataset[:,0:4]
Y = dataset[:,4]

min_max_scaler = preprocessing.MinMaxScaler()
X_scale = min_max_scaler.fit_transform(X)

X_train, X_v_test, Y_train, Y_v_test = train_test_split(X_scale, Y, test_size=0.5)
print("Y_v_test")
print(Y_v_test)
X_val, X_test, Y_val, Y_test = train_test_split(X_v_test, Y_v_test, test_size=0.5)

#append_list_as_row('newinput.csv', row_contents)

model = Sequential([
    Dense(32, activation='relu', input_shape=(4,)),   #changed to (1,) from (4,)
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid'),
])

model.compile(optimizer='adam',
              loss='mse',
              metrics=['accuracy'])

history = model.fit(X_train, Y_train,
          batch_size=1, epochs=10,
          validation_data=(X_val, Y_val))

toPredict = X[len(dataset)-1]

toPredict = numpy.reshape(toPredict, (1,4,))


Ynew = model.predict(toPredict)
print(Ynew)


f = open('newinput.csv','r')
r = csv.reader(f) # Check if you can save computation here
lines = list(r)
lines[no_rows][5] = Ynew[0][0]
f.close()
f = open('newinput.csv','w')
writer = csv.writer(f)
writer.writerows(lines)
f.close()

# print("Enter the new set of parameters")
# Time = input()
# Level = input()
# Mode = input()
# Rate = Ynew



# acc = model.evaluate(X_test, Y_test)[1]
# print(acc)

