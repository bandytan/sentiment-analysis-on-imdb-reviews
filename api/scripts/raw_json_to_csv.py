import csv, json, re, string, sys

in_file = 'req.json'
out_file = sys.argv[1]
filter_keywords = ['<br/>', 'movie', 'film', '\n']
tbl = string.punctuation
spaces = ' ' * len(string.punctuation)

def clean(row, movie_name):
    # Input is read as a dictionary containing the parsed JSON input.
    try:
        rating = row['rating']
        helpful = row['helpful']
        title = row['title']
        review = row['review']
        
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
        return {
            'movie_name': movie_name,
            'norm_rating': norm_rating,
            'helpful': helpful,
            'review': filtered_punctuation
        }
    except ValueError:
        # Ignore unparseable data (like null ratings, etc.)
        return None

with open(out_file, 'w', newline='', encoding='utf-8') as out_csv:
    field_names = ['movie_name', 'norm_rating', 'helpful', 'review']
    writer = csv.DictWriter(out_csv, fieldnames=field_names, dialect='unix')
    writer.writeheader()
    with open(in_file) as data_file:
        data = json.load(data_file)
        movie_name = data['movie']
        rows = [row for r in data['reviews'] if (row := clean(r, movie_name))]
        writer.writerows(rows)

