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
out_file=sentiment.json
sentiment_analysis_script=sentiment_analysis.py
python3 $sentiment_analysis_script $cleaned_csv $out_file
cat $out_file

# Cleanup:
rm $in_file $cleaned_csv $out_file
