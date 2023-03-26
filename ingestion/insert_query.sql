LOAD DATA LOCAL INFILE 'out.csv'
INTO TABLE review_data
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
(movie, rating, helpful, review);
