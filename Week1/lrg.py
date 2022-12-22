import tensorflow as tf
import sklearn
import numpy as np
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train_r = x_train.reshape(x_train.shape[0], x_train.shape[1]*x_train.shape[2])
x_test_r = x_test.reshape(x_test.shape[0], x_test.shape[1]*x_test.shape[2])

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

clf = make_pipeline(StandardScaler(), LogisticRegression(multi_class="multinomial"))
clf.fit(x_train_r, y_train)

from sklearn.metrics import accuracy_score
print(f'Accuracy: {accuracy_score(y_test, [clf.predict(x.reshape(1, -1))[0] for x in x_test_r])*100}%')