# -*- coding: utf-8 -*-


from urllib import quote_plus
from log_this import log_search, log_download
from string_funcs import encode
from config import *
from get_title import get_title

from easy_parallelize import easy_parallelize
from flatten_list import flatten_list

import urllib2
from time import sleep
from random import uniform
from bs4 import BeautifulSoup

from urlparse import urljoin

import re
import shelve


# EMPTYING PERSISTENT STORAGE OF DOWNLOADED PDFs:
db = shelve.open('download_db.db', writeback=True)
try:
    for key in db:
        del db[key]
finally:
    db.close()


# mini crawler functions:
def check_db(entry):
    db = shelve.open('download_db.db', writeback=True)
    try:
        if entry in db:
            # print '{} found'.format(entry)
            exist = True
        else:
            db[entry] = ''  # putting entry into db
            exist = False
    finally:
        db.close()
    return exist


def get_pdf(pdf_link):

    # check whether value already existing in permanent storage:
    pdf_name = pdf_link.rsplit('/', 1)[-1]  # set filename according to last element of link
    if not check_db(pdf_name) and not check_db(pdf_link):
        # print 'Downloading: {}'.format(pdf_link)
        try:
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', USER_AGENT)]

            r = opener.open(pdf_link)

            path = tmp_dir + pdf_name

            with open(path, "wb") as code:  # 'w'
                code.write(r.read())

            # log successful download:
            log_download('DOWNLOADED: {}'.format(pdf_link))

        except Exception as e:
            log_download('FAILURE: {} | {}'.format(pdf_link, e))
    else:
        log_download('File already downloaded: {}'.format(pdf_name))


def rem_blacklisted(url_l):
    ret_list = []

    whitelist = [r'ncbi.nlm.nih.gov/pmc/articles',
                 r'scholar?cluster ='
                 ]

    blacklist = [r'mailto',  # important to prevent crashes

                 r'nlm.nih.gov',
                 r'pubmed.gov',
                 r'nih.gov',
                 r'dhhs.gov',
                 r'usa.gov',
                 r'youtube.com',
                 r'facebook.com',
                 r'twitter.com',
                 r'sci-hub.cc/donate',
                 r'vk.com',
                 r'google',
                 r'scholar.google',
                 r'.css',
                 r'index.html'
                 ]

    wl_rx = re.compile('.*' + '.*|.*'.join(wl for wl in whitelist) + '.*')
    bl_rx = re.compile('.*' + '.*|.*'.join(bl for bl in blacklist) + '.*')

    for u in url_l:
        # if whitelisted or not blacklisted join to return list
        if re.match(wl_rx, u) or not re.match(bl_rx, u):
            ret_list.append(u)
        else:
            continue

    return ret_list


def get_links(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', USER_AGENT)]

    # print ' get_links working on url: {}'.format(url)

    #  if 'sci-hub.cc' in url:  # workaround for not having captcha solving right now
    #      driver = webdriver.Chrome()
    #      driver.get("http://www.google.com")

    fetch_timeout = 30
    try:
        response = opener.open(url, timeout=fetch_timeout)

        if response:
            soup = BeautifulSoup(response, cr_parser, from_encoding=response.info().getparam('charset'))
            href_l = [urljoin(url, h['href']) for h in soup.find_all(href=True)]
            # print 'href_l 1: ', href_l
            href_l = list(set(href_l))  # removing potential duplicates
            href_l = rem_blacklisted(href_l)  # removing blacklisted
            href_l = map(encode, href_l)  # transforming all potential unicode items to stringm

            pdf_l = [p for p in href_l if p.lower().endswith('.pdf')]  # picking potential pdf links

            # print 'pdf_l: ', pdf_l

            href_l = list(set(href_l) - set(pdf_l))  # removing pdf links from link list
            # print 'href_l 3: ', href_l

            # downloading pdf files:
            map(get_pdf, pdf_l)

            return href_l

    except Exception as e:
        log_download("ERROR in get_links: {}".format(e))
        return []


def mini_crawler(seed_url):
    link_l = [seed_url]  # starting link_l, populating with seed_url
    visited = []
    # print 'link_l in mini_crawler: ', link_l
    max_depths = 2

    for i in range(max_depths):
        if not link_l:
            break
        else:
            go_to = set(link_l) - set(visited)  # preventing visiting site twice
            go_to = list(go_to)
            visited.extend(link_l)

            res_x = easy_parallelize(get_links, go_to)
            link_l = list(set((flatten_list(res_x))))

            # print 'link_l: ', link_l
        sleep(uniform(1.3, 4.7))  # small randomized pause to be easy on servers
    log_download('CRAWLER FINISHED working on seed: {}'.format(seed_url))


# --------------------------------------------------------------------------------------
'''    MAIN FUNCTION    '''


def retriever(pmid):
    # print 'threader received data: ', data
    log_search('SEARCHING: {}'.format(pmid))

    # retrievingpaper title via pubmed API:
    title = get_title(pmid, email)

    seed_links = []  # seed links, populated with data

    ncbi_url = pubmed_base_url + pmid
    scihub_url = scihub_base_url + pmid
    seed_links.extend([ncbi_url, scihub_url])

    if title:
        scho_tit = quote_plus(title)
        gosch_url = schola_base_url.format(scho_tit)
        seed_links.append(gosch_url)

    # print 'seed_links: ', seed_links
    # via iteration:
    for seed in seed_links:
        mini_crawler(seed)



