import keras.preprocessing.text
import numpy as np
import pandas as pd
np.random.seed(1337)  # for reproducibility
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from sklearn.metrics import (precision_score, recall_score,f1_score, accuracy_score,mean_squared_error,mean_absolute_error)
from sklearn import metrics
from sklearn.metrics import roc_auc_score
from keras.utils.np_utils import to_categorical
from sklearn.cross_validation import train_test_split


print("Loading")

traindata = pd.read_csv('eNews_2016_Train.csv', header=None)


x = traindata.iloc[:,0]
y = traindata.iloc[:,1]


X_train, X_test, y_train, y_test = train_test_split(x, y,test_size=0.2,random_state=42)


tk = keras.preprocessing.text.Tokenizer(nb_words=20000, filters=keras.preprocessing.text.base_filter(), lower=True, split="\t")
tk.fit_on_texts(X_train)
X_train = tk.texts_to_sequences(X_train)


tk = keras.preprocessing.text.Tokenizer(nb_words=20000, filters=keras.preprocessing.text.base_filter(), lower=True, split="\t")
tk.fit_on_texts(X_test)
X_test = tk.texts_to_sequences(X_test)

X_train=np.array(X_train)
X_test=np.array(X_test)


y_train = np.array(y_train)
y_test = np.array(y_test)

batch_size = 32
max_len = 80
print "max_len ", max_len
print('Pad sequences (samples x time)')

X_train = sequence.pad_sequences(X_train, maxlen=max_len)
X_test = sequence.pad_sequences(X_test, maxlen=max_len)

y_train= to_categorical(y_train)
y_test = to_categorical(y_test)


max_features = 20000
model = Sequential()
print('Build model...')

model = Sequential()
model.add(Embedding(max_features, 128, input_length=max_len, dropout=0.2))
model.add(LSTM(128, dropout_W=0.2, dropout_U=0.2))
model.add(Dense(5))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])


model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=15,
          validation_data=(X_test, y_test), shuffle=True)
score, acc = model.evaluate(X_test, y_test,
                            batch_size=batch_size)
print('Test score:', score)
print('Test accuracy:', acc)
