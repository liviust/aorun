import os
import sys
sys.path.insert(0, os.path.abspath('..'))

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

import numpy as np
from aorun.models import Model
from aorun.layers import ProbabilisticDense
from aorun.layers import Activation
from aorun.optimizers import SGD

X, y = datasets.load_iris(return_X_y=True)
X = X.astype('float32')
y = np.eye(y.max() + 1)[y].astype('float32')
X = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
print(X_train.shape, y_train.shape)

model = Model(
    ProbabilisticDense(10, input_dim=X_train.shape[-1]),
    Activation('relu'),
    ProbabilisticDense(10),
    Activation('relu'),
    ProbabilisticDense(y_test.shape[-1]),
    Activation('softmax')
)

sgd = SGD(lr=0.1)
history = model.fit(X_train, y_train, n_epochs=500,
                    loss='categorical_crossentropy', optimizer=sgd)

y_pred = model.forward(X_test)
acc = metrics.accuracy_score(y_test.argmax(axis=1), y_pred.argmax(axis=1))
print('Accuracy:', acc)