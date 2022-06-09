# https://www.youtube.com/watch?v=7azmUg6XZA0

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

file = 'xrp_links.csv'

df = pd.read_csv(file,encoding='cp1252')
# print(df.head())

analyzer = SentimentIntensityAnalyzer()

negative = []
neutral = []
positive = []

for n in range(df.shape[0]):

    title = df.iloc[n,0]
    link = df.iloc[n, 1]
    description = df.iloc[n, 2]

    title_analyzed = analyzer.polarity_scores(title)
    link_analyzed = analyzer.polarity_scores(link)
    description_analyzed = analyzer.polarity_scores(description)

    # Adding findings to original df
    negative.append(((title_analyzed['neg']) + (description_analyzed['neg']))/2)
    neutral.append(((title_analyzed['neu']) + (description_analyzed['neu']))/2)
    positive.append(((title_analyzed['pos']) + (description_analyzed['pos']))/2)

df['Negative'] = negative
df['Neutral'] = neutral
df['Positive'] = positive

pd.set_option('display.max.columns', None)
# print(df.head())


most_negative_articles = df.nlargest(5,['Negative'])
most_neutral_articles = df.nlargest(5,['Neutral'])
most_positive_articles = df.nlargest(5,['Positive'])

negative_mean = df['Negative'].mean()
neutral_mean = df['Neutral'].mean()
positive_mean = df['Positive'].mean()

print(negative_mean, neutral_mean,positive_mean)