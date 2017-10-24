import pandas as pd
import os
import time
from datetime import datetime

#path to the files
path = "X:/Backups/intraQuarter"

#gather is what data what we want to get from the page 
def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path+'/_KeyStats'
    #stock_list is a quick one-liner for loop that uses os.walk to list out all contents within a directory.
    stock_list = [x[0] for x in os.walk(statspath)]
    #print(stock_list)
    # cycling through every directory (which is every stock ticker). Then, we list "each_file" which is each file within that stock's directory.
    for each_dir in stock_list[1:]:
        #taking all the files in each directory and saving them
        each_file = os.listdir(each_dir)
        #print(each_file)
        if len(each_file) > 0:
            for file in each_file:
                #explain to date-time what the format for our date stamp is, then we convert to a unix time stamp
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                print(date_stamp, unix_time)
                #time.sleep(15)

Key_Stats()
