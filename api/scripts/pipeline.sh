#!/bin/bash

# First, we need to ensure that the input file exists.
# Otherwise, we abort with an error.
in_file=req.json
if [[ ! -f $in_file ]]; then
    echo 'Expected input file not found!'
    exit 1
fi

# Parsing & initial cleaning:
raw_to_csv_script=raw_json_to_csv.py
cleaned_csv=cleaned.csv
python3 $raw_to_csv_script $cleaned_csv

# Sentiment analysis, TF-IDF, cosine similarity:
mkdir -p nltk
out_json=sentiment.json
review_csv=reviews.csv
movie_csv=movie.csv
tfidf_csv=tfidf.csv
sentiment_analysis_script=sentiment_analysis.py
python3 $sentiment_analysis_script $cleaned_csv $out_json $review_csv $movie_csv $tfidf_csv

# Load data into MySQL:
load_mysql_script=to_mysql.py
python3 $load_mysql_script $review_csv $movie_csv $tfidf_csv

cat $out_json

# Cleanup:
rm $in_file $cleaned_csv $out_json $review_csv $movie_csv $tfidf_csv
