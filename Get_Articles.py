import os
import urllib.request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from newspaper import Article
from newspaper import Config
import re
import string
from tqdm.auto import tqdm
import time



file = 'bitcoin_links.csv'


def get_link_list(file):
    df = pd.read_csv(file,encoding='cp1252')
    link_lists = []
    number_of_articles = df.shape[0]

    for n in range(number_of_articles):

        link = df.iloc[n, 1]
        title = df.iloc[n, 0]
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

        # print(df_text_analyzed)
        return df_text_analyzed


link_list = get_link_list(file)

i = 0;
os.mkdir('Articles')
for l in tqdm(link_list, desc = 'Getting Articles'):
    get_article(l, 'Articles/Article_' + str(i))
    i = i + 1

j = 0
num_of_Articles = (len([name for name in os.listdir('Articles') if os.path.isfile(os.path.join('Articles', name))]))
os.mkdir('Cleaned_Articles')
for a in tqdm(range(num_of_Articles), desc = 'Cleaning Articles'):
    clean_article('Articles/Article_' + str(j) + '.txt', 'Cleaned_Articles/Cleaned_Article_' + str(j) + '.txt')
    j = j + 1

k = 0
os.mkdir('Sentiment_Analysis_Articles')
num_of_Cleaned_Articles = (len([name for name in os.listdir('Cleaned_Articles') if os.path.isfile(os.path.join('Cleaned_Articles', name))]))
article_name = []
sentiment_score = []
for ca in tqdm(range(num_of_Cleaned_Articles), desc = 'Performing Sentiment Analysis'):
    article_name.append('Cleaned_Article_' + str(k) + '.txt')
    sentiment_score.append(article_sentiment_analysis('Cleaned_Articles/Cleaned_Article_' + str(k) + '.txt'))
    k = k + 1

data = {'Article Name': article_name,
        'Sentiment Score': sentiment_score
        }

df_score = pd.DataFrame(data, columns=['Article Name','Sentiment Score'])
pd.set_option('display.max.columns', None)
print(df_score)

df_score.to_pickle('dataframe')

# Then you can load it back using:
# df = pd.read_pickle(file_name)