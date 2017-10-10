import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import style
import warnings
from math import sqrt
from collections import Counter
#style.use('fivethirtyeight')

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
    print(Counter(votes).most_common(1))
    vote_result = Counter(votes).most_common(1)[0][0]
    return vote_result

#creatig data in a dataset 
#features of class k are 1,2 then 2,3 ect (and has a total number of features = 3) 
dataset = {'k':[[1,2],[2,3],[3,1]], 'r':[[6,5],[7,7],[8,6]]}
#new feature we created
new_features = [5,7]


#loop to graph this to visualize it
[[plt.scatter(ii[0],ii[1],s=100,color=i) for ii in dataset[i]] for i in dataset]
plt.scatter(new_features[0], new_features[1], s=100)

plt.show()

#same thing above expect in 1 line loop
'''
#i coresponds to k and r in the dataset
for i in dataset:
    #ii in i corresponds to each feature in the dataset so first would be 1,2 of k
    for ii in dataset[i]:
        plt.scatter(ii[0],ii[1],s=100,color=i)
plt.show()
'''

plt.scatter(new_features[0], new_features[1], s=100)

result = k_nearest_neighbors(dataset, new_features)
print(result)
[[plt.scatter(ii[0],ii[1],s=100,color=i) for ii in dataset[i]] for i in dataset]
plt.scatter(new_features[0], new_features[1], s=100, color = result)  
plt.show()
