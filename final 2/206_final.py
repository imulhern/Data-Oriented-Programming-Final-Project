import requests
import json
import matplotlib.pyplot as plt
import sqlite3
import numpy as np

#Source: https://www.boxofficemojo.com/yearly/chart/?yr=2017&p=.htm
titles_17 = ['Star Wars: The Last Jedi', 'Beauty and the Beast', 'Wonder Woman',
'Jumanji: Welcome to the Jungle', 'Guardians of the Galaxy Vol. 2', 'Spider-Man: Homecoming',
 'It', 'Thor: Ragnarok', 'Despicable Me 3', 'Justice League', 'Logan', 'The Fate of the Furious',
  'Coco', 'Dunkirk', 'Get Out', 'The LEGO Batman Movie', 'The Boss Baby', 'The Greatest Showman',
  'Pirates of the Caribbean: Dead Men Tell No Tales', 'Kong: Skull Island', 'Cars 3',
  'War for the Planet of the Apes', 'Split', 'Wonder', 'Transformers: The Last Knight',
   'Girls Trip', 'Fifty Shades Darker', 'Baby Driver', 'Pitch Perfect 3', "Daddy's Home 2",
   'Murder on the Orient Express', 'Annabelle: Creation', 'Kingsman: The Golden Circle',
    'Blade Runner 2049', 'John Wick: Chapter Two', 'The Emoji Movie', 'Power Rangers',
     'Ferdinand', 'The Post', 'The Mummy', "The Hitman's Bodyguard", 'Alien: Covenant',
      'Captain Underpants: The First Epic Movie', 'A Bad Moms Christmas', "A Dog's Purpose",
       'The Shape of Water', 'The LEGO Ninjago Movie', 'Baywatch', 'The Shack', 'Darkest Hour']


#Source: https://www.boxofficemojo.com/yearly/chart/?p=.htm&yr=2018
titles_18 = ['Black Panther', 'Avengers: Infinity War', 'Incredibles 2', 'Jurassic World: Fallen Kingdom',
 'Aquaman', 'Deadpool 2', "Dr. Seuss' The Grinch", 'Mission: Impossible - Fallout',
  'Ant-Man and the Wasp', 'Bohemian Rhapsody', 'A Star is Born', 'Solo: A Star Wars Story',
   'Venom', 'Ralph Breaks the Internet', 'Spider-Man: Into The Spider-Verse', 'A Quiet Place',
    'Crazy Rich Asians', 'Mary Poppins Returns', 'Hotel Transylvania 3: Summer Vacation',
     'Fantastic Beasts: The Crimes of Grindelwald', 'Halloween', 'The Meg', "Ocean's 8",
      'Ready Player One', 'Bumblebee', 'Mamma Mia! Here We Go Again', 'The Nun', 'Creed II',
       'Peter Rabbit', 'The Mule', 'The Equalizer 2', 'Rampage', 'A Wrinkle in Time',
        'Fifty Shades Freed', "Disney's Christopher Robin", 'Green Book', 'I Can Only Imagine',
         'Smallfoot', 'Night School', 'The First Purge', 'Game Night', 'Book Club',
          'The House With A Clock In Its Walls', 'Skyscraper', 'Insidious: The Last Key',
           'Instant Family', 'Blockers', 'Pacific Rim Uprising', 'Tomb Raider',
           'Maze Runner: The Death Cure']

#No input to get_omdb. Makes request for each title and returns a list
#of tuples with each tuple containing data about a single movie.
def get_omdb():
    base_url = 'http://www.omdbapi.com/?i=tt3896198&apikey=f25f8d63'
    movie_genre_rt_yr = []
    for title in titles_17:
        param_d = {'type': 'movie', 't': title, 'y': '2017'}
        resp1 = requests.get(base_url, params=param_d)
        resp1_data = resp1.json()
        rating = 0
        rt_count = 0
        if 'Ratings' in resp1_data:
            for x in resp1_data['Ratings']:
                if 'Internet Movie Database' in x.values():
                    value = float(x['Value'][:x['Value'].find("/")]) * 10
                    rating += value
                    rt_count += 1
                if 'Rotten Tomatoes' in x.values():
                    value = float(x['Value'][:-1])
                    rating += value
                    rt_count += 1
                if 'Metacritic' in x.values():
                    value = float(x['Value'][:x['Value'].find("/")])
                    rating += value
                    rt_count += 1

            if rt_count != 0:
                avg_rating = round(rating/rt_count,2)
            else:
                continue
            movie_genre_rt_yr.append((resp1_data['Title'], resp1_data['Genre'], avg_rating, int(resp1_data['Year'])))

    for title_2 in titles_18:
        param_d = {'type': 'movie', 't': title_2, 'y': '2018'}
        resp2 = requests.get(base_url, params=param_d)
        resp2_data = resp2.json()
        rating = 0
        rt_count = 0
        if 'Ratings' in resp2_data:
            for x in resp2_data['Ratings']:
                if 'Internet Movie Database' in x.values():
                    value = float(x['Value'][:x['Value'].find("/")]) * 10
                    rating += value
                    rt_count += 1
                if 'Rotten Tomatoes' in x.values():
                    value = float(x['Value'][:-1])
                    rating += value
                    rt_count += 1
                if 'Metacritic' in x.values():
                    value = float(x['Value'][:x['Value'].find("/")])
                    rating += value
                    rt_count += 1
            if rt_count != 0:
                avg_rating = round(rating/rt_count,2)
            else:
                continue
            movie_genre_rt_yr.append((resp2_data['Title'], resp2_data['Genre'], avg_rating, int(resp2_data['Year'])))

    return movie_genre_rt_yr
movie_genre_rt_yr = get_omdb()

conn = sqlite3.connect('HelloFriends.sqlite')
cur = conn.cursor()
# cur.execute('DROP TABLE IF EXISTS MOVIES')
#
# cur.execute('DROP TABLE IF EXISTS NAMES')





#insert_titles takes no input and has no output. insert the movie titles into
#the NAMES table
def insert_titles():
    cur.execute("CREATE TABLE IF NOT EXISTS NAMES (id INTEGER, title TEXT)")
    n = cur.execute('SELECT * FROM NAMES').fetchall()
    if len(n) < 2:
        count = 1
        for lst in [titles_17, titles_18]:
            for x in lst:

                cur.execute('INSERT INTO NAMES (id, title) VALUES (?,?)', (count,x))
                count+=1
    return None

#insert_movie_data takes no input and has no output. It inserts an id, genre,
#rating, and year of a movie into the MOVIES table in the database.
def insert_movie_data():
    cur.execute('CREATE TABLE IF NOT EXISTS MOVIES (title_id INTEGER, genre TEXT, rating DECIMAL, year INTEGER)')
    n = cur.execute('SELECT * FROM MOVIES').fetchall()

    if len(n) < 2:
        i = 1
        for x in movie_genre_rt_yr:
            movie_tup = (i,x[1],float(x[2]),int(x[3]))
            cur.execute('INSERT INTO MOVIES (title_id, genre, rating, year) VALUES (?,?,?,?)', movie_tup)
            i+=1
    return None

insert_titles()
insert_movie_data()

conn.commit()
file_data = list(cur.execute('SELECT * FROM MOVIES'))
genre_count = {'2017': {'Comedy': 0, 'Action': 0, 'Thriller': 0, 'Horror': 0, 'Fantasy': 0,'Drama': 0,'Documentary': 0, 'Romance': 0},
 '2018': {'Comedy': 0, 'Action': 0, 'Thriller': 0, 'Horror': 0, 'Fantasy': 0,'Drama': 0,'Documentary': 0, 'Romance': 0}}
for x in file_data:
    if str(x[3]) == '2017':
        temp_genre_lst = [y.strip() for y in str(x[1]).split(",")]
        for genre in temp_genre_lst:
            if genre in genre_count['2017']:
                genre_count['2017'][genre] += 1

    elif str(x[3]) == '2018':
        temp_genre_lst = [y.strip() for y in str(x[1]).split(",")]
        for genre in temp_genre_lst:
            if genre in genre_count['2018']:
                genre_count['2018'][genre] += 1

#to_json_file takes in a json file name and writes data to said file.
#Has no output.
def to_json_file(f_name):

    out_file = open(f_name,'w')
    movie_data = json.dump(genre_count, out_file,indent=4)
    out_file.close()
    return None
conn.close()

to_json_file('movie_results.json')

N = len(list(genre_count['2017'].keys()))
values_2017 = tuple(genre_count['2017'].values())
values_2018 = tuple(genre_count['2018'].values())

ind = np.arange(N)
width = 0.35

p1 = plt.bar(ind, values_2017, width,)
p2 = plt.bar(ind, values_2018, width,
             bottom=values_2017)

plt.tight_layout(pad=1.20)
plt.ylabel('Frequency')
plt.xlabel('Genre')
plt.title('2017 & 2018 Genre Counts of Top Grossing Films')
plt.xticks(ind, ('Comedy', 'Action', 'Thriller', 'Horror', 'Fantasy', 'Drama', 'Documentary', 'Romance'), rotation='vertical')
plt.yticks(np.arange(0, 60, 5))
plt.legend((p1[0], p2[0]), ('2017', '2018'))

plt.savefig("genre_count.png")
