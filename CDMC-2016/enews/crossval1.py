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
from keras.layers import Dropout
from sklearn.cross_validation import StratifiedKFold
from sklearn.cross_validation import cross_val_score
from keras.wrappers.scikit_learn import KerasClassifier

print("Loading")

traindata = pd.read_csv('eNews_2016_Train.csv', header=None)


x = traindata.iloc[:,0]
y = traindata.iloc[:,1]


tk = keras.preprocessing.text.Tokenizer(nb_words=5000, filters=keras.preprocessing.text.base_filter(), lower=True, split=" ")
tk.fit_on_texts(x)
X_train = tk.texts_to_sequences(x)


X_train=np.array(X_train)
y_train1 = np.array(y)

y_train = to_categorical(y_train1)


batch_size = 64
max_len = 500
print "max_len ", max_len
print('Pad sequences (samples x time)')

X_train = sequence.pad_sequences(X_train, maxlen=max_len)

max_features = 5000
model = Sequential()
print('Build model...')
embedding_vecor_length = 32

def create_model():
   model = Sequential()
   model.add(Embedding(max_features, embedding_vecor_length, input_length=max_len))
   model.add(Dropout(0.2))
   model.add(LSTM(100))
   model.add(Dropout(0.2))
   model.add(Dense(5))
   model.add(Activation('softmax'))
   model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
   print(model.summary())
   return model


# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

model = KerasClassifier(build_fn=create_model, nb_epoch=30, batch_size=32)

# evaluate using 10-fold cross validation
kfold = StratifiedKFold(y=y_train1, n_folds=10, shuffle=True, random_state=seed)
results = cross_val_score(model, X_train, y_train, cv=kfold)
print(results.mean())


