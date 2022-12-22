import tensorflow as tf
import sklearn
import numpy as np
import matplotlib.pyplot as plt

from sklearn.pipeline import make_pipeline
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train_r = x_train.reshape(x_train.shape[0], x_train.shape[1]*x_train.shape[2])
x_test_r = x_test.reshape(x_test.shape[0], x_test.shape[1]*x_test.shape[2])

pca = PCA(n_components=68)
pca.fit(x_train_r)
x_tr = pca.transform(x_train_r)
x_te = pca.transform(x_test_r)

model1 = QuadraticDiscriminantAnalysis()


model1.fit(x_tr, y_train)
from sklearn.metrics import accuracy_score
print(f'Accuracy: {accuracy_score(y_test, [model1.predict(x.reshape(1, -1))[0] for x in x_te])*100}%')