import pandas as pd
import glob
from scipy import stats, spatial
# all the movies (w/o accuracy check)
movies = pd.DataFrame(columns=["movie", "pearson", "p-value"])
path = '/Users/laureneterno/Desktop/output/*.csv'
for filename in glob.glob(path):
  df = pd.read_csv(filename)
  df = df[['movie', 'rating','review_polarity']]   
  result = stats.pearsonr(df['rating'], df['review_polarity'])
  movies.loc[len(movies.index)] = [df['movie'][0],  result[0], result[1]]
filepath = "/Users/laureneterno/Desktop/pearson.csv"
movies.to_csv(filepath)

# the three movies with the accuracy check (the deployable one)
path1 = '/Users/laureneterno/Desktop/accuracy_check/*.csv'
movies_w_accuracy = pd.DataFrame(columns=["movie", "pearson_ratings_polarity", "p_value_ratings_polarity", "cosine_sim_polarity_manual"])
for filename in glob.glob(path1):
  df = pd.read_csv(filename)
  df = df[['movie', 'rating','review_polarity', 'manual_polarity']]   
  result_ratings_polarity = stats.pearsonr(df['rating'], df['review_polarity'])
  results_polarity_manual =  1 - spatial.distance.cosine(df['manual_polarity'], df['review_polarity'])
  movies_w_accuracy.loc[len(movies_w_accuracy.index)] = [df['movie'][0],  result_ratings_polarity[0], result_ratings_polarity[1], results_polarity_manual]
filepath1 = "/Users/laureneterno/Desktop/pearson_with_accuracy.csv"
movies_w_accuracy.to_csv(filepath1)
