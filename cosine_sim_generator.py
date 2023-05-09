import pandas as pd
import glob
from scipy import spatial
movies = pd.DataFrame(columns=["movie", "cosine_sim"])
path = '/Users/laureneterno/Desktop/output/*.csv'
for filename in glob.glob(path):
  df = pd.read_csv(filename)
  df = df[['movie', 'rating','review_polarity']]   
  result = 1 - spatial.distance.cosine(df['rating'], df['review_polarity'])
  movies.loc[len(movies.index)] = [df['movie'][0],  result]
  filepath = "/Users/laureneterno/Desktop/cosine_sim.csv"
movies.to_csv(filepath)