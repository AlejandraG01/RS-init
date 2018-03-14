#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 13:04:41 2017

@author: alejandra
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import recommender as rs

triplets_file = 'https://static.turi.com/datasets/millionsong/10000.txt'
songs_metadata_file = 'https://static.turi.com/datasets/millionsong/song_data.csv'

song_df_1= pd.read_table(triplets_file, header=None)
song_df_1.columns = ['user_id','song_id','listen_count']

song_df_2 = pd.read_csv(songs_metadata_file)
song_df = pd.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how="left")
song_df.head()
len(song_df)

#selec a subset of total dataset
song_df_subset = song_df.loc[0:10000, :]


############
song_df_subset["song"] = song_df["title"].map(str)+"-"+song_df["artist_name"].map(str)
song_df_subset.head()
song_grouped = song_df_subset.groupby(["song"]).agg({'listen_count': 'count'}).reset_index()
song_grouped.head()
grouped_sum = song_grouped['listen_count'].sum()

######### songs are grouped by % listen_count
song_grouped['percentage']  = song_grouped['listen_count'].div(grouped_sum)*100
song_grouped.sort_values(['listen_count', 'song'], ascending = [0,1])

print song_grouped

# the total users are grouped with unique() funtion
users = song_df_subset["user_id"].unique()
len(users)

songs = song_df_subset["song"].unique()
len(songs)

#We then create a song recommender by splitting our dataset into training and testing data. 
#We use the train_test_split function of scikit-learnlibrary
train_data, test_data = train_test_split(song_df_subset, test_size = 0.20, random_state=0)

#Create recommendation by popularity 
#a class popularity_recommender_py() is used such as back box 
# to make a simple recommendation by popularity model

pm = rs.popularity_recommender_py()
pm.create(train_data, 'user_id', 'song')

#test with some users
user_id = users[5]
print pm.recommend(user_id)

user_id = users[8]
print pm.recommend(user_id)

#####################ITEM PERSONALIZATION##################################3
##create recommendation with personalization
# Class for an item similarity based personalized recommender system 
#(Can be used as a black box)

item_model = rs.item_similarity_recommender_py()
item_model.create(train_data, 'user_id', 'song')
#print item_model
#test with some users
user_id = users[7]
user_items = item_model.get_user_items(user_id)

#Use the personalized model to make some song recommendations
print("------------------------------------------------------------------------------------")
print("Training data songs for the user userid: %s:" % user_id)
print("------------------------------------------------------------------------------------")

for user_item in user_items:
    print(user_item)

print("----------------------------------------------------------------------")
print("Recommendation process going on:")
print("----------------------------------------------------------------------")

#Recommend songs for the user using personalized model
print item_model.recommend(user_id)
################################################
#Use the personalized model to make recommendations for the following user id. 
#(Note the difference in recommendations from the first user id.)
##user_id = users[7]
#Fill in the code here
##user_items = item_model.get_user_items(user_id)
#
#print("------------------------------------------------------------------------------------")
#print("Training data songs for the user userid: %s:" % user_id)
#print("------------------------------------------------------------------------------------")

#for user_item in user_items:
#    print(user_item)

#print("----------------------------------------------------------------------")
#print("Recommendation process going on:")
#print("----------------------------------------------------------------------")

#Recommend songs for the user using personalized model
#item_model.recommend(user_id)

#################################################i
#Use the personalized recommender model to get similar songs for the following song.
#song = "Somebody To Love-Justin Bieber"
#item_model.get_similar_items([song])


