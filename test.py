# Topic Modeling: Latent Dirichlet Allocation (LDA)
from PythonProjects.NLP_Trading_Bot.NLP_methods import *
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from gensim import matutils, models
import scipy.sparse

# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

name = 'article_0'
article = 'text.txt'

save_name = "dtm.pkl"
def txt_doc_to_Document_Term_Matric(article, save_name):
    # Get article
    with open(article, 'r') as f:
        clean_text = f.read()
        f.close()

    # Document-Term Matrix - word counts in matrix format
    cv = CountVectorizer(stop_words='english')
    data_cv = cv.fit_transform([clean_text])
    data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
    # data_dtm.index = dict[name].index
    data_dtm.to_pickle(save_name)


def Latent_Dirichlet_Allocation(document_tem_matrix, num_of_topics, num_of_iterations):
    # Topic Modeling: Latent Dirichlet Allocation (LDA)
    data = pd.read_pickle(document_tem_matrix)
    # print(wakeword_data)

    # One of the required inputs is a term-document matrix
    tdm = data.transpose()
    # print(tdm.head())
    
    # We're going to put the term-document matrix into a new gensim format, from df
    sparse_counts = scipy.sparse.csr_matrix(tdm)
    corpus = matutils.Sparse2Corpus(sparse_counts)

    # Re-add the additional stop words since we are recreating the document-term matrix
    # add_stop_words = ['like', 'im', 'know', 'just', 'dont', 'thats', 'right', 'people',
    #                   'youre', 'got', 'gonna', 'time', 'think', 'yeah', 'said']
    # stop_words = corpus.ENGLISH_STOP_WORDS.union(add_stop_words)

    # # Gensim also requires dictionary of the all terms and their respective location in the term-document matrix
    # cv = CountVectorizer(stop_words=stop_words, min_df=2)
    # pickle.dump(cv, open("cv_stop.pkl", "wb"))

    cv = pickle.load(open("cv_stop.pkl", "rb"))
    id2word = dict((v, k) for k, v in cv.vocabulary_.items())
    
    # Now that we have the corpus (term-document matrix) and id2word (dictionary of location: term),
    # we need to specify two other parameters as well - the number of topics and the number of passes
    lda = models.LdaModel(corpus=corpus, id2word=id2word, num_topics=num_of_topics, passes=num_of_iterations)
    lda.print_topics()

Latent_Dirichlet_Allocation('dtm.pkl', 3, 10)