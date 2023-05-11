import pandas as pd
import nltk, json, warnings, sys
from nltk.corpus import stopwords
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from scipy.stats import pearsonr
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

warnings.filterwarnings('ignore') 

_, in_csv, out_json, *out_csvs = sys.argv
review_csv, movie_csv, tfidf_csv = out_csvs

############################
## NLTK & TF-IDF ANALYSIS ##
############################
nltk_cache_dir = './nltk'
nltk.download('stopwords', download_dir=nltk_cache_dir, quiet=True)
nltk.download('punkt', download_dir=nltk_cache_dir, quiet=True)
nltk.data.path.append(nltk_cache_dir)

# CSV has movie_name, rating, helpful, review columns:
movie_data = pd.read_csv(in_csv)

def generate_nlp_features(df):
    vect = TfidfVectorizer( 
        tokenizer=word_tokenize,
        lowercase=True,
        analyzer='word', 
        ngram_range=(1,3), # unigram, bigram and trigram 
        max_features=100, # vocabulary that only consider the top max_features ordered by term frequency across the corpus
        min_df=5, # minimum word frequency required to be in model
        stop_words=stopwords.words('english') # remove stopwords
    )

    review = pd.Series(df['review'])

    tfidf_fit_review = vect.fit(review)
    tfidf_array = tfidf_fit_review.transform(review).toarray()
    tfidf_df = pd.DataFrame(tfidf_array)
    tfidf_df.columns = list(map(lambda x : 'review_' + str(x), tfidf_df.columns))

    df = pd.merge(df, tfidf_df, left_index=True, right_index=True)
    feature_names = vect.get_feature_names_out()
    top_words = {}

    # Get the indices of the top 50 words based on their TF-IDF scores
    top_word_indices = tfidf_array.sum(axis=0).argsort()[-50:][::-1]
    for i in top_word_indices:
        top_words[feature_names[i]] = tfidf_array.sum(axis=0)[i]
    
    return (df, top_words)

df, top_words = generate_nlp_features(movie_data)
df['review_polarity'] = df['review'].apply(lambda x: TextBlob(x).sentiment.polarity)

movie_name = df['movie_name'].iloc[0]
tfidf_list = [{'word': wd, 'tfidf': frq} for wd, frq in top_words.items()]
tfidf_df = pd.DataFrame(tfidf_list)
tfidf_df['movie_name'] = movie_name

#############################
## COSINE SIMILARITY SCORE ##
#############################
df = df[['movie_name', 'review', 'norm_rating', 'review_polarity']]
pearson_r, p_value = pearsonr(df['norm_rating'], df['review_polarity'])
results = {
    'reviews': df[['review', 'norm_rating', 'review_polarity']].to_dict(orient='records'),
    'pearson_r': pearson_r,
    'p_value': p_value,
    'top_words': top_words
}

movie_df = pd.DataFrame([{
    'movie_name': movie_name,
    'pearson_r': pearson_r,
    'p_value': p_value
}])

# Here, we stream our outputs into several files:
# sentiment.json (which is piped to the API's HTTP response)
# [a whole bunch of csvs]  (which is fed directly into MySQL) 
with open(out_json, 'w') as out:
    json.dump(results, out)

df.to_csv(review_csv, index=False, header=False)
movie_df.to_csv(movie_csv, index=False, header=False)
tfidf_df.to_csv(tfidf_csv, index=False, header=False)