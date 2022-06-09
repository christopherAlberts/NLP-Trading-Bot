# https://www.youtube.com/watch?v=Ikf6Xdox0Go

import sys
from datetime import time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests
import logger
from newspaper import Config

# topic = 'bitcoin'
# link_24hours = 'https://www.google.com/search?q=' + topic + '&rlz=1C1GCEU_enZA868ZA868&tbs=qdr:d&tbm=nws&sxsrf=ALeKk00oIr5sQSgoul7Zqn91u_FJEPHYZQ:1620330639115&tbas=0&source=lnt&sa=X&ved=0ahUKEwik0aaB6rXwAhUdSxUIHXebDF0QpwUIKQ&biw=1536&bih=722&dpr=1.25'
# # next_page = 2
# document = open(topic + "_links.csv", "a")
# document.write("{},{},{} \n".format('title', 'link', 'description'))
# document.close()


def news_link(link_24hours, name):

    # root = 'https://www.google.com/'
    req = Request(link_24hours, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    with requests.Session() as c:
        soup = BeautifulSoup(webpage, 'html5lib')
        print(soup)

        for item in soup.find_all('div', attrs={'class': 'ZINbbc xpd O9g5cc uUPGi'}):
        # for item in soup.find_all('div', attrs={'class': 'kCrYT'}):
                # print('hi')
                print(item)
                # try:
                #
                #     title = (item.find('div', attrs={'class': 'BNeawe vvjwJb AP7Wnd'}).get_text())
                #     print(title)
                #
                #     raw_link = (item.find('a', href=True)['href'])
                #     link = (raw_link.split("/url?q=")[1]).split('&sa=U&')[0]
                #     print(link)
                #
                #     description = (item.find('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'}).get_text())
                #     print(description)
                #
                #     title = title.replace(',', '')
                #     link = link.replace(',', '')
                #     description = description.replace(',', '')
                #
                #     document = open(name + topic+"_links.csv", "a")
                #     document.write
                #     document.write("{},{},{} \n".format(title, link, description))
                #     document.close()
                #
                #     # One needs to add a delay to avoid a http 429 error
                #     time.sleep(1)
                #
                # except:
                #     print("Unexpected error:", sys.exc_info()[0])

        # next = soup.find('a', attrs={'aria-label':'Next page'})

        # print('Page ' + str(next_page))

        # next = soup.find('a', attrs={'aria-label': 'page 2'})
        # print(next)
        # next_page = next_page + 1

        # next = (next['href'])
        # print(next)
        # link = root + next
        # print("LINK-> " + link)

        # news_link(link)
        # news_link(link, next_page)

# news_link(link_24hours, next_page)
# news_link(link_24hours)
news_link('https://www.google.com/search?q=bitcoin&rlz=1C1GCEU_enZA868ZA868&biw=1920&bih=937&sxsrf=ALeKk03z1MWuT7DEF0C3JAd_wzX3QA-gQw%3A1621367548365&source=lnt&tbs=cdr%3A1%2Ccd_min%3A11%2F1%2F2019%2Ccd_max%3A11%2F1%2F2019&tbm=nws','12_')
# print('##############################################################################################')
# news_link('https://www.google.com/search?q=bitcoin&rlz=1C1GCEU_enZA868ZA868&biw=958&bih=870&sxsrf=ALeKk03bSk-LPzCaslgN1M50Oqob5mNfKA%3A1620916538489&source=lnt&tbs=cdr%3A1%2Ccd_min%3A05%2F13%2F2021%2Ccd_max%3A05%2F13%2F2021&tbm=nws','13_')
# https://www.google.com/search?q=bitcoin&rlz=1C1GCEU_enZA868ZA868&biw=1920&bih=937&sxsrf=ALeKk02hbEfuYM9EUtbe40IFrLmfoasibg%3A1621366965948&source=lnt&tbs=cdr%3A1%2Ccd_min%3A5%2F18%2F2021%2Ccd_max%3A5%2F18%2F2021&tbm=nws

# https://www.google.com/search?q=bitcoin&rlz=1C1GCEU_enZA868ZA868&sxsrf=ALeKk01s2BT3SJD8EkJ6VUo29Y4_sERTkA:1621366962773&source=lnms&tbm=nws&sa=X&ved=2ahUKEwjA6vbO_tPwAhWHbsAKHU_hBiwQ_AUoAXoECAEQAw&biw=1920&bih=937