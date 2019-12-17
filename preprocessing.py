# -*- coding: utf-8 -*-
"""
ANNEX 2:

Data preprocessing
"""

import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt

#%% Fonctions

def datetimify(x):
    return datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")

def stringify(x):
    datetime.datetime.strftime()
    return x.strftime("%Y-%m-%d %H:%M:%S")

def getProfile(Station, X, delta_minutes, output=False):
    
    nb = Station[1]
    banking = Station[4]
    bonus = Station[5]
    if banking == True:
        banking = 1
    else:
        banking = 0
    if bonus == True:
        bonus = 1
    else:
        bonus = 0
    selected = X['Station'] == nb
    
    Temp = X[selected]
    start = datetimify("2016-04-25 04:01:00")
    end = datetimify("2016-04-29 04:01:00")
    delta = datetime.timedelta(minutes=delta_minutes)
    K = int((end - start)/delta) + 1
    timestamps = [start + k*delta for k in range(K)]
    profile = []

    N = len(Temp.index)
    index = iter(range(N))
    i = next(index, N)
    stands = Temp.iloc[i,3]
    date = datetimify(Temp.iloc[i,1])
    bikes = Temp.iloc[i,4]
    
    for ts in timestamps:
        while (i < N and date < ts):
            i = next(index, N)
            if i < N:               
                date = datetimify(Temp.iloc[i,1])
        bikes = Temp.iloc[max(0,i-1),4]
        profile.append(str(100.0*bikes/stands))
    
    if output:
        f = open('profiles_52.csv','a')
        f.write("{};{};{};{};{}\n".format(nb,stands, banking, bonus,';'.join(profile)))
        f.close()
  
    return timestamps, profile
    
def plotprofile(timestamps, profile, title):
    
    plt.figure(figsize=(15,10))
    plt.plot(timestamps, profile, color='red')
    plt.ylabel('Occupance rate')
    plt.xlabel('Time')
    plt.savefig("profile_{}.png".format(title))  
    plt.show()

def getClosedStations(X, Y):
    
    closed = []
    for station in Y.itertuples():
        nb = station[1]
        selected = X1['Station'] == nb    
        Temp = X1[selected]
    
        if 'OPEN' not in list(Temp['Status']):
            print(nb)
            closed.append(nb)
            
    return closed

def createDataPoints(nb, timestamps, profile, delta_minutes):
    
    step = int(60/delta_minutes)
    K = len(profile)
    
    f = open('datapoints1.csv', 'a')
    
    for k in range(0,K,step):
        nexthour = [float(x) for x in profile[k:k+step]]
        time = timestamps[k].hour
        current = profile[k]
        if(100.0 in nexthour):
            test = 1
        elif(0.0 in nexthour):
            test = -1
        else:
            test = 0
        
        f.write("{};{};{};{}\n".format(nb,time,current,test))
    
    f.close()

#%% Loading Data
X1 = pd.read_csv('week1.csv', sep=',',header=None)
Y = pd.read_csv('stations.csv', sep=';',header=None, encoding = 'latin1')
X1.columns = ['Station', 'Date', 'Status', 'Stands', 'Bikes', 'Spots']
Y.columns = ['ID','Name','Position','Banking','Bonus','Lastupdate']

#%% Code

closed = getClosedStations(X1, Y)
print(closed)

f = open('datapoints1.csv','w')
f.close()

for Station in Y.itertuples():
    nb = Station[1]
    print(nb)       
    timestamps, profile = getProfile(Station, X1, 5)
    createDataPoints(nb, timestamps, profile,5)