#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 14:34:34 2018

@author: aleja
"""

import pandas as pd
import numpy as np

df = pd.DataFrame({'A': [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
                   'B': [1, 2, 3, 4, 1, 2, 3, 5, 5, 3, 1, 4],
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
u_i_data = list(u_data['B'].unique())
print "user-item data: {}" .format(u_i_data)

user_item_users = []

for x in range(0, len(u_i_data)):
    i_data = df[df['B'] == u_i_data[x]]
    print "item data: {}" .format(i_data)
    item_users = set(i_data['A'].unique())
    print "item_users: {}" .format(item_users)
    user_item_users.append(item_users)
    
print "user item users: {}" .format(user_item_users)