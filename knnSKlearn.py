import numpy as np
from sklearn import preprocessing, cross_validation, neighbors
import pandas as pd

df = pd.read_csv('breast-cancer-wisconsin.data.txt')
df.replace('?',-99999, inplace=True)
df.drop(['id'], 1, inplace=True)

#dropping the first or the id col since we dont need that
X = np.array(df.drop(['class'], 1))
#the class is our labels 
y = np.array(df['class'])

#creating the training and testing smaples (about 20% of all the data)
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

#defining the classifier
clf = neighbors.KNeighborsClassifier()
#training the classifier 
clf.fit(X_train, y_train)

#testing
accuracy = clf.score(X_test, y_test)
print(accuracy)

#testing on sample data that not in dataset
example_measures = np.array([[4,2,1,1,1,2,3,2,1],[4,2,1,1,1,2,3,2,1]])
#reshaping to the amount of exaples we gave it thats the len ex and -1 meaning all the data 
example_measures = example_measures.reshape(len(example_measures), -1)
prediction = clf.predict(example_measures)
#the printed prediction is a label of either 2 or 4 (2 for benign, 4 for malignant)
print(prediction)
