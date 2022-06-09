# https://github.com/kotartemiy/pygooglenews

from PythonProjects.NLP_Trading_Bot.NLP_methods import *

# The following code will log "DEBUG" to the console.
# ---------------------------------------------------------------------------------------------------
# logging.basicConfig( level=logging.DEBUG, format='%(asctime)s: line:%(lineno)d: %(levelname)s: %(message)s')
# ---------------------------------------------------------------------------------------------------


# The following code will log "INFO" to the console.
# ---------------------------------------------------------------------------------------------------
logging.basicConfig( level=logging.INFO, format='%(asctime)s: line:%(lineno)d: %(levelname)s: %(message)s')
# ---------------------------------------------------------------------------------------------------

country = 'usa'
topic = 'bitcoin'
ticker = 'BTC'
currency_unit = 'ZAR'
API_key = "9881bfae39e5ffb6b94740a0fe09bed7"  # https://p.nomics.com/cryptocurrency-bitcoin-api
start_date = date(2021, 1, 1)
end_date = date(2021,6, 8)
now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
decimal_round = 2

# Define the name of the directories to be created
# path = str(now + '_' + topic)
path = str('this_year_so_far' + '_' + topic + '_2')
num_of_stages = '8'
date_links_path = path + '/Stage_1_' + topic + "_date_links"
news_articles_path = path + '/Stage_2_' + topic + "_news_articles"
clean_articles_path = path + '/Stage_3_' + topic + "_cleaned_news_articles"
correlation_test_path = path + '/Stage_4_' + topic + "_correlation_test"
sentiment_analysis_path = path + '/Stage_5_' + topic + "_sentiment_analysis"
df_and_csv_document_path = path + '/Stage_6_' + topic + "avg_sentiment_analysis"
price_df_and_csv_document_path = path + '/Stage_7_' + topic + "_prices"
combined_seg_and_price_document_path = path + '/Stage_8_' + topic + "_sentiment_analysis_and_prices"


############################################################
# Create Main Directory.
############################################################
def create_main_directory(path):

    logging.info('Create Main Directory:')
    try:
        os.mkdir(path)
    except OSError:
        logging.info("Creation of the directory %s failed" % path)
    else:
        logging.info("Successfully created the directory %s " % path)


############################################################
# Stage 1: Get all the news links for each day.
############################################################
def stage_1(date_links_path, country, topic, start_date, end_date):

    logging.info('STAGE 1/' + num_of_stages + ':')

    try:
        os.mkdir(date_links_path)
    except OSError:
        logging.info("Creation of the directory %s failed" % date_links_path)
    else:
        logging.info("Successfully created the directory %s " % date_links_path)


    # Get date in right order and run news_link() function.
    delta = end_date - start_date
    for i in tqdm(range(delta.days + 1), desc='Creating News Links per day files'):
        date_start = start_date + timedelta(days=i)
        list_date = list(str(date_start).split("-"))
        year = list_date[0]
        month = list_date[1]
        day = list_date[2]
        date_use_format_start = "%" + year + "-%" + month + "-%" + day

        date_next = start_date + timedelta(days=i + 1)
        list_date = list(str(date_next).split("-"))
        year_n = list_date[0]
        month_n = list_date[1]
        day_n = list_date[2]
        date_use_format_next = "%" + year_n + "-%" + month_n + "-%" + day_n

        news_link(date_links_path, country, topic, date_use_format_start, date_use_format_next)


############################################################
# Stage 2: Get news articles.
############################################################
def stage_2(news_articles_path, date_links_path):

    logging.info('STAGE 2/' + num_of_stages + ':')

    try:
        os.mkdir(news_articles_path)
    except OSError:
        logging.info("Creation of the directory %s failed" % news_articles_path)
    else:
        logging.info("Successfully created the directory %s " % news_articles_path)

    for filename in os.listdir(date_links_path):

        # Get link file
        filename.endswith(".csv")

        # Create a directory for each days news articles.
        directory_name = news_articles_path + '/' + filename[0:len(filename)-4] + '_articles'
        try:
            os.mkdir(directory_name)
        except OSError:
            logging.info("Creation of the directory %s failed" % directory_name)
        else:
            logging.info("Successfully created the directory %s " % directory_name)

        # Get news articles.
        ll = get_link_list(date_links_path + '/' + filename)
        article_num = 0
        for link in tqdm(ll, desc = 'Getting articles for ' + filename):
            article_save_name = directory_name + '/article' + str(article_num)
            try:
                get_article(link, article_save_name)
                article_num = article_num + 1
            except:
                logging.debug('Error reading artickle: ' + link)
            # article_num = article_num + 1


############################################################
# Stage 3: Clean news articles.
############################################################
def stage_3(news_articles_path, clean_articles_path ):
    logging.info('STAGE 3/' + num_of_stages + ':')

    try:
        os.mkdir(clean_articles_path)
    except OSError:
        logging.info("Creation of the directory %s failed" % clean_articles_path)
    else:
        logging.info("Successfully created the directory %s " % clean_articles_path)

    for directory in tqdm(os.listdir(news_articles_path), desc= 'Cleaning articles'):

        # Create cleaned directory for that date
        new_cleaned_directory = clean_articles_path + '/' + directory + '_cleaned'
        try:
            os.mkdir(new_cleaned_directory)
        except OSError:
            logging.info("Creation of the directory %s failed" % new_cleaned_directory)
        # else:
        #     logging.info("Successfully created the directory %s " % new_cleaned_directory)

        for filename in os.listdir(news_articles_path + '/' + str(directory)):
            open_file = news_articles_path + '/' + directory + '/' + filename
            save_title = clean_articles_path + '/' + directory + '_cleaned/clean_' + filename
            clean_article(open_file,save_title)

    # More wakeword_data cleaning steps to look into:
    #
    # > tokenization
    # > Stemming / lemmatization
    # > Parts of speech tagging
    # > Create bi - grams or tri - grams
    # > Deal with typos

############################################################
# Stage 4:  Correlation Test.
############################################################
def stage_4(clean_articles_path, correlation_test_path):
    logging.info('STAGE 4/' + num_of_stages + ':')

    try:
        os.mkdir(correlation_test_path)
    except OSError:
        logging.info("Creation of the directory %s failed" % correlation_test_path)
    else:
        logging.info("Successfully created the directory %s " % correlation_test_path)

    # for directory in tqdm(os.listdir(clean_articles_path), desc='Cleaning articles'):


############################################################
# Stage 5: Preform Sentiment analysis on articles.
############################################################
def stage_5(clean_articles_path, sentiment_analysis_path):
    logging.info('STAGE 5/' + num_of_stages + ':')

    try:
        os.mkdir(sentiment_analysis_path)
    except OSError:
        logging.info("Creation of the directory %s failed" % sentiment_analysis_path)
    else:
        logging.info("Successfully created the directory %s " % sentiment_analysis_path)


    for directory in tqdm(os.listdir(clean_articles_path), desc= 'Preform Sentiment analysis on articles'):

        # Create cleaned directory for that date
        new_sentiment_analysis_directory = sentiment_analysis_path + '/' + directory + '_sentiment_analysis'
        try:
            os.mkdir(new_sentiment_analysis_directory)
        except OSError:
            logging.debug("Creation of the directory %s failed" % new_sentiment_analysis_directory)
        # else:
        #     logging.info("Successfully created the directory %s " % new_cleaned_directory)

        data = []
        for filename in os.listdir(clean_articles_path + '/' + str(directory)):
            open_file = clean_articles_path + '/' + directory + '/' + filename
            # save_title = sentiment_analysis_path + '/' + directory + '_sentiment_analysis/sentiment_analysis_' +
            sa = article_sentiment_analysis(open_file)

            # print(save_title)
            data.append({'name': filename[0:len(filename)-4],
                         'neg': sa['neg'],
                         'neu': sa['neu'],
                         'pos': sa['pos'],
                         'compound': sa['compound']
                         })
        df = pd.DataFrame(data, columns=['name', 'neg', 'neu', 'pos', 'compound'])
        save_title = sentiment_analysis_path + '/' + directory + '_sentiment_analysis/sentiment_analysis_clean_article'
        df.to_pickle(save_title + '.pkl')
        df.to_csv(save_title + '.csv')


############################################################
# Stage 6: Build final .csv document.
############################################################
def stage_6(df_and_csv_document_path,sentiment_analysis_path, decimal_round, topic):
    logging.info('STAGE 6/' + num_of_stages + ':')

    try:
        os.mkdir(df_and_csv_document_path)
    except OSError:
        logging.info("Creation of the directory %s failed" % df_and_csv_document_path)
    else:
        logging.info("Successfully created the directory %s " % df_and_csv_document_path)

    final_data = []

    for directory in tqdm(os.listdir(sentiment_analysis_path), desc= 'Building final document'):
        neg_array = []
        neu_array = []
        pos_array = []
        compound_array = []

        f = open(sentiment_analysis_path + "/" + directory +"/sentiment_analysis_clean_article.csv")
        csv_f = csv.reader(f)

        i = 0
        for row in csv_f:
            if i >= 1:
                neg_array.append(float(row[2]))
                neu_array.append(float(row[3]))
                pos_array.append(float(row[4]))
                compound_array.append(float(row[5]))
            i = i + 1

        # Date
        date = directory[0:10]

        # Number of articles
        num_of_articles = len(neg_array)

        if num_of_articles > 0:
            # Average
            neg_average = round(average(neg_array), decimal_round)
            neu_average = round(average(neu_array), decimal_round)
            pos_average = round(average(pos_array), decimal_round)
            compound_average = round(average(compound_array), decimal_round)

            # # Mode
            # neg_mode = round(statistics.mode(neg_array), decimal_round)
            # neu_mode = round(statistics.mode(neu_array), decimal_round)
            # pos_mode = round(statistics.mode(pos_array), decimal_round)
            # compound_mode = round(statistics.mode(compound_array), decimal_round)
        else:
            # Average
            neg_average = 0
            neu_average = 0
            pos_average = 0
            compound_average = 0

            # # Mode
            # neg_mean = 0
            # neu_mean = 0
            # pos_mean = 0
            # compound_mean = 0

        # df['num_of_articles'] = num_of_articles
        # df['neg_average'] = neg_average
        # df['neu_average'] = neu_average
        # df['pos_average'] = pos_average
        # df['compound_average'] = compound_average
        final_data.append({
                     'date': date,
                     'num_of_articles': num_of_articles,
                     'neg_average': neg_average,
                     'neu_average': neu_average,
                     'pos_average': pos_average,
                     'compound_average': compound_average,
                     # 'neg_mode': neg_mode,
                     # 'neu_mode': neu_mode,
                     # 'pos_mode': pos_mode,
                     # 'compound_mode': compound_mode,
                     })
    df = pd.DataFrame(final_data, columns=['date',
                                           'num_of_articles',
                                           'neg_average',
                                           'neu_average',
                                           'pos_average',
                                           'compound_average',
                                           # 'neg_mode',
                                           # 'neu_mode',
                                           # 'pos_mode',
                                           # 'compound_mode'
                                           ])
    df.to_pickle(df_and_csv_document_path + '/' + topic + '_final' + '.pkl')
    df.to_csv(df_and_csv_document_path + '/' + topic + '_final' + '.csv')


############################################################
# Stage 7: Build Price wakeword_data-frame/document.
############################################################
def stage_7( start_date, end_date, API_key, ticker):
    logging.info('STAGE 7/' + num_of_stages + ':')

    try:
        os.mkdir(price_df_and_csv_document_path)
    except OSError:
        logging.info("Creation of the directory %s failed" % price_df_and_csv_document_path)
    else:
        logging.info("Successfully created the directory %s " % price_df_and_csv_document_path)

    delta = end_date - start_date  # as timedelta

    final_crypto_data = [{'currency': ticker, 'timestamps': [], 'prices': []}]

    for i in tqdm(range(delta.days + 1), desc='Building Crypto File'):
        day = start_date + timedelta(days=i)

        url = "https://api.nomics.com/v1/currencies/sparkline?key=" + API_key + "&ids=" + ticker + "&start=" + str(
            day) + "T00%3A00%3A00Z&end=" + str(day) + "T00%3A00%3A00Z&convert=" + str(currency_unit)
        api_data = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))

        date = api_data[0]['timestamps'][0]
        prices = api_data[0]['prices'][0]
        print(date)
        print(prices)
        final_crypto_data[0]['timestamps'].append(date)
        final_crypto_data[0]['prices'].append(prices)



    price_data = {'Date' : final_crypto_data[0]['timestamps']}
    col = ['Date']
    for i in final_crypto_data:
        currency = i['currency']
        timestamp = i['timestamps']
        prices = i['prices']

        price_data[currency] = prices

        col.append(currency)

    df = pd.DataFrame(price_data, columns = col)

    df.to_pickle(price_df_and_csv_document_path + '/' + topic + '_price' + '.pkl')
    df.to_csv(price_df_and_csv_document_path + '/' + topic + '_price' + '.csv')


############################################################
# Stage 8: Combining Sentiment Analysis wakeword_data-frame/document
#          with Price wakeword_data-frame/document.
############################################################
def stage_8( df_and_csv_document_path, price_df_and_csv_document_path):
    logging.info('STAGE 8/' + num_of_stages + ':')

    try:
        os.mkdir(combined_seg_and_price_document_path)
    except OSError:
        logging.info("Creation of the directory %s failed" % combined_seg_and_price_document_path)
    else:
        logging.info("Successfully created the directory %s " % combined_seg_and_price_document_path)

    seg_data = df_and_csv_document_path + '/' + topic + '_final' + '.pkl'

    price_data = price_df_and_csv_document_path + '/' + topic + '_price' + '.pkl'


    seg_object = pd.read_pickle( seg_data)
    price_object = pd.read_pickle(price_data)

    frames = [ price_object, seg_object]

    seg_price_combination = pd.concat(frames, axis=1, join='inner')

    # print(seg_price_combination)

    df = seg_price_combination

    del df['date']
    df.to_pickle(combined_seg_and_price_document_path + '/' + topic + '_combined_seg_and_price' + '.pkl')
    df.to_csv(combined_seg_and_price_document_path + '/' + topic + '_combined_seg_and_price' + '.csv')


# create_main_directory(path)
# stage_1(date_links_path, country, topic, start_date, end_date)
# stage_2(news_articles_path, date_links_path)
# stage_3(news_articles_path, clean_articles_path)
stage_4(clean_articles_path, correlation_test_path )
# stage_5(clean_articles_path, sentiment_analysis_path)
# stage_6(df_and_csv_document_path, sentiment_analysis_path, decimal_round, topic)
# stage_7( start_date, end_date, API_key, ticker)
# stage_8(df_and_csv_document_path, price_df_and_csv_document_path)
