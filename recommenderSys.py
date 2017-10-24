#recommender systems give you recommendations using previous things you liked or prev things your friends have liked
import numpy as np
from lightfm.datasets import fetch_movielens
from lightfm import LightFM

#importing huge movie data set with movie ratings
#fetch data and format it and only get movies with 4.0 or higher rating
data = fetch_movielens(min_rating=4.0)

#print trainig and testing data 
print(repr(data['train']))
print(repr(data['test']))

#create model with loss function
#measures the diff between our prediction and actual pred
model = LightFM(loss='wrap') #uses gradient descent

model.fit(data['train'], epochs=30, num_threads=2)

def sampleRecommendation(model, data, userIds):
    #number of users and movies in training data
    nUsers, nItems = data['train'].shape

    #generate rec for each user we input
    for userId in userIds:
        #movies they already like 
        knownPos = data['item_labels'][data['train'].tocsr()[userId].indices]

        #movies our model predicts they will like
        scores = model.predict(userId, np.arange(nItems))
        #rank them in order of most liked to least using argsort
        top = data['item_labels'][np.argsort(-scores)]

        #printing out the results
        print("user %s" %userId)
        print("        known pos: ")
        
        for x in knownPos[:3]:
            print("     %s" %x)

        print("     Recommended: ")

        for x in top[:3]:
            print("    %" % x)

sampleRecommendation(model, data, [3, 25, 450])#passing 3 random user ids 
