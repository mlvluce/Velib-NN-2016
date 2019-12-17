# -*- coding: utf-8 -*-
"""
ANNEX 4:

Neural Network
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split


#%% Fonctions

def sigmoid(x,deriv=False):
	if(deriv==True):
	    return x*(1-x)
	return 1/(1+np.exp(-x))

def softmax(y,deriv=False):
    if(deriv):
        return softmax(y)
    return np.exp(y)/np.sum(np.exp(y),axis=1,keepdims=True)

def binarize(Y):
    
    Ytemp = Y.copy()
    Ytemp[Ytemp>0.5] = 1
    Ytemp[Ytemp<0.5] = 0
    
    return Ytemp

def binarize2(Y):
    
    Y[Y>0.5] = 1
    Y[Y<-0.5] = -1
    Y[np.all([Y>-0.5,Y<0.5])] = 0
    
    return Y

def confmatrix2(y, Y):
    
    Ytemp = binarize2(Y)
    
    nY = 3
    N = len(y.index)
    M = np.zeros((nY,nY), dtype = np.int)
    cat = [0,1,-1]
    for i in range(N):
        jy = cat.index(y.iloc[i,0])
        jY = cat.index(Ytemp[i])
        M[jy,jY] += 1
    
    error = 1.0 - np.trace(M)/np.sum(M)

    return M, error
    
def confmatrix(y, Y):
    
    nY = len(y.columns)
    N = len(y.index)
    M = np.zeros((nY,nY), dtype = np.int)
    
    if nY == 1:
        return confmatrix2(y,Y)
    
    Ytemp = binarize(Y)
    
    for i in range(N):
        jy = np.argmax(y.iloc[i,:])-6
        jY = np.argmax(Ytemp[i,:])
        M[jy,jY] += 1
    
    error = 1.0 - np.trace(M)/np.sum(M)
    conf = np.trace(M[1:,1:])/np.sum(M[1:,:])

    return M, error, conf
 

#%% Data

dftrain = pd.read_csv('datapoints4train.csv', sep=';', header=None)
dftest = pd.read_csv('datapoints4test.csv', sep=';', header=None)

x = dftrain.iloc[:,0:6]
y = dftrain.iloc[:,6:]

xtest = dftest.iloc[:,0:6]
ytest = dftest.iloc[:,6:]


#%% Code

#Number of hidden neurons
nZ = 5
#Learning rate
ro = 0.0005

N = len(x.index)
nX = len(x.columns)
nY = len(y.columns)

np.random.seed(1)

# randomly initialize our weights with mean 0

a = 2*np.random.random((nX,nZ)) - 1
a0 = np.zeros((1,nZ))
b = 2*np.random.random((nZ,nY)) - 1
b0 = np.zeros((1,nY))

for j in range(60000):

	#Feedforward
    X = x
    V = np.dot(X,a) + a0
    Z = sigmoid(V)
    Y = softmax(np.dot(Z,b) + b0)

    #Backpropagation
    d2 = Y - y
    d1 = sigmoid(Z, deriv=True)*(np.dot(d2,b.T))
    
#    ro = ros[int(j/20000)]
    
    b += -ro*np.dot(Z.T,d2)
    b0 += -ro*np.sum(d2, axis=0)
    a += -ro*np.dot(X.T, d1)
    a0 += -ro*np.sum(d1, axis=0)

    if(j%10000)==9999:
        M, e, c = confmatrix(y,Y)
        print(M)
        print(e,c)
        print("")

X = xtest
V = np.dot(X,a) + a0
Z = sigmoid(V)
Ytest = softmax(np.dot(Z,b) + b0)

M, e, c = confmatrix(ytest,Ytest)
print(M)
print(e, c)