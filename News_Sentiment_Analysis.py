from PythonProjects.NLP_Trading_Bot.NLP_methods import *

# The following code will log "INFO" to the console.
# ---------------------------------------------------------------------------------------------------
logging.basicConfig( level=logging.INFO, format='%(asctime)s: line:%(lineno)d: %(levelname)s: %(message)s')
# ---------------------------------------------------------------------------------------------------

topic = 'bitcoin'
start_date = date(2021, 5, 12)
end_date = date(2021,5, 13)
now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Define the name of the directories to be created
path = str(now + '_' + topic)
date_links_path = path + '/' + topic + "_date_links"

############################################################
# Create Main Directory.
############################################################
def create_main_directory():

    logging.info('Create Main Directory:')
    try:
        os.mkdir(path)
    except OSError:
        logging.info("Creation of the directory %s failed" % path)
    else:
        logging.info("Successfully created the directory %s " % path)

    # document = open(path + '/' + topic + "_date_links.csv", "a")
    # document.write("{},{}\n".format('date', 'link'))
    # document.close()

############################################################
# Stage 1: Get date page links.
############################################################

def stage_1():

    logging.info('STAGE 1:')

    try:
        os.mkdir(date_links_path)
    except OSError:
        logging.info("Creation of the directory %s failed" % date_links_path)
    else:
        logging.info("Successfully created the directory %s " % date_links_path)

    document = open(date_links_path + '/' + topic + "_date_links.csv", "a")
    document.write("{},{}\n".format('date', 'link'))
    document.close()

    document = open(date_links_path + "/" + topic + "_date_links.csv", "a")
    delta = end_date - start_date

    for i in tqdm(range(delta.days + 1), desc='Creating Date Page Links'):

        date = start_date + timedelta(days=i)
        list_date = list(str(date).split("-"))
        year = list_date[0]
        month = list_date[1]
        day = list_date[2]
        link = 'https://www.google.com/search?q=' + topic + '&rlz=1C1GCEU_enZA868ZA868&biw=958&bih=870&sxsrf=ALeKk03bSk-LPzCaslgN1M50Oqob5mNfKA%3A1620916538489&source=lnt&tbs=cdr%3A1%2Ccd_min%3A'+ month + '%2F' + day + '%2F' + year + '%2Ccd_max%3A' + month + '%2F' + day + '%2F' + year + '&tbm=nws'
        document.write("{},{}\n".format(date, link))

    document.close()

############################################################
# Stage 2: Get all the news links for each day.
############################################################

def stage_2():

    logging.info('STAGE 2:')
    # Create news_links_per_day Directory
    links_per_day_directory_path = path + '/' + topic +  '_news_links_per_day'
    try:
        os.mkdir(links_per_day_directory_path)
    except OSError:
        logging.info("Creation of the directory %s failed" % links_per_day_directory_path)
    else:
        logging.info("Successfully created the directory %s " % links_per_day_directory_path)

    # Read date links out of file and add .csv doc containing the day's news_links_per_day
    with open(date_links_path + '/' + topic + "_date_links.csv", 'r') as csvfile:

        datareader = csv.reader(csvfile,delimiter=',')
        num_of_rows = len(list(datareader))
        df = pd.read_csv(date_links_path + '/' + topic + "_date_links.csv")

        for i in tqdm(range(num_of_rows-1), desc = 'Creating News Links per day files'):

            # if (row[1] != 'link'):
            # print(df.iloc[i]['link'])
            # print(df.iloc[i]['date'])
            news_link(topic, df.iloc[i]['link'],links_per_day_directory_path,df.iloc[i]['date'])


create_main_directory()  # Create Main Directory.
stage_1()  # Get date page links.
stage_2()  # Get all the news links for each day.
