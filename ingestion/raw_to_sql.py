#!/usr/bin/python3
import os, csv
from pathlib import Path

data_dir = Path('2_reviews_per_movie_raw/')
out_file = 'out.csv'

def clean(row, movie_name):
    # Input is read as an array of strings; entries are in the
    # format [user, rating, helpful, total, date, title, review]. 
    try:
        rating, helpful, title, review = int(row[1]), int(row[2]), row[5], row[6]
        
        # Here, we clean the data using a handful of steps.
        # First, we normalize rating (to be between -1 and 1).
        # We also combine the title and review, while filtering
        # out miscellaneous stuff.
        norm_rating = (rating - 1) * 2 / 9 - 1
        title_review = f'{title} {review}'.replace('<br/>', '').replace('\n', '')
        return [movie_name, norm_rating, helpful, title_review]
    except ValueError:
        # Ignore unparseable data (like null ratings, etc.)
        return None

with open(out_file, 'w', newline='') as out_csv:
    writer = csv.writer(out_csv, dialect='unix')
    for fname in data_dir.glob('*.csv'):
        movie_name = fname.stem
        print(f'Processing movie {movie_name}...')

        with open(fname, newline='') as data_file:
            reader = csv.reader(data_file)
            rows = [row for r in reader if (row := clean(r, movie_name))] 
            writer.writerows(rows)

