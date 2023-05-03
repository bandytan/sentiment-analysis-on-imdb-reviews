USE movie_reviews;
LOAD DATA LOCAL INFILE 'out.csv'
INTO TABLE review_data
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
(movie, rating, helpful, review);
