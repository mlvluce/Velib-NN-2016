# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:56:13 2016

@author: Malivaï
"""

import simplekml
import pandas as pd

X = pd.read_csv('stations.csv', sep=';', header=None, encoding = 'latin1')
Y = pd.read_csv('stations_clusters.csv', sep=';', header=None)

color = {}
color[1] = 'http://www.google.com/intl/en_us/mapfiles/ms/icons/red-dot.png'
color[2] = 'http://www.google.com/intl/en_us/mapfiles/ms/icons/blue-dot.png'
color[3] = 'http://www.google.com/intl/en_us/mapfiles/ms/icons/yellow-dot.png'
color[4] = 'http://www.google.com/intl/en_us/mapfiles/ms/icons/green-dot.png'

kml = simplekml.Kml()

for i in range(len(X.index)):
    
    nb = X.iloc[i,0]
    coord = eval(X.iloc[i,2])
    cluster = Y.iloc[i,1]    
    
    pnt = kml.newpoint(name=str(nb), coords=[(coord['lng'],coord['lat'])])
    pnt.style.iconstyle.icon.href = color[cluster]

kml.save("clusters_map.kml")