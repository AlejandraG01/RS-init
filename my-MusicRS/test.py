#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 14:34:34 2018

@author: aleja
"""

import pandas as pd
import numpy as np

df = pd.DataFrame({'A': ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'c', 'c', 'c', 'c'],
                   'B': [1, 2, 3, 4, 6, 2, 3, 5, 5, 3, 1, 4],
                   'C': [0.5, 0.2, 0.1, 0.2, 0.5, 0.5, 0.0, 0.3, 0.2, 0.0, 0.0, 0.1 ]})

#all users
u = df['A'].unique()
print u

#all items
i = df['B'].unique()
print i

#id user
u_id = u[1]
print u_id

#array all items
#lista do total de items
all_i = list(df['B'].unique())
print all_i

##user data
#save all informations of user u_id
u_data = df[df['A'] == u_id]
print "user data: {}".format(u_data)

#user - items data array
#create a list of items that user likes
items_of_user = list(u_data['B'].unique())
print "user-item data: {}" .format(items_of_user)

user_item_users = []

for x in range(0, len(items_of_user)):
    #selec all data associate to item[i]
    item_data = df[df['B'] == items_of_user[x]]
    print "data of item {}: {}" .format(items_of_user[x],item_data)
    #selec all users that listened item[i]
    users_of_item = set(item_data['A'].unique())
    print "users of item {}: {}" .format(items_of_user[x], users_of_item)
    user_item_users.append(users_of_item)
    
print "user item users: {} \n" .format(user_item_users)

##coocurencia dos dados
cooccurence_matrix = np.matrix(np.zeros(shape=(len(items_of_user), len(all_i))), float)

#arrai que contem todos os usuarios q escutaram um determinado item
total_item_users = []

for y in range(0,len(all_i)):
    total_item_data = df[df['B'] == all_i[y]]   
    #exporta o conjunto de usuarios que gostam do item na posição y do array all_i
    y_users_item = set(total_item_data['A'].unique())
    print "item {}: total users like: {} \n" .format(all_i[y], y_users_item)
    
    total_item_users.append(y_users_item)
    for j in range(0,len(items_of_user)):
        j_users_items = user_item_users[j]
        print "**item_user {}:  users which like the item of user {}: {} \n" .format(items_of_user[j],u_id, j_users_items)
        
        users_intersection =  y_users_item.intersection(j_users_items)
        print "**len(intersation): {}" .format(float(len(users_intersection)))
        print "**intersection of users {} \n" .format(users_intersection)
        
        if len(users_intersection) != 0:
            users_union = y_users_item.union(j_users_items)
            print "**users union:{}" .format(users_union)
            print "**len(union): {} \n" .format(float(len(users_union)))
            cooccurence_matrix[j,y] = float(len(users_intersection))/float(len(users_union))
        else:
            cooccurence_matrix[j,y] = 0
                    
print "co-ocurrencia: {} \n" .format(cooccurence_matrix)


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
                
k= 1 
P = user_item_users
Q = total_item_users 
R = np.array(cooccurence_matrix)
nP, nQ  = matrix_factorization(R, P, Q, k)
nR = np.dot(nP, nQ.T)

print "RESULTADO MATRIX FACTORIZATION: {}" .format(nR)



print "suma: {}" .format(cooccurence_matrix.sum(axis=0))

print "shape:{}" .format(cooccurence_matrix.shape[0])

sim_scores_user = cooccurence_matrix.sum(axis=0)/float(cooccurence_matrix.shape[0])
print "sim_scores_user1:{} \n" .format(sim_scores_user)

sim_scores_user = np.array(sim_scores_user)[0].tolist()
print "sim_scores_user:{} \n" .format(sim_scores_user)

#ordena os resultados de maior a menor
sort_index = sorted(((e,i) for i,e in enumerate(list(sim_scores_user))), reverse=True)

print sort_index

#Create a dataframe from the following
columns = ['user_id', 'song', 'score', 'rank']
dataset = pd.DataFrame(columns = columns)

#Fill the dataframe with top 10 item based recommendations
rank = 1

for i in range(0,len(sort_index)):
    #all_i[sort_index[0][1]] = all_i[2] = 3
    if ~np.isnan(sort_index[i][0]) and all_i[sort_index[i][1]] not in items_of_user and rank <= 5:
        dataset.loc[len(dataset)]=[u_id,all_i[sort_index[i][1]],sort_index[i][0],rank]
        rank = rank+1
        
if dataset.shape[0] == 0:
    print("The current user has no songs for training the item similarity based recommendation model.")
    print  -1
else:
    print dataset















