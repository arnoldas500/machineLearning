import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import numpy as np

#simple cluster 
X = np.array([[1, 2],
              [1.5, 1.8],
              [5, 8 ],
              [8, 8],
              [1, 0.6],
              [9,11],
              [8,2],
              [10,2],
              [9,3],])

##plt.scatter(X[:,0], X[:,1], s=150)
##plt.show()

colors = 10*["g","r","c","b","k"]

#mean shift method:
'''
Make all datapoints centroids
Take mean of all featuresets within centroid's radius, setting this mean as new centroid.
Repeat step #2 until convergence.
'''
class Mean_Shift:
    def __init__(self, radius=4):
        self.radius = radius

    def fit(self, data):
        centroids = {}

        for i in range(len(data)):
            centroids[i] = data[i]
        
        while True:
            new_centroids = []
            #loop for known centroids
            for i in centroids:
                in_bandwidth = []
                #value of centroid
                centroid = centroids[i]
                #is it within our radius
                for featureset in data:
                    if np.linalg.norm(featureset-centroid) < self.radius:
                        in_bandwidth.append(featureset)

                #recalcute a mean vecture to be the new centroid to update it
                new_centroid = np.average(in_bandwidth,axis=0)
                new_centroids.append(tuple(new_centroid)) #converting an array to a tuple

            #getting unique elements from the centroids lists (getting set of uniq centroids to get convergence)
            uniques = sorted(list(set(new_centroids)))

            #just copying centroid dictionary without the attributes
            prev_centroids = dict(centroids)

            centroids = {}
            for i in range(len(uniques)):
                centroids[i] = np.array(uniques[i]) #converting back to an array 

            optimized = True

            for i in centroids:
                #compare the 2 arrays to see if they are equal
                if not np.array_equal(centroids[i], prev_centroids[i]):
                    optimized = False
                if not optimized:
                    break
                
            if optimized:
                break

        #reset the centroids
        self.centroids = centroids



clf = Mean_Shift()
clf.fit(X)

centroids = clf.centroids
#scatters the data
plt.scatter(X[:,0], X[:,1], s=150)
#scatters the centroids 
for c in centroids:
    plt.scatter(centroids[c][0], centroids[c][1], color='k', marker='*', s=150)

plt.show()
