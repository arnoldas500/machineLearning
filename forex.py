import time
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np

def graphRawFx():
    date,bid,ask = np.loadtxt('GBPUSD1d.txt', 
                                unpack=True, 
                                delimiter=',', 
                                converters={0:mdates.bytespdate2num('%Y%m%d%H%M%S')})
    # numpy passes a byte string to the converter instead of a string. In python 2, since bytes and str are equivalent it does not matter. For python 3, however, this results in an error as strpdate2num passes it to the standard library's strptime which only expects a string.
    fig = plt.figure(figsize=(10,7))
    ax1= plt.subplot2grid((40,40), (0,0), rowspan=40, colspan=40)
    ax1.plot(date,bid)
    ax1.plot(date,ask)
    
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M:%S'))
    
    plt.grid(True)
    plt.show()

graphRawFx()
