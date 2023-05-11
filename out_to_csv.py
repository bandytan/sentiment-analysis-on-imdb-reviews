# We'll just reuse some code for this part!
import csv
import pandas as pd
from pathlib import Path
from scipy.stats import pearsonr

data_dir = Path('output/')
script_dir = Path('api/scripts')

for review_csv in data_dir.glob('*.csv'):
    filename = review_csv.stem
    print(f'Processing {filename}...')

    # Read each file into a separate CSV that is parseable by LOAD DATA INFILE.
    # Check out the SQL insertion queries in api/scripts/to_mysql.py for details!
    df = pd.read_csv(review_csv)
    review_df = df[['movie', 'review', 'rating', 'review_polarity']]
    pearson_r, p_value = pearsonr(df['rating'], df['review_polarity'])
    movie_df = pd.DataFrame([{
        'movie_name': filename,
        'pearson_r': pearson_r,
        'p_value': p_value
    }])

    review_df.to_csv(script_dir / 'reviews.csv', header=False, index=False)
    movie_df.to_csv(script_dir / 'movie.csv', header=False, index=False)

    # Process TF-IDF data separately, since it's in a different format...
    # Also yes, the file names are messed up. Not my fault!
    words_txt = data_dir / f'{filename}_polarity.txt'
    with open(words_txt, errors='ignore') as tfidf_data, open(script_dir / 'tfidf.csv', 'w', newline='') as tfidf_out:
        writer = csv.writer(tfidf_out)
        for line in tfidf_data:
            word, freq = line.rstrip().split(': ', 2)
            writer.writerow([word, freq, filename])

    # Execute the insertion script:
    exec(open(script_dir / 'to_mysql.py').read())
