import argparse
import json
import pprint
import sys
import urllib
import urllib2
import time
import datetime
import pandas as pd
import seaborn as sns
from copy import deepcopy

# Read the previosuly created pickle file 
ActorTable = pd.read_pickle('ActorTable_Counted.pkl')
MovieTable = pd.read_pickle('MovieTable_Counted.pkl')

# testing
ActorTable.head()
MovieTable.head()

# Boxplots of our relevance 
plt.figure(figsize=(10, 10))
MovieTable.boxplot("BoxOffice", by = "ReleaseYear", figsize=(10, 10))
plt.xticks(rotation = 60)

plt.figure(figsize=(10, 10))
MovieTable.boxplot("Audience_rating", by = "ReleaseYear", figsize=(10, 10))
plt.xticks(rotation = 60)

plt.figure(figsize=(10, 10))
MovieTable.boxplot("Critic_rating", by = "ReleaseYear", figsize=(10, 10))
plt.xticks(rotation = 60)

MovieTable.columns

MovieExpandedTable = pd.DataFrame(columns=MovieTable.columns)
MovieExpandedTable
for i in xrange(MovieTable.shape[0]):
    for g in MovieTable["Genre"][i]:
        temp = deepcopy(MovieTable.irow(i))
        temp["Genre"] = g
        MovieExpandedTable = MovieExpandedTable.append(temp)#, ignore_index=True)

MovieExpandedTable.head()

plt.figure(figsize=(10, 10))
MovieExpandedTable.boxplot("BoxOffice", by = "Genre", figsize=(10, 10))
plt.xticks(rotation = 80)

plt.figure(figsize=(10, 10))
MovieExpandedTable.boxplot("Critic_rating", by = "Genre", figsize=(10, 10))
plt.xticks(rotation = 80)

plt.figure(figsize=(10, 10))
MovieExpandedTable.boxplot("Audience_rating", by = "Genre", figsize=(10, 10))
plt.xticks(rotation = 80)

MovieTable = pd.read_pickle('MovieTable_Counted.pkl')
GenreTable = pd.read_pickle('GenreTable.pkl')
GenreToPlot = GenreTable.sort("Count", ascending = False).Genre.values[0:7]
MovieExpandedTable = pd.DataFrame(columns=MovieTable.columns)
for i in xrange(MovieTable.shape[0]):
    for g in MovieTable["Genre"][i]:
        temp = deepcopy(MovieTable.irow(i))
        temp["Genre"] = g
        MovieExpandedTable = MovieExpandedTable.append(temp)
df = pd.DataFrame(index=range(1995, 2014), columns=GenreToPlot)
for g in GenreToPlot:
    SpecificGenreTable = MovieExpandedTable[MovieExpandedTable["Genre"] == g]
    #print SpecificGenreTable.groupby["ReleaseYear"].count()
    df[g] = SpecificGenreTable.groupby("ReleaseYear").count()["Movie"][5:24].values
plt.figure(); df.plot(figsize=(10, 10)); plt.title("Number of Movies In Different Genre Across Years")
plt.xlabel("Year"); plt.ylabel("Number of Movies")

import pandas as pd
GenreTable = pd.read_pickle('GenreTable.pkl')
GenreTable

for i in xrange(GenreTable.shape[0]):
    for j in xrange(int(log(int(GenreTable["Count"][i])))):
        print GenreTable["Genre"][i]
		
int(GenreTable["BoxOffice"][i])/3000

for i in xrange(GenreTable.shape[0]):
    for j in xrange(int(GenreTable["BoxOfficeAvg"][i])/1000000):
        print GenreTable["Genre"][i]
		
ActorTable = pd.read_pickle('ActorTable_Counted.pkl')
ActorTable.head()
ActorTable.shape[0] # Checking the shape

for i in xrange(ActorTable.shape[0]):
    for j in xrange(int(ActorTable["Boxoffice_AVG"][i])/10000000):
        print ActorTable["Name"][i]
		
for i in xrange(ActorTable.shape[0]):
    summ = sum(ActorTable["Boxoffice"][i])/500000000
    for j in xrange(int(summ * summ)):
        print ActorTable["Name"][i]

DirectorTable = pd.read_pickle('DirectorTable_Counted.pkl')

for i in xrange(DirectorTable.shape[0]):
    summ = sum(DirectorTable["Boxoffice"][i])/500000000
    for j in xrange(int(summ * summ)):
        print DirectorTable["Name"][i]

sum_list = []
for i in xrange(DirectorTable.shape[0]):
    sum_list.append(sum(DirectorTable["Boxoffice"][i]))

len(sum_list)
DirectorTable["Boxoffice_Sum"] = sum_list
DirectorTable.to_pickle('DirectorTable_Pred.pkl')
DirectorTable.head()

import matplotlib.pyplot as plt
%matplotlib inline

MovieTable = pd.read_pickle('MovieTable_Counted.pkl')
CriticTable = pd.read_pickle('CriticTable.pkl')
MovieTable.head()

# Use linear regression to explore the relationship between audience rating and critic rating
from sklearn import linear_model

ax = sns.lmplot( 'Critic_rating','Audience_rating', data=MovieTable, size=8)
plt.title('Simple Linear Regression of Audience Rating on Critic Rating')
import statsmodels.formula.api as smf
reg = smf.ols(formula="Audience_rating ~ Critic_rating", data=MovieTable).fit()
reg.summary()

# The relationship between critic rating and audience rating
MovieTable['log'] = np.log(MovieTable.BoxOffice)
sns.lmplot( 'Critic_rating','log', data=MovieTable, size=8)
plt.title('Simple Linear Regression of Box Office on Critic Rating')

MovieTable.head()

# Check the fidelity of Linear regression model 
# by plotting fitted values vs real values
reg = smf.ols(formula="Audience_rating ~ Critic_rating", data=MovieTable).fit()
plt.figure(figsize=(8, 6), dpi=300)
plt.scatter(MovieTable.Audience_rating/100, reg.predict()/100)
plt.title('Linear Regression')
plt.xlabel('real values')
plt.ylabel('fitted values')

# Put all information needed for regression into the MovieTable dataframe

MovieTable['Director_BoxOffice'] = range(len(MovieTable))
MovieTable['Director_BoxOffice_Sum'] = range(len(MovieTable))
MovieTable['Director_CR'] = range(len(MovieTable))
MovieTable['Director_AR'] = range(len(MovieTable))
MovieTable['Director_Count'] = range(len(MovieTable))
for i in range(len(MovieTable)):
    boxoffice = 0
    cr = 0
    ar = 0
    count = 0
    boxoffice_sum = 0
    for director in MovieTable.Director[i]:
        if DirectorTable[DirectorTable.Name==director['name']]['Boxoffice_AVG'].values[0]>boxoffice:
            boxoffice = DirectorTable[DirectorTable.Name==director['name']]['Boxoffice_AVG'].values[0]
        if DirectorTable[DirectorTable.Name==director['name']]['Boxoffice_Sum'].values[0]>boxoffice_sum:
            boxoffice_sum = DirectorTable[DirectorTable.Name==director['name']]['Boxoffice_Sum'].values[0]
        if DirectorTable[DirectorTable.Name==director['name']]['Critic_rating_AVG'].values[0]>cr:
            cr = DirectorTable[DirectorTable.Name==director['name']]['Critic_rating_AVG'].values[0]
        if DirectorTable[DirectorTable.Name==director['name']]['Audience_rating_AVG'].values[0]>ar:
            ar = DirectorTable[DirectorTable.Name==director['name']]['Audience_rating_AVG'].values[0]
        if DirectorTable[DirectorTable.Name==director['name']]['Count'].values[0]>count:
            count =DirectorTable[DirectorTable.Name==director['name']]['Count'].values[0]
    MovieTable.Director_BoxOffice[i] = boxoffice
    MovieTable.Director_CR[i] = cr
    MovieTable.Director_AR[i] = ar
    MovieTable.Director_Count[i] = count
    MovieTable.Director_BoxOffice_Sum[i] = boxoffice_sum

MovieTable['Actor_BoxOffice'] = range(len(MovieTable))
MovieTable['Actor_BoxOffice_Sum'] = range(len(MovieTable))
MovieTable['Actor_CR'] = range(len(MovieTable))
MovieTable['Actor_AR'] = range(len(MovieTable))
MovieTable['Actor_Count'] = range(len(MovieTable))
for i in range(len(MovieTable)):
    boxoffice = 0
    boxoffice_sum = 0
    cr = 0
    ar = 0
    count = 0
    for actor in MovieTable.Cast[i]:
        boxoffice = boxoffice + ActorTable[ActorTable.ID==actor['id']]['Boxoffice_AVG'].values[0]
        boxoffice_sum = boxoffice_sum + ActorTable[ActorTable.ID==actor['id']]['Boxoffice_Sum'].values[0]
        cr = cr + ActorTable[ActorTable.ID==actor['id']]['Critic_rating_AVG'].values[0]
        ar = ar + ActorTable[ActorTable.ID==actor['id']]['Audience_rating_AVG'].values[0]
        count = count + ActorTable[ActorTable.ID==actor['id']]['Count'].values[0]
    MovieTable.Actor_BoxOffice[i] = boxoffice
    MovieTable.Actor_BoxOffice_Sum[i] = boxoffice_sum
    MovieTable.Actor_CR[i] = cr
    MovieTable.Actor_AR[i] = ar
    MovieTable.Actor_Count[i] = count

MovieTable['Genre_BoxOffice'] = range(len(MovieTable))
for i in range(len(MovieTable)):
    boxoffice = 0
    for genre in MovieTable.Genre[i]:
        boxoffice = boxoffice + GenreTable[GenreTable.Genre==genre]['BoxOfficeAvg'].values[0]
    MovieTable.Genre_BoxOffice[i] = boxoffice/len(MovieTable.Genre[i])

MovieTable['ReleaseMonth'] = [float(i.split('-')[1]) for i in MovieTable.Release]
MovieTable.ReleaseYear = MovieTable.ReleaseYear.apply(float)
MovieTable.Label = MovieTable.Label.apply(str)
	
# Multiple Linear Regression The variables were chosen mannually by determine the decrease in adj. r-squared after dropping a variable.
reg = smf.ols(formula='log~Audience_rating+Critic_rating+Director_BoxOffice+Director_BoxOffice_Sum+Director_Count+Director_CR+Genre_BoxOffice+Actor_BoxOffice_Sum+ReleaseYear', data=MovieTable).fit()
reg.summary()

# Test the regression result with movies in 2016
TestMovieTable = pd.read_pickle('MovieTable2016.pkl')
TestMovieTable.head()

# Wrangle data to put all information into MovieTable
TestMovieTable['Director_BoxOffice'] = range(len(TestMovieTable))
TestMovieTable['Director_BoxOffice_Sum'] = range(len(TestMovieTable))
TestMovieTable['Director_CR'] = range(len(TestMovieTable))
TestMovieTable['Director_AR'] = range(len(TestMovieTable))
TestMovieTable['Director_Count'] = range(len(TestMovieTable))
for i in range(len(TestMovieTable)):
    boxoffice = 0
    cr = 0
    ar = 0
    count = 0
    boxoffice_sum = 0
    for director in TestMovieTable.Director[i]:
        if len(DirectorTable[DirectorTable.Name==director['name']])>0:
            if DirectorTable[DirectorTable.Name==director['name']]['Boxoffice_AVG'].values[0]>boxoffice:
                boxoffice = DirectorTable[DirectorTable.Name==director['name']]['Boxoffice_AVG'].values[0]
            if DirectorTable[DirectorTable.Name==director['name']]['Boxoffice_Sum'].values[0]>boxoffice_sum:
                boxoffice_sum = DirectorTable[DirectorTable.Name==director['name']]['Boxoffice_Sum'].values[0]
            if DirectorTable[DirectorTable.Name==director['name']]['Critic_rating_AVG'].values[0]>cr:
                cr = DirectorTable[DirectorTable.Name==director['name']]['Critic_rating_AVG'].values[0]
            if DirectorTable[DirectorTable.Name==director['name']]['Audience_rating_AVG'].values[0]>ar:
                ar = DirectorTable[DirectorTable.Name==director['name']]['Audience_rating_AVG'].values[0]
            if DirectorTable[DirectorTable.Name==director['name']]['Count'].values[0]>count:
                count =DirectorTable[DirectorTable.Name==director['name']]['Count'].values[0]
    TestMovieTable.Director_BoxOffice[i] = boxoffice
    TestMovieTable.Director_CR[i] = cr
    TestMovieTable.Director_AR[i] = ar
    TestMovieTable.Director_Count[i] = count
    TestMovieTable.Director_BoxOffice_Sum[i] = boxoffice_sum
	
TestMovieTable['Actor_BoxOffice'] = range(len(TestMovieTable))
TestMovieTable['Actor_BoxOffice_Sum'] = range(len(TestMovieTable))
TestMovieTable['Actor_CR'] = range(len(TestMovieTable))
TestMovieTable['Actor_AR'] = range(len(TestMovieTable))
TestMovieTable['Actor_Count'] = range(len(TestMovieTable))
for i in range(len(TestMovieTable)):
    boxoffice = 0
    boxoffice_sum = 0
    cr = 0
    ar = 0
    count = 0
    for actor in TestMovieTable.Cast[i]:
        if len(ActorTable[ActorTable.ID==actor['id']])>0:
            boxoffice = boxoffice + ActorTable[ActorTable.ID==actor['id']]['Boxoffice_AVG'].values[0]
            boxoffice_sum = boxoffice_sum + ActorTable[ActorTable.ID==actor['id']]['Boxoffice_Sum'].values[0]
            cr = cr + ActorTable[ActorTable.ID==actor['id']]['Critic_rating_AVG'].values[0]
            ar = ar + ActorTable[ActorTable.ID==actor['id']]['Audience_rating_AVG'].values[0]
            count = count + ActorTable[ActorTable.ID==actor['id']]['Count'].values[0]
    TestMovieTable.Actor_BoxOffice[i] = boxoffice
    TestMovieTable.Actor_BoxOffice_Sum[i] = boxoffice_sum
    TestMovieTable.Actor_CR[i] = cr
    TestMovieTable.Actor_AR[i] = ar
    TestMovieTable.Actor_Count[i] = count
	
TestMovieTable['Genre_BoxOffice'] = range(len(TestMovieTable))
for i in range(len(TestMovieTable)):
    boxoffice = 0
    for genre in TestMovieTable.Genre[i]:
        boxoffice = boxoffice + GenreTable[GenreTable.Genre==genre]['BoxOfficeAvg'].values[0]
    TestMovieTable.Genre_BoxOffice[i] = boxoffice/len(TestMovieTable.Genre[i])
	
TestMovieTable['ReleaseMonth'] = [float(i.split('-')[1]) for i in TestMovieTable.Release]
TestMovieTable['ReleaseYear'] = [int(i.split('-')[0]) for i in TestMovieTable.Release]

test = TestMovieTable[TestMovieTable.Director_AR>0]
test = test[test.Actor_CR>0]

from sklearn import linear_model as lm

# predict the result 
reg = lm.LinearRegression()
reg.fit(MovieTable[['Audience_rating', 'Critic_rating', 'Director_BoxOffice', 'Director_BoxOffice_Sum', 'Director_Count', 'Director_CR', 'Genre_BoxOffice', 'Actor_BoxOffice_Sum', 'ReleaseYear']], MovieTable['log'])
prediction = reg.predict(test[['Audience_rating', 'Critic_rating', 'Director_BoxOffice', 'Director_BoxOffice_Sum', 'Director_Count', 'Director_CR', 'Genre_BoxOffice', 'Actor_BoxOffice_Sum', 'ReleaseYear']])
test['PredictBoxOffice'] = np.exp(prediction)

PredictRank = test.sort(columns='PredictBoxOffice', ascending=False)
PredictRank.reset_index(inplace=True, drop = True)
RealRank = test.sort(columns='BoxOffice', ascending=False)
RealRank.reset_index(inplace=True, drop = True)

result = pd.DataFrame([PredictRank.Movie,PredictRank.PredictBoxOffice,PredictRank.Audience_rating, 
                       PredictRank.Critic_rating, RealRank.Movie, RealRank.BoxOffice, 
                       RealRank.Audience_rating, RealRank.Critic_rating]).transpose()
result

RealRank['RealRank'] = range(1, len(result)+1)
PredictRank['PredictRank'] = range(1, len(result)+1)

resultplot = pd.merge(RealRank[['Movie', 'RealRank']], PredictRank[['Movie', 'PredictRank']], on='Movie')

from pandas.tools.plotting import parallel_coordinates
resultplot = resultplot[['Movie', 'RealRank', 'PredictRank']]
plt.figure(figsize=(8,6))
ax = parallel_coordinates(resultplot, 'Movie')
plt.ylabel('Rank')
plt.title('Real and Predicted Rank for 2014 Movies')
legend = ax.legend()
legend.set_visible(False)

plt.figure(figsize=(8, 6), dpi=300)
ax = parallel_coordinates(test[['Movie', 'BoxOffice', 'PredictBoxOffice']], 'Movie')
legend = ax.legend()
plt.ylabel('Boxoffice')
plt.title('Real and Predicted Box Office for 2014 Movies')
legend.set_visible(False)

# =========== End of the data analysis, plots and prediction =========================================================




































