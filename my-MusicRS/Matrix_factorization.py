#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 12:52:14 2018

@author: aleja
ref: http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/#viewSource
"""

import numpy as np

def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    Q = Q.T
    print Q
    for step in xrange(steps):
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    #calcular erro
                    eij = R[i][j] - np.dot(P[i, : ], Q[: , j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = np.dot(P, Q)
        ##função de optimização
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                     e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                     for k in xrange(K):
                         e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        if e < 0.001:
            break
    
    return P, Q.T
                
                
           
    
R = [[5,3,0,1],
     [4,3,3,1],
     [1,1,0,5],
     [0,0,0,0],
     [4,4,5,0],]




R = np.array(R)
# len #users
N = len(R)
M = len(R[0])
K = 2

# P = #users, Q = #product
P = np.random.rand(N,K)
print ("valor inicial de P: {}" .format(P))
Q = np.random.rand(M,K)
print ("valor inicial de Q: {}" .format(Q))


nP, nQ = matrix_factorization(R, P, Q, K)
nR = np.dot(nP, nQ.T)

print ("nR: {}" .format(nR))























