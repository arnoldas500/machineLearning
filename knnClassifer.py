import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import style
import warnings
from math import sqrt
from collections import Counter
#style.use('fivethirtyeight')
import pandas as pd
import random

def k_nearest_neighbors(data, predict, k=3):
    if len(data) >= k:
        warnings.warn('K is set to a value less than total voting groups!')
        
    distances = []
    for group in data:
        for features in data[group]:
            euclidean_distance = np.linalg.norm(np.array(features)-np.array(predict))
            distances.append([euclidean_distance,group])
            #distances list  is a list that contains lists of distance and class. 
    
    votes = [i[1] for i in sorted(distances)[:k]]
    print("label and num votes : " ,Counter(votes).most_common(1))
    #[0][0] is the location of the label 
    vote_result = Counter(votes).most_common(1)[0][0]
    print("vote result is (label) :  " ,vote_result)
    #how confident are we on the label we are giving it ([0][1] is how many votes)
    confidence = float(Counter(votes).most_common(1)[0][1] / k)
    #confidence is how many points (k) are similar to our point so if k= 6 and we have 6 similar points then confidence will be 100% but if we only have k = 6 and only 3 similar points then conf will be 50% 
    #print("confidence is :", confidence)
    return vote_result, confidence

'''
#creatig data in a dataset 
#features of class k are 1,2 then 2,3 ect (and has a total number of features = 3) 
dataset = {'k':[[1,2],[2,3],[3,1]], 'r':[[6,5],[7,7],[8,6]]}
#new feature we created
new_features = [5,7]


#loop to graph this to visualize it
[[plt.scatter(ii[0],ii[1],s=100,color=i) for ii in dataset[i]] for i in dataset]
plt.scatter(new_features[0], new_features[1], s=100)
'''
#plt.show()

#same thing above expect in 1 line loop
'''
#i coresponds to k and r in the dataset
for i in dataset:
    #ii in i corresponds to each feature in the dataset so first would be 1,2 of k
    for ii in dataset[i]:
        plt.scatter(ii[0],ii[1],s=100,color=i)
plt.show()
'''
'''
plt.scatter(new_features[0], new_features[1], s=100)

result = k_nearest_neighbors(dataset, new_features)
#print(result)
[[plt.scatter(ii[0],ii[1],s=100,color=i) for ii in dataset[i]] for i in dataset]
plt.scatter(new_features[0], new_features[1], s=100, color = result)  
#plt.show()
'''

#test on cancer data
df = pd.read_csv('breast-cancer-wisconsin.data.txt')
df.replace('?',-99999, inplace=True)
df.drop(['id'], 1, inplace=True)
#convert all the data to a float
full_data = df.astype(float).values.tolist()

random.shuffle(full_data)

test_size = 0.2
train_set = {2:[], 4:[]}
test_set = {2:[], 4:[]}
train_data = full_data[:-int(test_size*len(full_data))]#slicing full data up to about the last 20% of it (so from 0 to last 20%)
test_data = full_data[-int(test_size*len(full_data)):]#This will be that last 20% that we got rid of above that we are going to test on (from 80% to 100%)

#populate the dictionaries 
for i in train_data:
    train_set[i[-1]].append(i[:-1]) #i[-1] is the classifer of bad or not bad cancer type(the class)... i[:-1] append all the data up to the class but not including it 

for i in test_data:
    test_set[i[-1]].append(i[:-1])

correct = 0
total = 0

for group in test_set: #the groups are 2 and 4
    for data in test_set[group]:
        vote,confidence = k_nearest_neighbors(train_set,data, k=25)
        if group == vote:
            correct += 1
        else:
            print(confidence)
    total += 1
acc = float(correct/total)
#accuracy is how many total correct labels we labeled out of all of the data labels we assigned 
print("Accuracy : " , acc)
