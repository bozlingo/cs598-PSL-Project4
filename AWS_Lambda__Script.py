# import the JSON utility package since we will be working with a JSON object
import json
import numpy as np
import pandas as pd

def load_ratings():
  ratingsData = 'https://liangfgithub.github.io/MovieData/ratings.dat?raw=true'

  ratings = pd.read_csv(ratingsData, sep='::', engine='python', header=None)
  ratings.columns = ['UserID', 'MovieID', 'Rating', 'Timestamp']

  return ratings

def load_movies():
  moviesData = 'https://liangfgithub.github.io/MovieData/movies.dat?raw=true'

  movies = pd.read_csv(moviesData, sep='::', engine='python', encoding="ISO-8859-1", header=None)
  movies.columns = ['MovieID', 'Title', 'Genres']

  base_image_url = "https://liangfgithub.github.io/MovieImages/"
  movies['Poster_URL'] = movies['MovieID'].apply(lambda x: f"{base_image_url}{x}.jpg?raw=true")

  return movies

#system 1
def calculate_weighted_ratings(ratings, movies):
    rating_merged = ratings.merge(movies, on='MovieID')

    # Calculate average rating and rating count for each movie
    movie_rating = rating_merged.groupby("MovieID")['Rating'].agg(['mean', 'count']).reset_index()
    movie_rating.columns = ['MovieID', 'Rating', 'Rating_count']

    # Calculate weighted average rating
    avg_rating_count = movie_rating['Rating_count'].mean()
    avg_rating = movie_rating['Rating'].mean()

    movie_rating['Weighted_Rating'] = (
        (movie_rating['Rating'] * movie_rating['Rating_count'] + avg_rating * avg_rating_count) /
        (movie_rating['Rating_count'] + avg_rating_count)
    )

    movie_with_rating = movies.merge(movie_rating, on='MovieID', how='left')

    movie_with_rating['Weighted_Rating'] = movie_with_rating['Weighted_Rating'].fillna(avg_rating)

    return movie_with_rating

#system 1 display
def get_top_movies(movie_with_rating, top_n=10):
    return movie_with_rating.sort_values(by='Weighted_Rating', ascending=False).head(top_n)

#system 2
def myIBCF (newuser):
  S = pd.read_csv('https://cs598-psl.s3.us-east-2.amazonaws.com/top_30_similarity_matrix(1).csv', index_col = 0)

  predictions = []
  for i in range(S.shape[0]):  # For each movie
    if pd.notna(newuser.iloc[i]):  # Skip already rated movies
      predictions.append(np.nan)
      continue

    # Get indices of items that are similar and rated
    similar_movies = S.iloc[i, :]
    rated_indices = newuser.notna()

    common_indices = similar_movies.index[rated_indices]
    common_similarities = similar_movies[common_indices]
    common_ratings = newuser[common_indices]

    # Compute the prediction for movie i
    numerator = np.nansum(common_similarities * common_ratings)
    denominator = np.nansum(common_similarities)
    prediction = numerator / denominator if denominator != 0 else np.nan
    predictions.append(prediction)

  # Get top 10 recommended movies
  predictions = pd.Series(predictions, index=S.index)
  top_10_movies = predictions.nlargest(10).index.tolist()

  # Fill missing recommendations with most popular movies
  if len(top_10_movies) < 10:
    # Get top 10 popular movies calculated from System 1
    popular_movies = ['m' + str(movie_id) for movie_id in top_10_popular_movies.iloc[:, 0]]
    top_10_movies += popular_movies[:10 - len(top_10_movies)]

  return top_10_movies

# define the handler function that the Lambda service will use as an entry point
def lambda_handler(event, context):
  # extract values from the event object we got from the Lambda service
  if (event['reviews'] == ""):
    ratings = load_ratings()
    movies = load_movies()

    movie_with_rating = calculate_weighted_ratings(ratings, movies)
    top_10_popular_movies = get_top_movies(movie_with_rating, top_n=10)

    results = []

    for _, row in top_10_popular_movies.iterrows():
      print (row)

      item = {"MovieID" : row['MovieID'], "Title" : row['Title'], "Poster_URL" : row['Poster_URL']}
      results.append(item)

    print (results)

    #system 1
    results = [
            {"MovieID":2858,"Title":"American Beauty (1999)","Genres":"Comedy|Drama","Poster_URL":"https:\/\/liangfgithub.github.io\/MovieImages\/2858.jpg?raw=true","Rating":4.317386231,"Rating_count":3428.0,"Weighted_Rating":4.0752679965},
            {"MovieID":260,"Title":"Star Wars: Episode IV - A New Hope (1977)","Genres":"Action|Adventure|Fantasy|Sci-Fi","Poster_URL":"https:\/\/liangfgithub.github.io\/MovieImages\/260.jpg?raw=true","Rating":4.4536944166,"Rating_count":2991.0,"Weighted_Rating":4.1678476904},
            {"MovieID":1196,"Title":"Star Wars: Episode V - The Empire Strikes Back (1980)","Genres":"Action|Adventure|Drama|Sci-Fi|War","Poster_URL":"https:\/\/liangfgithub.github.io\/MovieImages\/1196.jpg?raw=true","Rating":4.2929765886,"Rating_count":2990.0,"Weighted_Rating":4.0203481473},
            {"MovieID":1210,"Title":"Star Wars: Episode VI - Return of the Jedi (1983)","Genres":"Action|Adventure|Romance|Sci-Fi|War","Poster_URL":"https:\/\/liangfgithub.github.io\/MovieImages\/1210.jpg?raw=true","Rating":4.02289282,"Rating_count":2883.0,"Weighted_Rating":3.7641314766},
            {"MovieID":480,"Title":"Jurassic Park (1993)","Genres":"Action|Adventure|Sci-Fi","Poster_URL":"https:\/\/liangfgithub.github.io\/MovieImages\/480.jpg?raw=true","Rating":3.7638473054,"Rating_count":2672.0,"Weighted_Rating":3.5102917724},
            {"MovieID":2028,"Title":"Saving Private Ryan (1998)","Genres":"Action|Drama|War","Poster_URL":"https:\/\/liangfgithub.github.io\/MovieImages\/2028.jpg?raw=true","Rating":4.3373539389,"Rating_count":2653.0,"Weighted_Rating":4.029194643},
            {"MovieID":589,"Title":"Terminator 2: Judgment Day (1991)","Genres":"Action|Sci-Fi|Thriller","Poster_URL":"https:\/\/liangfgithub.github.io\/MovieImages\/589.jpg?raw=true","Rating":4.0585126463,"Rating_count":2649.0,"Weighted_Rating":3.7757135423},
            {"MovieID":2571,"Title":"Matrix, The (1999)","Genres":"Action|Sci-Fi|Thriller","Poster_URL":"https:\/\/liangfgithub.github.io\/MovieImages\/2571.jpg?raw=true","Rating":4.3158301158,"Rating_count":2590.0,"Weighted_Rating":4.0029136458},
            {"MovieID":1270,"Title":"Back to the Future (1985)","Genres":"Comedy|Sci-Fi","Poster_URL":"https:\/\/liangfgithub.github.io\/MovieImages\/1270.jpg?raw=true","Rating":3.9903213318,"Rating_count":2583.0,"Weighted_Rating":3.7074308649},
            {"MovieID":593,"Title":"Silence of the Lambs, The (1991)","Genres":"Drama|Thriller","Poster_URL":"https:\/\/liangfgithub.github.io\/MovieImages\/593.jpg?raw=true","Rating":4.3518231187,"Rating_count":2578.0,"Weighted_Rating":4.0341771398}]
  else:
    #system 2

    inputMovies = event['reviews']   

    refMovies = load_movies()

    newuser = pd.DataFrame([np.nan] * 3706).T

    newuser.columns = pd.read_csv('https://cs598-psl.s3.us-east-2.amazonaws.com/columns.csv', header=None).squeeze().tolist()

    for movie in inputMovies:
      newuser.loc[:, "m" + str(movie["MovieID"])] = movie["Rating"]

    myResults = myIBCF (newuser.iloc[0])
    results = []

    for recID in myResults:
      title = refMovies.loc[int(recID[1:])]["Title"]
      posterURL = refMovies.loc[int(recID[1:])]["Poster_URL"]
      item = {"MovieID" : recID[1:], "Title" : title, "Poster_URL" : posterURL}
      results.append(item)
    #print (results)

  return {
    'statusCode': 200,
    'body': json.dumps(results)
  }