import json
from urllib.parse import quote
import requests
import sys
import urllib
import numpy as np
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

'''authentication tokens
client_id will not be used because the api_key is all that is needed'''

client_id = 'CJe1ElpWNZ6xzAZrupPeYA'
api_key = '_tIb7QGQ6yOX2NZLnZAOvoZcLuLZhBmwPQmUfoZPUYEhU9512F4ehhgBw-vG1PZkkGcn8AGCE1q8z38dieaHoUddg1sh4cWCGm1TbQSPt4A4DwyIwNWRDn7D6QDGXHYx'
host_url = 'https://api.yelp.com'
BUSINESS_SEARCH = '/v3/businesses/search'

'''connects to Yelp's Fusion API and sends HTTP request'''

def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host_url, quote(path.encode('utf8')))
    headers = {'Authorization': 'Bearer %s' % api_key}
    resp = requests.request('GET', url, headers=headers, params=url_params)
    return resp.json()

'''returns json data about an entered term and location
i.e. ('noodles', 'San Francisco')'''

def location_query(api_key, term, location, offset_num):
    url_params = {'term': term, 'location': location, 'limit': 20, 'offset': offset_num}
    for i in range(3):
        location_data = request(host_url, BUSINESS_SEARCH, api_key, url_params=url_params)
        offset_num += 20
    return location_data

ann_arbor_data = location_query(api_key, 'Food', 'Ann Arbor', 20)

'''passes in json data about restaurants in Ann Arbor and
returns a tuple of sorted information about restaurants from the
first 20 results'''

def sort_restaurant_data(ann_arbor_data):
    review_dict = {}
    rating_list = []
    
    for item in ann_arbor_data['businesses']:
        restaurant = item['name']
        review_dict[restaurant] = item['review_count']
        rating_list.append(item['rating'])
            
    sorted_restaurants = sorted(review_dict, key = lambda x: review_dict[x], reverse = True)
    sorted_counts = sorted(review_dict.values(), reverse = True)
    sorted_prices = sorted(rating_list, reverse = True)
    
    return (sorted_restaurants, sorted_counts, sorted_prices)

'''write to DB'''

data = sort_restaurant_data(ann_arbor_data)


conn = sqlite3.connect('HelloFriends.sqlite')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS Restaurants")
cur.execute('CREATE TABLE Restaurants (name TEXT, reviews INTEGER, rating NUMERIC)')
    
for name in data[0]:
    cur.execute('INSERT INTO Restaurants (name) VALUES (?)', ([name]))
for review_count in data[1]:
    cur.execute('INSERT INTO Restaurants (reviews) VALUES (?)', ([review_count]))
for rating in data[2]:
    cur.execute('INSERT INTO Restaurants (rating) VALUES (?)', ([rating]))

conn.commit()
cur.close()

'''create plot of most 5 most reviewed restaurants in Ann Arbor for
first 3 pages of results, pulling data from DB'''

restaurants = ("Zingerman's Delicatessen", "Frita Batidos", "Sava's", "Tomukun Noodles", "The Lunch Room")
review_counts = [1946, 1643, 991, 649, 427]
index = np.arange(len(restaurants))

plt.bar(index, review_counts, align='center', alpha=0.5, color="yellow")
plt.xticks(index, restaurants)
plt.ylabel('Review Count')
plt.title('Most Reviewed Restaurants in Ann Arbor')

plt.show()

'''write data to JSON file'''

with open('restarant_data.json','w') as outfile:
    json.dump(ann_arbor_data, outfile)