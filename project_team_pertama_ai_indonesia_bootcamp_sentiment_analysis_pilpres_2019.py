# -*- coding: utf-8 -*-
"""Project team pertama - AI Indonesia Bootcamp - Sentiment analysis PILPRES 2019.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12PCLrgivjJbwhcZtehVoY-b550OiNQct
"""

import pandas as pd
from google.colab import drive

from google.colab import drive
drive.mount('/content/drive', force_remount = True)

train_df = pd.read_csv('/content/drive/MyDrive/Indonesia AI Bootcamp project/Sentiment Analaysis /tweet.csv')

train_df.head(5)

train_df.drop('Unnamed: 0', inplace=True, axis=1)

train_df.head(5)

display(train_df.info())
display(train_df.head())

!pip install Sastrawi
import csv
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import csv
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from sklearn import preprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
# factory = StemmerFactory()
# stemmer = factory.create_stemmer()

labelEncoder = preprocessing.LabelEncoder()
train_df['sentimen'] = labelEncoder.fit_transform(train_df['sentimen'])

train_df.sentimen.value_counts()

X = train_df['tweet'].copy()
y = train_df['sentimen'].copy()

swFunc = StopWordRemoverFactory()
stopword = swFunc.create_stop_word_remover()
stemFunc = StemmerFactory()
stemmer = stemFunc.create_stemmer()

def clean_tweet(tweet):
  # remove extra white space
  tweet  = tweet.strip()
  # convert to lower case
  tweet = tweet.lower()
  # remove hasthtag
  tweet = re.sub(r"#\w+", "", tweet)
  # remove non alpha numeric characters
  tweet = re.sub(r"[^\w\s]+", "", tweet)
  # tweet = re.sub(r"\s+", "", tweet)
  # remove angka
  tweet = re.sub(r"\d+", "", tweet)
  # remove tanda baca
  tweet = tweet.translate(str.maketrans("","",string.punctuation))
  # stopwords dengan sastrawi
  tweet = stopword.remove(tweet)
  # stemming dengan sastrawi
  tweet = stemmer.stem(tweet)
  # # tokenizing
  # tweet = word_tokenize(tweet)

  return tweet

X

X_cleaned = X.apply(clean_tweet)
X_cleaned

tfidf_vectorizer = TfidfVectorizer()
tfidf_vectorizer.fit(X_cleaned)
X = tfidf_vectorizer.transform(X_cleaned)

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.70)

text_classifier = RandomForestClassifier(n_estimators=500, random_state=40)
text_classifier.fit(X_train, y_train)

y_pred = text_classifier.predict(X_test)
print(classification_report(y_test, y_pred))