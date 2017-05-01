# -*- coding: UTF-8 -*-
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import time
import datetime
import pandas as pd

# ======================== Web Scraping and building the Movies table ==================================================
# Testing of TMDb API --------------------------------------------------------------------------------------------------
API_key = 'd2189e753db5381d70ac0d51e45b19cc'
def getUrl(startyear, startmonth, endyear, endmonth, page):
    domain = 'http://api.themoviedb.org/3/discover/movie?language=en&page='+str(page)+'&sort_by=revenue.desc&primary_release_date.gte='
    url = domain +str(startyear) + '-'+str(startmonth)+'-02&primary_release_date.lte='+str(endyear) + '-'+str(endmonth)+'-01&api_key='+API_key
    return url

names = [] # Declaring the empty list for appending
years = []
year = 2014
month = 1
page = 1
if (month == 12):
    url = getUrl(year, month, year+1, 1, page)
else:
    url = getUrl(year, month, year, month+1, page)
data = json.loads(urllib2.urlopen(url).read())
results = data['results']
for i in results:
    names.append(i['title']) # Creating a list of dictionaries
    years.append((i['release_date']).split('-')[0])
print names
print years
# --------------------- Done with testing ------------------------------------------------------------------------------

# Get movie names from TMDb --------------------------------------------------------------------------------------------
# Rotten Tomatoes API does not support search movies by year. I tried querying all possible movie ID.
# However, it was very exhaustive requiring extremely high number of API calls well beyond API call limits.
# So, I decided to get movies names by year in TMDb API. The movies names from TMDb API would also correspond to
# the movies names in Rotten Tomatoes which would give us movie IDs and the relevant information of each movie.
API_key = 'd2189e753db5381d70ac0d51e45b19cc'
def getUrl(startyear, startmonth, endyear, endmonth, page):
    domain = 'http://api.themoviedb.org/3/discover/movie?language=en&page='+str(page)+'&sort_by=revenue.desc&primary_release_date.gte='
    url = domain +str(startyear) + '-'+str(startmonth)+'-02&primary_release_date.lte='+str(endyear) + '-'+str(endmonth)+'-01&api_key='+API_key
    return url

names = []
years = []
for year in xrange(1990, 2016):
    print year # To check if it runs through
    for month in xrange(1, 13):
        for page in xrange(1, 4):
            time.sleep(0.35) # to prevent the overflow and stopping of the execution
            if (month == 12):
                url = getUrl(year, month, year+1, 1, page)
            else:
                url = getUrl(year, month, year, month+1, page)
            data = json.loads(urllib2.urlopen(url).read())
            results = data['results']
            for i in results:
                names.append(i['title']) # Creating a list of dictionaries
                years.append((i['release_date']).split('-')[0])


# Storing the information to a csv file for future use
Movies = pd.DataFrame({'Name':names, 'Year': years}) # Dataframe that has two dictionaries
Movies = Movies.drop_duplicates()
Movies.to_csv('Movies.csv', encoding='utf-8', index=False) # Since we don't need to write row names (index = False)

print Movies.shape # Checking the size of our movie list ---------------------------------------------------------------

# Testing for one data -------------------------------------------------------------------------------------------------

# Creating the movie table with Rottentomato data using the movie names from TMDb
Movies = pd.read_csv('Movies.csv', encoding='utf-8')

# Relevant information to parse the data
api_key = 'm7jmrcna938zje4rqefde4n7'
moviesearch = 'http://api.rottentomatoes.com/api/public/v1.0/movies.json&page_limit=1?apikey='
movieinfo = 'http://api.rottentomatoes.com/api/public/v1.0/movies/'
movieinfo_key = '.json?apikey=' + api_key
query = '&page_limit=2&q='

#time.sleep(0.5)
newname = Movies['Name'][7].replace(' ', '+') # newname is the part of the URL that we need to open
newname = newname.replace('&', 'and')
url = moviesearch + api_key + query + newname #  the url for each new movie
try:
    data = json.loads(urllib2.urlopen(url).read())
except:
    pass
print data
# ------------ Done with testing ---------------------------------------------------------------------------------------

# Creating the movie table with Rottentomato data using the movie names from TMDb --------------------------------------
Movies = pd.read_csv('Movies.csv', encoding='utf-8')

# Relevant information to parse the data
api_key = 'm7jmrcna938zje4rqefde4n7'
moviesearch = 'http://api.rottentomatoes.com/api/public/v1.0/movies.json&page_limit=1?apikey='
movieinfo = 'http://api.rottentomatoes.com/api/public/v1.0/movies/'
movieinfo_key = '.json?apikey=' + api_key
query = '&page_limit=2&q='

# Declaring the empty lists for appending
movie_id =[]
imdb_id = []
name = []
cast = []
release = []
director = []
genre = []
critic_rating = []
audience_rating = []
review = []
weblink = []

# Looping through all the movies for running our logic
for i in xrange(len(Movies['Name'])):
    #time.sleep(0.5)
    if (i%500 == 0):
        print i # Checking if it is working
    newname = Movies['Name'][i].replace(' ','+') # newname is the part of the URL that we need to open
    newname = newname.replace('&', 'and')
    url = moviesearch + api_key + query + newname #  the url for each new movie
    try:
        data = json.loads(urllib2.urlopen(url).read())
    except:
        pass
    to_add = -1
    if (data['total'] >= 1):
        temp_id = 0
        if (data['movies'][0]['release_dates'] and ('theater' in data['movies'][0]['release_dates']) and
            abs(int(data['movies'][0]['release_dates']['theater'].split('-')[0]) - int(Movies['Year'][i])) < 2):
            temp_id = data['movies'][0]['id']
            to_add = 0
        elif (data['total'] > 1):
            if(data['movies'][1]['release_dates'] and ('theater' in data['movies'][1]['release_dates']) and
               abs(int(data['movies'][1]['release_dates']['theater'].split('-')[0]) - int(Movies['Year'][i])) < 2):
               temp_id = data['movies'][1]['id']
               to_add = 1
        if (to_add != -1):
            idx = temp_id
            url = movieinfo + str(idx) + movieinfo_key
            info = json.loads(urllib2.urlopen(url).read())
            #Use exception to deal with missing data.
            try:
                temp_imdb_id = info['alternate_ids']['imdb']
                temp_name = info['title']
                temp_cast = info['abridged_cast']
                temp_release = info['release_dates']['theater']
                temp_director = info['abridged_directors']
                temp_genre = info['genres']
                temp_critic = info['ratings']['critics_score']
                temp_andience = info['ratings']['audience_score']
                temp_review = info['links']['reviews']
                temp_weblink = info['links']['alternate']
                movie_id.append(temp_id)
                imdb_id.append(info['alternate_ids']['imdb'])
                name.append(info['title'])
                cast.append(info['abridged_cast'])
                release.append(info['release_dates']['theater'])
                director.append(info['abridged_directors'])
                genre.append(info['genres'])
                critic_rating.append(info['ratings']['critics_score'])
                audience_rating.append(info['ratings']['audience_score'])
                review.append(info['links']['reviews'])
                weblink.append(info['links']['alternate'])
            except:
                pass
# Dataframe with all relevant data
MovieTable = pd.DataFrame(
    {'ID': movie_id, 'imdb': imdb_id, 'Movie': name, 'Cast': cast, 'Release': release, 'Director': director,
     'Genre': genre,
     'Critic_rating': critic_rating, 'Audience_rating': audience_rating, 'Review': review,
     'weblink': weblink})

# csv and pickle file for future use
MovieTable.to_csv("MovieTable.csv", encoding = 'utf-8', index = False)
MovieTable.to_pickle('MovieTable.pkl')

# Concatenate Data from TMDb
MovieTable1 = pd.read_pickle('MovieTable1.pkl')
MovieTable2 = pd.read_pickle('MovieTable2.pkl')
MovieTable3 = pd.read_pickle('MovieTable3.pkl')
MovieTable4 = pd.read_pickle('MovieTable4.pkl')

MovieTable = pd.concat([MovieTable1, MovieTable2, MovieTable3, MovieTable4], axis=0)
MovieTable.reset_index(inplace=True, drop=True)

MovieTable = MovieTable.drop_duplicates(subset=['ID'])
MovieTable.reset_index(inplace=True, drop=True)
MovieTable.to_csv("MovieTable.csv", encoding = 'utf-8', index = False)
MovieTable.to_pickle('MovieTable.pkl')
#========================= Done with building the Movie table ==========================================================

# ======= Data Wrangling ===============================================================================================

# Create Actor Table from MovieTable and Delete movies without rating -------------------------------------------------
MovieTable = pd.read_pickle('MovieTableBoxOffice.pkl')
MovieTable = MovieTable.drop_duplicates(subset=['ID'])
MovieTable = MovieTable[MovieTable.Critic_rating != -1]
MovieTable.reset_index(inplace=True, drop=True)
MovieTable.head()
MovieTable.to_pickle('MovieTable.pkl')
MovieTable.shape

name = dict()
movie = dict()
critic_rating = dict()
audience_rating = dict()
genre = dict()
boxoffice = dict()
for i in range(len(MovieTable)):
    for actor in MovieTable['Cast'][i]:
        if actor['id'] in movie:
            movie[actor['id']].append(MovieTable['ID'][i])
            critic_rating[actor['id']].append(MovieTable.Critic_rating[i])
            audience_rating[actor['id']].append(MovieTable.Audience_rating[i])
            genre[actor['id']].append(MovieTable.Genre[i])
            boxoffice[actor['id']].append(MovieTable.BoxOffice[i])
        else:
            name[actor['id']] = actor['name']
            movie[actor['id']] = [MovieTable['ID'][i]]
            critic_rating[actor['id']] = [MovieTable.Critic_rating[i]]
            audience_rating[actor['id']] = [MovieTable.Audience_rating[i]]
            genre[actor['id']] = [MovieTable.Genre[i]]
            boxoffice[actor['id']] = [MovieTable.BoxOffice[i]]

ActorTable = pd.DataFrame([name, movie, critic_rating, audience_rating, genre, boxoffice]).transpose()
ActorTable.reset_index(inplace=True)
ActorTable.columns = ['ID', 'Name', 'Movie', 'Critic_rating', 'Audience_rating', 'Genre', 'Boxoffice']
ActorTable.head() # Printing the first five rows to verify
ActorTable.to_pickle('ActorTable.pkl')

# Create Director table from the Movie table ---------------------------------------------------------------------------
MovieTable = pd.read_pickle('MovieTable2014.pkl')
movie = dict()
critic_rating = dict()
audience_rating = dict()
genre = dict()
boxoffice = dict()
for i in xrange(len(MovieTable)):
    for director in MovieTable.Director[i]:
        name = director['name']
        if name in movie:
            movie[name].append(MovieTable.ID[i])
            critic_rating[name].append(MovieTable.Critic_rating[i])
            audience_rating[name].append(MovieTable.Audience_rating[i])
            genre[name].append(MovieTable.Genre[i])
            boxoffice[name].append(MovieTable.BoxOffice[i])
        else:
            movie[name] = [MovieTable.ID[i]]
            critic_rating[name] = [MovieTable.Critic_rating[i]]
            audience_rating[name] = [MovieTable.Audience_rating[i]]
            genre[name] = [MovieTable.Genre[i]]
            boxoffice[name] = [MovieTable.BoxOffice[i]]

DirectorTable = pd.DataFrame([movie, critic_rating, audience_rating, genre, boxoffice]).transpose()
DirectorTable.reset_index(inplace=True)
DirectorTable.columns = ['Name', 'Movie', 'Critic_rating', 'Audience_rating', 'Genre', 'Boxoffice']

DirectorTable.head() # Printing the first five rows to verify
print len(DirectorTable)
DirectorTable.to_pickle('DirectorTable.pkl')

# Get number of followers from Twitter ---------------------------------------------------------------------------------
from TwitterAPI import TwitterAPI
CONSUMER_KEY = 'L96guHuxCIRxz0quUVCNkHYL7'
CONSUMER_SECRET = 'kSHrrjByp6OyjQM0pFcYTlGE3olASilkIhkBbAuGebZPXGnBVB'
access_token = '806213791-laNuZaMYzd54k9teiqQ8uOgBlP3XO8qxUBF1ebST'
access_secret = 'rU1dp7KTreCXl02mckYVceX8iJmywcG9F95TBYOCzioYW'
api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, access_token, access_secret)

CONSUMER_KEY2 = 'ZanES4cy8hufvy2yjTLFG8tbO'
CONSUMER_SECRET2 = 'uSbXql55opsnhzGyUlRngp72ZrjjTDNrtkXRHJZ2nTmJJCQ5Mi'
access_token2 = '2268307190-H2eYVAJ3QrrMyuV9nc4ri44pCyZsol0ricXdniU'
access_secret2 = 'I7doox0PWs22EUMIqFPnk7SqMDFydethoOOR83Wif954f'
api2 = TwitterAPI(CONSUMER_KEY2, CONSUMER_SECRET2, access_token2, access_secret2)

ActorTable = pd.read_pickle('ActorTable.pkl')
MovieTable = pd.read_pickle('MovieTable.pkl')
tweets = dict()
follower = dict()
for i in xrange(len(ActorTable)):
    time.sleep(3)
    if i%60==0:
        print i
    name = ActorTable['Name'][i].encode('ascii', 'ignore')
    result = 0
    if i%2==0:
        result = api.request('users/search', {'q':name, 'page':'1', 'count':'1'}).json()
    else:
        result = api2.request('users/search', {'q':name, 'page':'1', 'count':'1'}).json()
    try:
        follower[ActorTable['ID'][i]] = result[0]['followers_count']
        tweets[ActorTable['ID'][i]] = result[0]['statuses_count']
    except:
        print name

Tweets = pd.DataFrame(tweets.items())
Tweets.columns = ['ID', 'Tweet']
Follower = pd.DataFrame(follower.items())
Follower.columns = ['ID', 'Follower']
TwitterData = pd.merge(Tweets, Follower, on='ID')

ActorTable = pd.read_pickle('ActorTable.pkl')
MovieTable = pd.read_pickle('MovieTable.pkl')
NewActorTable = pd.merge(ActorTable, TwitterData, on='ID')
NewActorTable.head()

NewActorTable.to_pickle('ActorTable_Twitter.pkl') # Storing in pickle file for future use

NewActorTable.shape
ActorTable.shape

#check if movie-actor pair number is consistent
count1 = 0
count2 = 0
ActorTable_Twitter = pd.read_pickle('ActorTable_Twitter.pkl')
for i in MovieTable.Cast:
    count1 = count1 + len(i)
    if len(i)==0:
        print 'alert!'
for i in ActorTable_Twitter.Movie:
    count2 = count2 + len(i)
print count1 == count2
print count1
print count2

DirectorTable = pd.read_pickle('DirectorTable.pkl')
#update director table
for movies in DirectorTable.Movie:
    todelete = []
    for i in range(len(movies)):
        if movies[i] not in MovieTable.ID.values:
            todelete.append(movies[i])
    for i in todelete:
        movies.remove(i)
        print i

MovieTable.to_pickle('MovieTable_Twitter.pkl')
ActorTable_Twitter.to_pickle('ActorTable_Twitter.pkl')
DirectorTable.to_pickle('DirectorTable_Twitter.pkl')

# Get Critics info from rotten tomato

MovieTable = pd.read_pickle('MovieTable_Twitter.pkl')
json.loads(urllib2.urlopen('http://api.rottentomatoes.com/api/public/v1.0/movies/12903/reviews.json?apikey=m7jmrcna938zje4rqefde4n7').read())['reviews'][0]

#get critic reviews from rotten
api_key = '?apikey=m7jmrcna938zje4rqefde4n7'

movie_id =[]
name=[]
fresh=[]
genre=[]
boxoffice=[]
publication = []


for i in xrange(len(MovieTable)):
    time.sleep(0.5)
    if (i%100 == 0):
        print i
    url = MovieTable.Review[i]+api_key
    data = json.loads(urllib2.urlopen(url).read())
    for review in data['reviews']:
        if (review['critic'] != ''):
            movie_id.append(MovieTable.ID[i])
            name.append(review['critic'])
            genre.append(MovieTable.Genre[i])
            boxoffice.append(MovieTable.BoxOffice[i])
            publication.append(review['publication'])
            if review['freshness']=='fresh':
                fresh.append(1)
            else:
                fresh.append(0)

CriticRaw = pd.DataFrame([movie_id, name, fresh, genre, boxoffice, publication]).transpose()
CriticRaw.to_pickle('CriticRaw.pkl')

# Checking if there are relevant data
CriticRaw.head()
# True or false check
movie = dict()
movie[('a', 'b')] = 1
('a', 'b') in movie

CriticRaw = pd.read_pickle('CriticRaw.pkl')
CriticRaw.columns = ['Movie', 'Critic', 'Rate', 'Genre', 'BoxOffice', 'Publication']
movie = dict()
rate = dict()
genre = dict()
boxoffice = dict()
for i in xrange(len(CriticRaw)):
    key = (CriticRaw.Critic[i], CriticRaw.Publication[i])
    if key in movie:
        movie[key].append(CriticRaw.Movie[i])
        rate[key].append(CriticRaw.Rate[i])
        genre[key].append(CriticRaw.Genre[i])
        boxoffice[key].append(CriticRaw.BoxOffice[i])
    else:
        movie[key]=[CriticRaw.Movie[i]]
        rate[key]=[CriticRaw.Rate[i]]
        genre[key]=[CriticRaw.Genre[i]]
        boxoffice[key]=[CriticRaw.BoxOffice[i]]

CriticTable = pd.DataFrame([movie, rate, genre, boxoffice]).transpose()
CriticTable.reset_index(inplace=True)
CriticTable.columns=['Critic', 'Movie', 'Rate', 'Genre', 'BoxOffice']
CriticTable.head()

CriticTable.to_pickle('CriticTable.pkl')
CriticTable = pd.read_pickle('CriticTable.pkl')
critic = []
genre = []
rate = []
for i in xrange(len(CriticTable)):
    tgenre = dict()
    critic.append(CriticTable.Critic[i])
    for j in range(len(CriticTable.Movie[i])):
        for g in CriticTable.Genre[i][j]:
            if g in tgenre:
                tgenre[g].append(CriticTable.Rate[i][j])
            else:
                tgenre[g] = [CriticTable.Rate[i][j]]
    genre.append(tgenre.keys())
    rate.append(map(lambda x: np.mean(np.asarray(x)),tgenre.values()))

CriticGenreTable = pd.DataFrame([critic, genre, rate]).transpose()
CriticGenreTable.columns=['Critic', 'Genre', 'Rate']
CriticGenreTable.head()
CriticGenreTable.to_pickle('CriticGenreTable.pkl')

print('Done with Web Scraping and building the tables')

# ============== Done with Web Scraping and building the tables ========================================================

