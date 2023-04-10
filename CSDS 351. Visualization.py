# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 16:55:36 2023

@author: paula
"""

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

### SCATTER PLOT

data1 = pd.read_csv("movie1.csv")
data2 = pd.read_csv("movie2.csv")
data3 = pd.read_csv("movie3.csv")

# Plot

fig, axs = plt.subplots(3, 1, figsize=(8, 12))

axs[0].scatter(x=data1['rating'], y=data1['review_polarity'])
axs[0].set_title("Movie 1")
axs[0].set_xlabel("Rating")
axs[0].set_ylabel("Polarity")

axs[1].scatter(x=data2['rating'], y=data2['review_polarity'])
axs[1].set_title("Movie 2")
axs[1].set_xlabel("Rating")
axs[1].set_ylabel("Polarity")

axs[2].scatter(x=data3['rating'], y=data3['review_polarity'])
axs[2].set_title("Movie 3")
axs[2].set_xlabel("Rating")
axs[2].set_ylabel("Polarity")

plt.tight_layout()
plt.show()


data = pd.concat([data1, data2, data3], axis = 0)

plt.scatter(x=data['rating'], y=data['review_polarity'])
plt.title("Movies 1, 2, 3")
plt.xlabel("Rating")
plt.ylabel("Polarity")
plt.show()


### WORD CLOUD


# Read the input text file and extract the list of words and their importance
with open('movie1_tfidf_feature_names.txt', 'r') as f:
    text1 = f.read()
    
with open('movie2_tfidf_feature_names.txt', 'r') as f:
    text2 = f.read()
    
with open('movie3_tfidf_feature_names.txt', 'r') as f:
    text3 = f.read()
    
# Convert the list of words and their importance to a dictionary

list1 = eval(text1)
words1 = {word: index for index, word in list1}

list2 = eval(text2)
words2 = {word: index for index, word in list2}

list3 = eval(text3)
words3 = {word: index for index, word in list3}

# Remove numbers and the words "film" and "movie" from the dictionaries

for words in [words1, words2, words3]:
    for key in list(words.keys()):
        if str(key).isnumeric() or key == "movie" or key == "film":
            del words[key]

# Plot

wordcloud1 = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate_from_frequencies(words1)
wordcloud2 = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate_from_frequencies(words2)
wordcloud3 = WordCloud(width=800, height=800, background_color='white', min_font_size=10).generate_from_frequencies(words3)

fig, axs = plt.subplots(1, 3, figsize=(12, 4))

axs[0].imshow(wordcloud1)
axs[0].axis("off")
axs[0].set_title("Movie 1")

axs[1].imshow(wordcloud2)
axs[1].axis("off")
axs[1].set_title("Movie 2")

axs[2].imshow(wordcloud3)
axs[2].axis("off")
axs[2].set_title("Movie 3")

plt.tight_layout()
plt.show()



