import tensorflow as tf
import sklearn
import numpy as np
import matplotlib.pyplot as plt

from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train_r = x_train.reshape(x_train.shape[0], x_train.shape[1]*x_train.shape[2])
x_test_r = x_test.reshape(x_test.shape[0], x_test.shape[1]*x_test.shape[2])

model1 = make_pipeline(StandardScaler(), LogisticRegression(multi_class = 'multinomial'))
model1.fit(x_train_r, y_train)
from sklearn.metrics import accuracy_score
print(f'Accuracy: {accuracy_score(y_test, [model1.predict(x.reshape(1, -1))[0] for x in x_test_r])*100}%')
