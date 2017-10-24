import matplotlib.pyplot as plt
#sample dataset
from sklearn import datasets
from sklearn import svm

#going to categorize digits (0 to 9)
digits = datasets.load_digits()

# the datas features and labels
print(digits.data)

#pritning the features
print(digits.target)

clf = svm.SVC(gamma=0.001, C=100)

#seperating data into features and labels
#This loads in all but the last 10 data points, so we can use all of these for training.
X, y = digits.data[:-10], digits.target[:-10]

#training the X and y
clf.fit(X,y)

#now going to test it on a value (5th from the last) to see how it does 
print('Prediction:',clf.predict(digits.data[-5]))

plt.imshow(digits.images[-5], cmap=plt.cm.gray_r, interpolation='nearest')
plt.show()
