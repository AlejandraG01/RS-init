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
                   'C': np.random.randn(12)})

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
all_i = list(df['B'].unique())
print all_i

##user data
u_data = df[df['A'] == u_id]
print "user data: {}".format(u_data)

#user - items data array
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

cooccurence_matrix = np.matrix(np.zeros(shape=(len(items_of_user), len(all_i))), float)



for y in range(0,len(all_i)):
    total_item_data = df[df['B'] == all_i[y]]    
    y_users_item = set(total_item_data['A'].unique())
    print "item {}: total users like: {} \n" .format(all_i[y], y_users_item)
    
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















