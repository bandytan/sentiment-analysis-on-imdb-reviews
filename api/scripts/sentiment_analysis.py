import pandas as pd
import nltk, json, warnings, sys
from nltk.corpus import stopwords
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

warnings.filterwarnings('ignore') 

in_csv = sys.argv[1]
out_json = sys.argv[2]

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

#############################
## COSINE SIMILARITY SCORE ##
#############################
results = {
    'reviews': df[['review', 'norm_rating', 'review_polarity']].to_dict(orient='records'),
    'cosine_similarity': 1 - cosine(df['norm_rating'], df['review_polarity']),
    'top_words': top_words
}

with open(out_json, 'w') as out:
    json.dump(results, out)