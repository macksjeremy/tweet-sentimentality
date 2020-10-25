import nltk
import random
import tweepy
import csv
import os
from nltk.classify.scikitlearn import SklearnClassifier
import pickle
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize
import re
#API.user_timeline([id/user_id/screen_name][, since_id][, max_id][, count][, page])
#https://gist.github.com/yanofsky/5436496
consumer_key =
consumer_secret =




access_token =
access_secret =
access_key = access_token

def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    # initialize a list to hold all the tweepy Tweets
    alltweets = []
    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    # save most recent tweets
    alltweets.extend(new_tweets)
    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print(f"getting tweets before {oldest}")
        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        # save most recent tweets
        alltweets.extend(new_tweets)
        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        print(f"...{len(alltweets)} tweets downloaded so far")
    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    # write the csv
    with open(f'new_{screen_name}_tweets.csv', 'w',encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)

    pass

files_pos = os.listdir('train/pos')
files_pos = [open('train/pos/'+f, 'r').read() for f in files_pos]
files_neg = os.listdir('train/neg')
files_neg = [open('train/neg/'+f, 'r').read() for f in files_neg]


all_words = []
documents = []

stop_words = list(set(stopwords.words('english')))

#  j is adject, r is adverb, and v is verb
# allowed_word_types = ["J","R","V"]
allowed_word_types = ["J"]

for p in files_pos:

    # create a list of tuples where the first element of each tuple is a review
    # the second element is the label
    documents.append((p, "pos"))

    # remove punctuations
    cleaned = re.sub(r'[^(a-zA-Z)\s]', '', p)

    # tokenize
    tokenized = word_tokenize(cleaned)

    # remove stopwords
    stopped = [w for w in tokenized if not w in stop_words]

    # parts of speech tagging for each word
    pos = nltk.pos_tag(stopped)

    # make a list of  all adjectives identified by the allowed word types list above
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

for p in files_neg:
    # create a list of tuples where the first element of each tuple is a review
    # the second element is the label
    documents.append((p, "neg"))

    # remove punctuations
    cleaned = re.sub(r'[^(a-zA-Z)\s]', '', p)

    # tokenize
    tokenized = word_tokenize(cleaned)

    # remove stopwords
    stopped = [w for w in tokenized if not w in stop_words]

    # parts of speech tagging for each word
    neg = nltk.pos_tag(stopped)

    # make a list of  all adjectives identified by the allowed word types list above
    for w in neg:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

print("Beginning NLTK Training")
print("Beginning this wonderful program")

authentication = tweepy.OAuthHandler(consumer_key,consumer_secret)
authentication.set_access_token(access_token, access_secret)

api = tweepy.API(authentication)
search = api.search("Donald_Trump")

for items in search:
    print(items.text)

search2 = api.statuses_lookup("realDonaldTrump")

for items in search:
    print(items.text)
for tweet in tweepy.Cursor(api.user_timeline,id="RealDonaldTrump").items():
    print(tweet.text)