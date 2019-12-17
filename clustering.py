# -*- coding: utf-8 -*-
"""
ANNEX 3:

Clustering
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.cluster.vq import kmeans2

#%% Fonctions

def datetimify(x):
    return datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S")
    
def getTimestamps(delta_minutes):
    
    start = datetimify("2016-04-25 04:01:00")
    end = datetimify("2016-04-29 04:01:00")
    delta = datetime.timedelta(minutes=delta_minutes)
    K = int((end - start)/delta) + 1
    timestamps = [start + k*delta for k in range(K)]
    
    return timestamps

def plotDendrogram(Y, title):

    plt.figure(figsize=(10, 7))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    dendrogram(
        Y,
        truncate_mode='lastp',
        p=25,
        leaf_rotation=90.,
        leaf_font_size=12.,
        show_contracted=True,
    )
    plt.savefig("{}.png".format(title))
    plt.show()

def plotprofile(timestamps, profile, title):
    
    plt.figure(figsize=(15,10))
    plt.plot(timestamps, profile, color='red')
    plt.ylabel('Occupance rate')
    plt.xlabel('Time')
    plt.savefig("profile_{}.png".format(title))  
    plt.show()

def plotAll(timestamps, avg_profiles):
    
    plt.figure(figsize=(15,10))
    plt.plot(timestamps, avg_profiles[0], color='red', label="Cluster 1")
    plt.plot(timestamps, avg_profiles[1], color='blue', label="Cluster 2")
    plt.plot(timestamps, avg_profiles[2], color='purple', label="Cluster 3")
    plt.plot(timestamps, avg_profiles[3], color='green', label="Cluster 4")
    plt.ylabel('Occupance rate')
    plt.xlabel('Time')
    plt.legend()
    plt.savefig("profile_all_1.png")  
    plt.show()
    
#%% Data

X = pd.read_csv('profiles_52.csv', sep=';', header=None)
Xoriginal = X.copy()
X = X.drop(0,1)

#D = pd.read_csv('datapoints1.csv', sep=';', header=None)
#%% Code

##Standardization
#for c in X.columns:
#    X[c] = X[c]/np.var(X[c])

Y = linkage(X, 'ward')
Z = fcluster(Y, 4, criterion='maxclust')

plotDendrogram(Y, "clusters2")

labels = []
for z in Z:
    if z not in labels:
        labels.append(z)
labels.sort()

timestamps = getTimestamps(5)
avg_values = []
avg_profiles = []
clusters = []
stations = []

for i in range(len(Xoriginal.index)):
    clusters.append(Z[i])
    stations.append(int(Xoriginal.iloc[i,0]))
        
for z in labels:
    values = np.zeros(3)
    profile = np.zeros(len(X.columns)-3)
    k = 0
    for i in range(len(Xoriginal.index)):
        if(Z[i] == z):
            values += Xoriginal.iloc[i,1:4]
            profile += Xoriginal.iloc[i,4:]
            k += 1
    values = values/k
    profile = profile/k
    avg_values.append(values)
    avg_profiles.append(profile)
    plotprofile(timestamps, profile, "cluster{}_1".format(z))
    print("Cluster {}:".format(z))
    print(k)
    print(values)
    
W = pd.DataFrame({'A':stations, 'B':clusters})
W.to_csv('stations_clusters.csv', header=None, index=None, sep=';')
    
plotAll(timestamps,avg_profiles)
