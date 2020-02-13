import pandas as pd
from sklearn import preprocessing
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
          batch_size=1, epochs=10,
          validation_data=(X_val, Y_val))

Ynew = model.predict(X_test)

print(Y_test)
print(Ynew)
acc = model.evaluate(X_test, Y_test)[1]
print(acc)

