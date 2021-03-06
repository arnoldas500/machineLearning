from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import random

style.use('fivethirtyeight')
#a regression line is just like a straight line (same as best fit line)

#xs = np.array([1,2,3,4,5,6], dtype=np.float64)
#ys = np.array([5,4,6,5,6,7], dtype=np.float64)

def createDataset(howMany, variance, step=2, correlation=False):
    val = 1
    ys = []
    for i in range(howMany):
        y = val + random.randrange(-variance, variance)
        ys.append(y)
        if correlation and correlation == 'pos':
            val+=step
        elif correlation and correlation == 'neg':
            val -= step
    xs = [i for i in  range(len(ys))]
    
    return np.array(xs, dtype=np.float64), np.array(ys, dtype=np.float64)

#finding m for best fit slope and y for intercept in eq y = mx + b
def bestFitSlopeIntercept(xs,ys):
    m = ( (mean(xs) * mean(ys)) - mean(xs*ys) ) / ( mean(xs)**2 - mean(xs**2) )
    b = mean(ys) - m*mean(xs)
    return m,b

def squaredErr(ysOrig, ysLine):
    return sum((ysLine - ysOrig)**2)

def coefficientOfDetermination(ysOrig, ysLine):
    yMeanLine = [mean(ysOrig) for y in ysOrig]
    squaredErrRegr = squaredErr(ysOrig, ysLine)
    squaredErrYMean = squaredErr(ysOrig, yMeanLine)
    return 1 - (squaredErrRegr / squaredErrYMean)


xs,ys = createDataset(40, 40, 2, correlation = 'pos')


m,b = bestFitSlopeIntercept(xs,ys)

print(m,b)

#do mx+b for each x in xs
regressionLine = [(m*x)+b for x in xs]

#going to predict the y value where x = 8
predictX = 8
predictY = (m*predictX)+b

rSquared = coefficientOfDetermination(ys, regressionLine)
print(rSquared)

plt.scatter(xs,ys)
plt.scatter(predictX,predictY, s=80 , color='red')
plt.plot(xs, regressionLine)
plt.show()


# using coefficient of determination or squared error to see how good our prediction is
#sqaured error is the dist between our point and our line squared
#squared since we want pos values and if point is above line then it would be a neg value
#want the r squared value to be pretty high ex 0.9

print("done")
