from datasetcreator import DatasetCreator
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import numpy as np
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

n_timesteps = 20
n_train = 1000
n_test = 1000


x_train, y_train = DatasetCreator.create_simple(n_train, n_timesteps, 50)
x_test, y_test = DatasetCreator.create_simple(n_test, n_timesteps, 50)
x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], 1))
x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], 1))

print(x_train[1, :])
print(y_train[1])

# define model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(n_timesteps, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=10, verbose=2)

y_hat_test = model.predict(x_test, verbose=0)

np.savetxt('ys.txt', np.concatenate((y_test, y_hat_test), axis=1), delimiter='\t', fmt='%.5f')
