import csv
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from newspaper import Article
from newspaper import Config
import re
import string
from tqdm.auto import tqdm
from datetime import date, timedelta
import datetime
import logging
import sys
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import time
from pygooglenews import GoogleNews
import pickle
import json
import statistics
import urllib.request
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from gensim import matutils, models
import scipy.sparse




def news_link(date_link_path, country,topic, date_use_format_start, date_use_format_next ):

    gn = GoogleNews(country = country )
    search = gn.search(topic, from_=date_use_format_start, to_=date_use_format_next)
    length = len(search['entries'])
    clean_date = date_use_format_start.replace('%', '')
    document = open(date_link_path + "/" + clean_date + "_" + topic + "_date_link.csv", "a")

    for i in range(length):

        link = search['entries'][i]['links'][0]['href']
        document.write("{}\n".format(link))

    document.close()


def get_link_list(file):
    df = pd.read_csv(file,encoding='cp1252', error_bad_lines=False)
    link_lists = []
    number_of_articles = df.shape[0]

    for n in range(number_of_articles):

        link = df.iloc[n, 0]
        link_lists.append(link)

    # print(link_lists[0])
    return(link_lists)


def get_article(link, save_title):
    config = Config()
    config.request_timeout = 10
    article = Article(link, config=config)
    article.download()
    article.parse()
    article.nlp()
    corpus = article.text
    f = open(save_title + ".txt", "w+")

    with open(save_title + ".txt", 'w', encoding='utf-8') as f:
        f.write(corpus)
        f.close()


def clean_article(article,save_title):
    # Get text...
    with open(article, 'r', encoding='utf-8') as f:
        text = f.read()
        f.close()

        # Apply a first round of text cleaning techniques
        text = text.lower()  # Make text lowercase
        text = re.sub('\[.*?\]', '', text)  # Remove text in square brackets.
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)  # Remove punctuation.
        text = re.sub('\w*\d\w*', '', text)  # Remove words containing numbers.
        text = re.sub('\n', '', text)  # Remove line spacing (\n).

        with open(save_title , 'w', encoding='utf-8') as f:
            f.write(text)
            f.close()


def article_sentiment_analysis(cleaned_article):
    with open(cleaned_article, 'r', encoding='utf-8') as f:
        text = f.read()
        f.close()
        text_array = [text]
        analyzer = SentimentIntensityAnalyzer()

        df = pd.DataFrame(text_array, columns=['Cleaned_Article'])
        df_text = df.iloc[0, 0]
        df_text_analyzed = analyzer.polarity_scores(df_text)
        return df_text_analyzed





        # with open(save_title , 'w', encoding='utf-8') as document:
        #     document.write("{}\n".format(df_text_analyzed))
        #     document.close()

        # print(df_text_analyzed)
        # return df_text_analyzed

def average(lst):
    if len(lst) > 0:
        return sum(lst) / len(lst)
    else :
        return 0