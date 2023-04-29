#!/usr/bin/python3
import csv, re, string
from pathlib import Path

data_dir = Path('2_reviews_per_movie_raw/')
out_file = 'out.csv'
filter_keywords = ['<br/>', 'movie', 'film', '\n']
tbl = string.punctuation
spaces = ' ' * len(string.punctuation)

def clean(row, file_name):
    movie_name = file_name[:-5]

    # Input is read as an array of strings; entries are in the
    # format [user, rating, helpful, total, date, title, review]. 
    try:
        rating, helpful, title, review = int(row[1]), int(row[2]), row[5], row[6]
        
        # Here, we clean the data using a handful of steps.
        # First, we normalize rating (to be between -1 and 1).
        # We also combine the title and review, while filtering
        # out miscellaneous stuff.
        norm_rating = (rating - 1) * 2 / 9 - 1
        combined = f'{title} {review}'
        for keywd in filter_keywords:
            combined = combined.replace(keywd, '')
        filtered_moviename = re.sub(re.escape(movie_name), '', combined, flags=re.IGNORECASE)
        filtered_punctuation = filtered_moviename.translate(str.maketrans(tbl, spaces))
        return [movie_name, norm_rating, helpful, filtered_punctuation]
    except ValueError:
        # Ignore unparseable data (like null ratings, etc.)
        return None

with open(out_file, 'w', newline='', encoding='utf-8') as out_csv:
    writer = csv.writer(out_csv, dialect='unix')
    for fname in data_dir.glob('*.csv'):
        movie_name = fname.stem
        print(f'Processing movie {movie_name}...')

        with open(fname, newline='', encoding='utf-8') as data_file:
            reader = csv.reader(data_file)
            rows = [row for r in reader if (row := clean(r, movie_name))] 
            writer.writerows(rows)

