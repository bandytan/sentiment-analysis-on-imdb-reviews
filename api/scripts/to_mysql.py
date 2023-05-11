import os, pymysql, sys
from dotenv import load_dotenv

# Database connection initialization
load_dotenv()
db_conn = pymysql.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = 'movie_reviews',
    local_infile = True
)
db_cursor = db_conn.cursor()

# Table initialization
# movie_tbl_create = """
# CREATE TABLE IF NOT EXISTS `movies` (
#   `movie_name` varchar(80) CHARACTER SET utf8mb3 NOT NULL,
#   `pearson_r` float DEFAULT NULL,
#   `p_value` float DEFAULT NULL,
#   PRIMARY KEY (`movie_name`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
# """

# review_tbl_create = """
# CREATE TABLE `reviews` (
#   `id` int NOT NULL AUTO_INCREMENT,
#   `movie_name` varchar(80) CHARACTER SET utf8mb3 NOT NULL,
#   `review` text CHARACTER SET utf8mb3 NOT NULL,
#   `norm_rating` float NOT NULL,
#   `review_polarity` float NOT NULL,
#   PRIMARY KEY (`id`),
#   KEY `movie_name_idx` (`movie_name`),
#   CONSTRAINT `movie_name` FOREIGN KEY (`movie_name`) REFERENCES `movies` (`movie_name`) ON DELETE CASCADE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
# """

# tfidf_tbl_create = """
# CREATE TABLE `tfidf_words` (
#   `id` int NOT NULL AUTO_INCREMENT,
#   `movie_name` varchar(80) CHARACTER SET utf8mb3 NOT NULL,
#   `word` varchar(30) CHARACTER SET utf8mb3 NOT NULL,
#   `tfidf` float NOT NULL,
#   PRIMARY KEY (`id`),
#   KEY `movie_name_idx` (`movie_name`),
#   CONSTRAINT `tfidf_movie_src` FOREIGN KEY (`movie_name`) REFERENCES `movies` (`movie_name`) ON DELETE CASCADE
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
# """

# Data insertion
_, review_csv, movie_csv, tfidf_csv = sys.argv
movie_insert = f"""
LOAD DATA LOCAL INFILE '{movie_csv}'
INTO TABLE movies
FIELDS TERMINATED BY ','
(movie_name, pearson_r, p_value);
"""

review_insert = f"""
LOAD DATA LOCAL INFILE '{review_csv}'
INTO TABLE reviews
FIELDS TERMINATED BY ','
(movie_name, review, norm_rating, review_polarity);
"""

tfidf_insert = f"""
LOAD DATA LOCAL INFILE '{tfidf_csv}'
INTO TABLE tfidf_words
FIELDS TERMINATED BY ','
(word, tfidf, movie_name);
"""

for query in [movie_insert, review_insert, tfidf_insert]:
    affected_rows = db_cursor.execute(query)

db_conn.commit()
db_conn.close()