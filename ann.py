import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

df = pd.read_csv('ann.csv')
dataset = df.values
#print(dataset[:,4])
X = dataset[:,0:4]
Y = dataset[:,4]

min_max_scaler = preprocessing.MinMaxScaler()
X_scale = min_max_scaler.fit_transform(X)

X_train, X_v_test, Y_train, Y_v_test = train_test_split(X_scale, Y, test_size=0.5)
X_val, X_test, Y_val, Y_test = train_test_split(X_v_test, Y_v_test, test_size=0.5)

model = Sequential([
    Dense(32, activation='relu', input_shape=(4,)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid'),
])

model.compile(optimizer='adam',
              loss='mse',
              metrics=['accuracy'])

history = model.fit(X_train, Y_train,
          batch_size=1, epochs=10, verbose=0,
          validation_data=(X_val, Y_val))

Ynew = model.predict(X_test)

#print(Y_test.shape)
#print(Ynew)

Y_test = np.reshape(Y_test, (-1,1))

def mean_ab_per_error(Y_test, Ynew):
	#Y_test, Ynew = check_array(Y_test, Ynew)
	Y_test, Ynew = np.array(Y_test), np.array(Ynew)
	return np.mean(np.abs((Y_test - Ynew) / Y_test)) * 100

err = mean_ab_per_error(Y_test, Ynew)
r_sq = r2_score(Y_test, Ynew)
print("Mean Absolute Percentage Error: " + str(err))
print("R squared score: " + str(r_sq))

