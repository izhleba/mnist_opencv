# Import the modules
import random
import time

from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.datasets import fetch_mldata
from skimage.feature import hog
from sklearn.svm import LinearSVC
import numpy as np
from collections import Counter
from sklearn import metrics

# Load the dataset
print "Download dataset..."
mnist = fetch_mldata('MNIST original')
n_train = 60000
n_test = 10000


indices = np.arange(len(mnist.data))
random.seed(0)
train_idx = np.arange(0, n_train)
test_idx = np.arange(n_train + 1, n_train + n_test)

X_train, y_train = mnist.data[train_idx], mnist.target[train_idx]
X_test, y_test = mnist.data[test_idx], mnist.target[test_idx]

start = time.time()
print "Extract features"


def hog_features(data_x):
    list_hog_fd = []
    perc = 0
    size = data_x.shape[0]
    for i, feature in enumerate(data_x):
        fd = hog(feature.reshape((28, 28)), orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1),
                 visualise=False)
        list_hog_fd.append(fd)
        new_perc = (i * 100) / (size - 1)
        if new_perc > perc + 5 or new_perc == 100:
            perc = new_perc
            print new_perc, "%"
    return np.array(list_hog_fd, 'float64')


hog_features_train = hog_features(X_train)

hog_features_test = hog_features(X_test)

print "Count of digits in dataset", Counter(y_train)


clf = LinearSVC()
clf.fit(hog_features_train, y_train)
print "Mean SVN accuracy: \t", (1 - clf.score(hog_features_test, y_test))
clf = LinearSVC()
clf.fit(np.concatenate((hog_features_train, hog_features_test)), np.concatenate((y_train, y_test)))
joblib.dump(clf, "digits_svn.pkl", compress=3)

clf = RandomForestClassifier(n_estimators=20, n_jobs=4)
clf.fit(hog_features_train, y_train)
print "Mean RF accuracy: \t", (1 - clf.score(hog_features_test, y_test))
clf = LinearSVC()
clf.fit(np.concatenate((hog_features_train, hog_features_test)), np.concatenate((y_train, y_test)))
joblib.dump(clf, "digits_rf.pkl", compress=3)
print "Complete", (time.time() - start), "sec"
