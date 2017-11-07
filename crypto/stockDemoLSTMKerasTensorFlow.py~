from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import lstm, time #helper libraries

#Step 1 Load Data and normalize it to improve convergence to reflect % changes from the starting point
X_train, y_train, X_test, y_test = lstm.load_data('sp500.csv', 50, True)

#Step 2 Build Model
model = Sequential()

model.add(LSTM(
    input_dim=1,
    #want 50 layers in this unit
    output_dim=50,
    #sets this layers output into the next layer by setting return seq to true
    return_sequences=True))
model.add(Dropout(0.2))

#next unit (outputs a prediction vector rather than a prediciton)
model.add(LSTM(
    100,
    return_sequences=False))
model.add(Dropout(0.2))

#dense layer to aggregate prediction into one single layer 
model.add(Dense(
    output_dim=1))
model.add(Activation('linear'))

#using mean squared error to compile this model and using rms prop as optimizer 
start = time.time()
model.compile(loss='mse', optimizer='rmsprop')
print 'compilation time : ', time.time() - start

#Step 3 Train the model
model.fit(
    X_train,
    y_train,
    batch_size=512,
    nb_epoch=1,
    validation_split=0.05)

#prediction next 50 steps
#Step 4 - Plot the predictions!
predictions = lstm.predict_sequences_multiple(model, X_test, 50, 50)
lstm.plot_results_multiple(predictions, y_test, 50)

