from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import unittest
import sqlite3
import requests
import json
import re
import sys
import os
import spotipy
import webbrowser
import spotipy.util as util 
import matplotlib
import matplotlib.pyplot as plt

#asks command line for my username 
username = sys.argv[1]
scope = 'user-top-read'
# My profile: ian.mulhern0106

#establish connection

try:
    token = util.prompt_for_user_token(username,scope,client_id='f789c75e373b47aaaae9af8917ea8201',client_secret='b7db0264c5224fa79eb09158be96e00c',redirect_uri='http://google.com/')
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username,scope,client_id='f789c75e373b47aaaae9af8917ea8201',client_secret='b7db0264c5224fa79eb09158be96e00c',redirect_uri='http://google.com/')

#Grab my information from API 

if token:
    
    SPTFY = spotipy.Spotify(auth=token)
    SPTFY.trace=False
    user = SPTFY.current_user()
    print(json.dumps(user,sort_keys=True,indent=4))
else:
    print("error")

#grab my top artists and tracks 


if token:
    SPTFY = spotipy.Spotify(auth=token)
    SPTFY.trace = False
    #access top artist info for the short, medium, and long term params spotify has built in 
    
    ranges = ['short_term','medium_term','long_term']
    short_term_list = []
    medium_term_list = []
    long_term_list = []
    lists = [short_term_list,medium_term_list,long_term_list]
    list_iterator = 0
    
    for r in ranges:
        most_played_artists = SPTFY.current_user_top_artists(limit=20,time_range=r)
        
        for artist in most_played_artists['items']:
            print(artist['name'])
            lists[list_iterator].append(artist['name'])
        print("-------------")
        list_iterator += 1 
    
    #access my top tracks
    
    short_term_dict = {}
    long_term_dict = {}
    medium_term_dict = {}
    
    dict_list = [short_term_dict,medium_term_dict,long_term_dict]
    
    dict_iterator = 0
    
    for r in ranges: 
        most_played_tracks = SPTFY.current_user_top_tracks(limit=45,time_range=r)
    
        for track in most_played_tracks['items']:
            title = track['name']
            artist = track['artists'][0]['name']
            dict_list[dict_iterator][artist]=title
        
        dict_iterator += 1
    
    # get frequency of artists that have songs that are also in my top listened 

    top_song_artists_short_term = short_term_dict.keys()
    top_song_artists_medium_term = medium_term_dict.keys()
    top_song_artists_long_term = long_term_dict.keys()
    short_term_freq = {}
    medium_term_freq = {}
    long_term_freq = {}
    
    for ar in top_song_artists_short_term:
        if ar not in short_term_freq and ar in short_term_list:
            short_term_freq[ar] = 1
        elif ar in short_term_freq and ar in short_term_list: 
            short_term_freq[ar] += 1
        
    print(short_term_freq)
    print('-------------')
    for ar in top_song_artists_medium_term:
        if ar not in medium_term_freq and ar in medium_term_list:
            medium_term_freq[ar] = 1
        elif ar in medium_term_freq and ar in medium_term_list:
            medium_term_freq[ar] += 1 
    print(medium_term_freq)
    print('------------')
    for ar in top_song_artists_long_term:
        if ar not in long_term_freq and ar in long_term_list:
            long_term_freq[ar] = 1
        elif ar in long_term_freq and ar in long_term_list:
            long_term_freq[ar] += 1
    print(long_term_freq)

else:
    print("token error")

#Write to DB 

conn = sqlite3.connect('HelloFriends.sqlite')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS spotify")
cur.execute("CREATE TABLE spotify(short_artist TEXT, short_freq INTEGER, med_artist TEXT, med_freq INTEGER, long_artist TEXT, long_freq INTEGER)")

for art in short_term_freq:
    _artist = art
    _frequency = short_term_freq[art]
    cur.execute("INSERT INTO spotify (short_artist, short_freq) VALUES (?,?)",(_artist,_frequency))
for art in medium_term_freq:
    _artist = art
    _frequency = medium_term_freq[art]
    cur.execute("INSERT INTO spotify (med_artist, med_freq) VALUES (?,?)",(_artist,_frequency))
for art in long_term_freq:
    _artist = art
    _frequency = long_term_freq[art]
    cur.execute("INSERT INTO spotify (long_artist, long_freq) VALUES (?,?)",(_artist,_frequency))
conn.commit()

#selecting the artists and their frequency of songs that are in my top listened in the different time ranges 

cur.execute("SELECT short_artist FROM spotify")
short_art = []
for row in cur:
    if row != (None,):
        short_art.append(str(row)[2:-3])
cur.execute("SELECT short_freq FROM spotify")
short_freq = []
for row in cur:
    if row != (None,):
        short_freq.append(str(row)[1:-2])
cur.execute("SELECT med_artist FROM spotify")
med_art =[]
for row in cur:
    if row != (None,):
        med_art.append(str(row)[2:-3])
cur.execute("SELECT med_freq FROM spotify")
med_freq = []
for row in cur:
    if row != (None,):
        med_freq.append(str(row)[1:-2])
cur.execute("SELECT long_artist FROM spotify")
long_art =[]
for row in cur:
    if row != (None,):
        long_art.append(str(row)[2:-3])
cur.execute("SELECT long_freq FROM spotify")
long_freq = []
for row in cur:
    if row != (None,):
        long_freq.append(str(row)[1:-2])

#plot three different pie charts showing artists that are both in my top artists and have songs that are in my top listened for that specfic period 
plt.figure(0)
plt.pie(short_freq,labels=short_art)
plt.title('Short Term Artists')
plt.figure(1)
plt.pie(med_freq,labels=med_art)
plt.title('Medium Term Artists')
plt.figure(2)
plt.pie(long_freq,labels=long_art)
plt.title("Long Term Artists")
plt.show()








