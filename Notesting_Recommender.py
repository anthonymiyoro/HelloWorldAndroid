import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
# from nltk.stem.wordnet import WordNetLemmatizer
# from nltk.corpus import wordnet

import warnings; warnings.simplefilter('ignore')


metadata = pd.read_csv('/Users/anthonymiyoro/Documents/code/MoviePredictor/data/movies_metadata.csv', low_memory=False)
links_small = pd.read_csv('/Users/anthonymiyoro/Documents/code/MoviePredictor/data/links_small.csv')
links_small = links_small[links_small['tmdbId'].notnull()]['tmdbId'].astype('int')
metadata = metadata.drop([19730, 29503, 35587])

metadata['id'] = metadata['id'].astype('int')

# Collect all the metadata for movies in the links_small dataset
smd = metadata[metadata['id'].isin(links_small)]

# Fill empty spaces and create new description column
smd['tagline'] = smd['tagline'].fillna('')
smd['description'] = smd['overview'] + smd['tagline']
smd['description'] = smd['description'].fillna('')

# Convert descriptions into a corpus then weigh the individual words using tfidf
# https://www.quora.com/How-does-TfidfVectorizer-work-in-laymans-terms

tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(smd['description'])

# Cosine Similarity

# I will be using the Cosine Similarity to calculate a numeric quantity that denotes the similarity between two movies. 
# Mathematically, it is defined as follows:
 
# Since we have used the TF-IDF Vectorizer, calculating the Dot Product will directly give us the Cosine Similarity Score. 
# Therefore, we will use sklearn's linear_kernel instead of cosine_similarities since it is much faster.

# Calculate the cosine similarity of each movies description to another in the dataset
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Create a new series based on movie titles using the similarity matrix
smd = smd.reset_index()
titles = smd['title']
indices = pd.Series(smd.index, index=smd['title'])

print ("1/4")

## NEW METHOD

# Import new data then change the ids to integers
credits = pd.read_csv('/Users/anthonymiyoro/Documents/code/MoviePredictor/data/credits.csv')
keywords = pd.read_csv('/Users/anthonymiyoro/Documents/code/MoviePredictor/data/keywords.csv')

# Change all ids to integers
keywords['id'] = keywords['id'].astype('int')
credits['id'] = credits['id'].astype('int')
metadata['id'] = metadata['id'].astype('int')

# Merge cast, crew, genres and credits into one dataframe
metadata = metadata.merge(credits, on='id')
metadata = metadata.merge(keywords, on='id')

# Merge credits and keywords to metadata in the smaller dataset
smd = metadata[metadata['id'].isin(links_small)]

# From the crew we will only pick the director as a feature.
# From the cast, we will only pick the first 3 mentioned as we assume that they are the most influential

smd['cast'] = smd['cast'].apply(literal_eval)
smd['crew'] = smd['crew'].apply(literal_eval)
smd['keywords'] = smd['keywords'].apply(literal_eval)
smd['cast_size'] = smd['cast'].apply(lambda x: len(x))
smd['crew_size'] = smd['crew'].apply(lambda x: len(x))


# Function that collects directors name
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

# Create new column that will hold the diroctors name
smd['director'] = smd['crew'].apply(get_director)

# Collect the first 3 cast members
smd['cast'] = smd['cast'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
smd['cast'] = smd['cast'].apply(lambda x: x[:3] if len(x) >=3 else x)

smd['keywords'] = smd['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

# For each movie in the dataset, there will be a metadata dump in which 
# all the genres, director, main actors and keywords. There will then be a count matrix from a count vectoriser with 
# which we calculate the cosine similarities and return movies that are most similar. 

# For the genre and credit data, we will strip spaces and convert to lowercase. We will also mention the director 3 
# times to increase its weighting to that above the cast.

smd['cast'] = smd['cast'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])

smd['director'] = smd['director'].astype('str').apply(lambda x: str.lower(x.replace(" ", "")))
smd['director'] = smd['director'].apply(lambda x: [x,x, x])

# Get weighted rating for each movie
vote_counts = metadata[metadata['vote_count'].notnull()]['vote_count'].astype('int')
vote_averages = metadata[metadata['vote_average'].notnull()]['vote_average'].astype('int')
C = vote_averages.mean()
m = vote_counts.quantile(0.95)

metadata['year'] = pd.to_datetime(metadata['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)


qualified = metadata[(metadata['vote_count'] >= m) & (metadata['vote_count'].notnull()) & (metadata['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity', 'genres']]
qualified['vote_count'] = qualified['vote_count'].astype('int')
qualified['vote_average'] = qualified['vote_average'].astype('int')


def weighted_rating(x):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)

qualified['wr'] = qualified.apply(weighted_rating, axis=1)
# List movies with the highest weighted ratings
qualified = qualified.sort_values('wr', ascending=False).head(250)

# For the keywords 
s = smd.apply(lambda x: pd.Series(x['keywords']),axis=1).stack().reset_index(level=1, drop=True)
s.name = 'keyword'

s = s.value_counts()

# To avoid duplicates remove the plurals from all the words
s = s[s > 1]

stemmer = SnowballStemmer('english')

def filter_keywords(x):
    words = []
    for i in x:
        if i in s:
            words.append(i)
    return words


# I use the TMDB Ratings to come up with our Top Movies Chart. I will use IMDB's weighted rating formula to construct my chart. Mathematically, it is represented as follows:
# 
# Weighted Rating (WR) =  (vv+m.R)+(mv+m.C)
#  
# where,
# 
# v is the number of votes for the movie
# m is the minimum votes required to be listed in the chart
# R is the average rating of the movie
# C is the mean vote across the whole report
# The next step is to determine an appropriate value for m, the minimum votes required to be listed in the chart. We will use 95th percentile as our cutoff. In other words, for a movie to feature in the charts, it must have more votes than at least 95% of the movies in the list.
# 
# I will build our overall Top 250 Chart and will define a function to build charts for a particular genre. Let's begin!

vote_counts = metadata[metadata['vote_count'].notnull()]['vote_count'].astype('int')
vote_averages = metadata[metadata['vote_average'].notnull()]['vote_average'].astype('int')
C = vote_averages.mean()

m = vote_counts.quantile(0.95)

metadata['year'] = pd.to_datetime(metadata['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)

qualified = metadata[(metadata['vote_count'] >= m) & (metadata['vote_count'].notnull()) & (metadata['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity', 'genres']]
qualified['vote_count'] = qualified['vote_count'].astype('int')
qualified['vote_average'] = qualified['vote_average'].astype('int')


# I use the TMDB Ratings to come up with our Top Movies Chart. I will use IMDB's weighted rating formula to construct my chart. Mathematically, it is represented as follows:
# Weighted Rating (WR) = (vv+m.R)+(mv+m.C) where, v is the number of votes for the movie m is the minimum votes required to be listed in the chart R is the 
# average rating of the movie C is the mean vote across the whole report The next step is to determine an appropriate value for m, the minimum votes required to be listed in the chart. 
# We will use 95th percentile as our cutoff. In other words, for a movie to feature in the charts, it must have more votes than at least 95% of the movies in the list. 
# I will build our overall Top 250 Chart and will define a function to build charts for a particular genre. Let's begin!

def weighted_rating(x):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * C)

smd['keywords'] = smd['keywords'].apply(filter_keywords)
smd['keywords'] = smd['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
smd['keywords'] = smd['keywords'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])

smd['soup'] = smd['keywords'] + smd['cast'] + smd['keywords'] + smd['cast'] +  smd['director'] 
# smd['soup'] =  + smd['genres']
smd['soup'] = smd['soup'].apply(lambda x: ' '.join(x))

count = CountVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
count_matrix = count.fit_transform(smd['soup'])

cosine_sim = cosine_similarity(count_matrix, count_matrix)

smd = smd.reset_index()
titles = smd['title']
indices = pd.Series(smd.index, index=smd['title'])

# From our results, we can see that we need to remove the bad movies (those that have low ratings). 
# I will take the top 25 movies based on similarity scores and calculate the vote of the 60th percentile movie. 
# Then, using this as the value of m, we will calculate the weighted rating of each movie using IMDB's formula like we did in the Simple Recommender section.

# Returns a dataframe ??
def improved_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]
    
    movies = smd.iloc[movie_indices][['title', 'vote_count', 'vote_average']]
    vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(0.60)
    qualified = movies[(movies['vote_count'] >= m) & (movies['vote_count'].notnull()) & (movies['vote_average'].notnull())]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    qualified['wr'] = qualified.apply(weighted_rating, axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(6)
    q_dict = qualified.to_json
    print (q_dict)


print('done')


improved_recommendations('Interstellar')

