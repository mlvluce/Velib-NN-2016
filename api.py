# -*- coding: utf-8 -*-
"""
ANNEX 1:

Downloading Data from JCDecaux API with an update every minute.
"""

import os
import requests
import datetime
import time

#%% Define working environment

workdir = os.getcwd()
root = os.path.abspath(os.path.join(workdir, os.pardir))
datadir = os.path.join(root,"Data")

class CET(datetime.tzinfo):
    def utcoffset(self, dt):
      return datetime.timedelta(hours=2)

    def dst(self, dt):
        return datetime.timedelta(0)
        
contracts_query = "https://api.jcdecaux.com/vls/v1/contracts"
contracts_params = {"apiKey": "###"}

stations_query = "https://api.jcdecaux.com/vls/v1/stations"
stations_params = {
    "apiKey": "###",
    "contract": "Paris",
    }
    
head = {"Accept": "application/json"}

#%% Define functions

def createLastUpdate(): 
        
    s = open("stations.csv", 'r')
    lines = s.readlines()
    
    lastupdates = {}
    
    for line in lines:
        entry = line.rstrip('\n').split(',')
        number = int(entry[0])
        lastupdate = entry[5]
        lastupdates[number]= lastupdate
    
    return lastupdates
    
def getUpdate(f, lastupdates):
    
    now = datetime.datetime.now(CET())
    now = datetime.datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
    r = requests.get(stations_query, params = stations_params, headers=head)
    response = r.json()
    
    k = 0
    for station in response:
        nb = station["number"]
        update = station["last_update"]
        update = datetime.datetime.fromtimestamp(int(update)/1000,CET())
        update = datetime.datetime.strftime(update, "%Y-%m-%d %H:%M:%S")
        if update != lastupdates[nb]:
            k+=1
            lastupdates[nb] = update
            status = station["status"]
            stands = station["bike_stands"]
            availstands = station["available_bike_stands"]
            availbikes = station["available_bikes"]
            f.write("{},{},{},{},{},{}\n".format(nb,update,status,stands,availbikes,availstands))    
    
    print("{}: {} updates".format(now, k))
    
    return lastupdates
    
#%% Download data

f = open(os.path.join(datadir, "week1.csv"), 'w')

starttime = datetime.datetime.strptime("2016-04-25 02:00:00", "%Y-%m-%d %H:%M:%S")
starttime = starttime.replace(tzinfo=CET())
endtime = datetime.datetime.strptime("2016-04-30 06:00:00", "%Y-%m-%d %H:%M:%S")
endtime = endtime.replace(tzinfo=CET())

now = datetime.datetime.now(CET())
lastupdates = createLastUpdate()

while(now <= starttime):
    print("Waiting {}".format(starttime))
    time.sleep(60)
    now = datetime.datetime.now(CET())
    
while(now <= endtime):    
    lastupdates = getUpdate(f, lastupdates)
    time.sleep(60)
    now = datetime.datetime.now(CET())

f.close()