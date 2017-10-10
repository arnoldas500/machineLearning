import time
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
import math

date,bid,ask = np.loadtxt('GBPUSD1d.txt', 
                                unpack=True, 
                                delimiter=',', 
                                converters={0:mdates.bytespdate2num('%Y%m%d%H%M%S')})
    # numpy passes a byte string to the converter instead of a string. In python 2, since bytes and str are equivalent it does not matter. For python 3, however, this results in an error as strpdate2num passes it to the standard library's strptime which only expects a string. (can use slashes too if we have slashes ex 2017/10/30)

patternArr= []
performanceArr = []
    
def percentChange(startPoint,currentPoint):
    try:
        x = ((float(currentPoint)-startPoint)/abs(startPoint))*100.00
        if x == 0.0:
            return 0.000000001
        else:
            return x
    except:
        return 0.0001

def patternStorage():
    '''
    The goal of patternFinder is to begin collection of %change patterns
    in the tick data. From there, we also collect the short-term outcome
    of this pattern. Later on, the length of the pattern, how far out we
    look to compare to, and the length of the compared range be changed,
    and even THAT can be machine learned to find the best of all 3 by
    comparing success rates.
    '''
    patStartTime = time.time()
    
    #Simple Average
    avgLine = ((bid+ask)/2)
    
    #This finds the length of the total array for us should use between 20 and 30
    x = len(avgLine)-30 
    #This will be our starting point, allowing us to compare to the
    #past 10 % changes. 
    y = 11
    # where we are in a trade. #
    # can be none, buy,
    currentStance = 'none'
    while y < x:
        pattern = []
        #avgLine[y-10] is our starting point
        #avgLine[y-9] is where we are currently
        p1 = percentChange(avgLine[y-10], avgLine[y-9])
        p2 = percentChange(avgLine[y-10], avgLine[y-8])
        p3 = percentChange(avgLine[y-10], avgLine[y-7])
        p4 = percentChange(avgLine[y-10], avgLine[y-6])
        p5 = percentChange(avgLine[y-10], avgLine[y-5])
        p6 = percentChange(avgLine[y-10], avgLine[y-4])
        p7 = percentChange(avgLine[y-10], avgLine[y-3])
        p8 = percentChange(avgLine[y-10], avgLine[y-2])
        p9 = percentChange(avgLine[y-10], avgLine[y-1])
        p10= percentChange(avgLine[y-10], avgLine[y])

        outcomeRange = avgLine[y+20:y+30] #array of 10 points
        currPoint = avgLine[y]

        #function to account for the average of the items in the array
        #lambda used to find a quick way to avg (adds everything together and divs by lenght of outcome range
        try:
            avgOutCome = reduce= lambda x, y: x + y, outcomeRange/ len(outcomeRange)
        except Exception as e:
            print(str(e))
            avgOutCome = 0

        #print (reduce)

        futureOutCome = percentChange(currPoint, avgOutCome)
        #pattern.append(p1) is an array of % changes
        pattern.append(p1)
        pattern.append(p2)
        pattern.append(p3)
        pattern.append(p4)
        pattern.append(p5)
        pattern.append(p6)
        pattern.append(p7)
        pattern.append(p8)
        pattern.append(p9)
        pattern.append(p10)
        
        patternArr.append(pattern)
        performanceArr.append(futureOutCome)
        
        #print (currPoint)
        #print ('--------------------------')
        #print (p1, p2, p3, p4, p5, p6, p7, p8, p9, p10)
        #time.sleep(55)
        
        y+=1

    patEndTime = time.time()
    print(len(patternArr))
    print(len(performanceArr))
    print('Pattern storage took: ',patEndTime-patStartTime,' seconds')

def graphRawFx():
    
    fig = plt.figure(figsize=(10,7))
    ax1= plt.subplot2grid((40,40), (0,0), rowspan=40, colspan=40)
    ax1.plot(date,bid)
    ax1.plot(date,ask)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M:%S'))
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    plt.subplots_adjust(bottom=.23)#making more room in the bottom so you can see full dates

    ax1_2 = ax1.twinx()
    ax1_2.fill_between(date, 0, (ask-bid), facecolor='g', alpha=.3) #ask- bid is the spread
    
    plt.grid(True)
    plt.show()

patternStorage()
graphRawFx()
