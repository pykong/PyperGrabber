#!/usr/bin/env python

""" https://github.com/martinrusev/imbox
https://www.rz.ruhr-uni-bochum.de/mitteilungen/faqs/mail-konfiguration.html
https://stackoverflow.com/questions/364802/generator-comprehension
"""

import sys
from mail2pmid.mail2pmid import mail2pmid
from retriever.retriever import retriever
from config import VERSION, save_dir, tmp_dir
import os


import subprocess
import shutil
import time

from retriever.web2pdf import pdf_print
import datetime

import glob
from pyPdf import PdfFileReader


# CHANGING TERMINAL TITLE
sys.stdout.write("\x1b]2;" + 'PyperGrabber v{}'.format(VERSION) + "\x07")

# check if folder path is already in use as it would cause trouble:
if os.path.exists(tmp_dir):
    # try saving remnant files by moving to lost and found folder
    new_dir = save_dir + 'lost_and_found/'
    files = os.listdir(tmp_dir)
    for f in files:
        try:
            shutil.move(f, new_dir)
        except Exception as e:
            print e
    # removing tmp_dir:
    shutil.rmtree(tmp_dir)


# retrieve pubmed's emails and extract PMID's from them
pmids = mail2pmid()

# counter variables for statistics
abstracts = 0
full_article = 0

# retrieve paper:
to = time.time()
num_digits = len(str(len(pmids)))  # dynamically calculate leading zeros
for i, pmid in enumerate(pmids):
    print "Fetching paper {number:0{wd}d} of {tot} with PMID: {id} ...".\
        format(wd=num_digits, number=i, tot=len(pmids), id=pmid),
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    retriever(pmid)

    content = os.listdir(tmp_dir)
    if not content:  # if dir empty make pdf of pubmed abstract:
        pdf_print(pmid, save_dir)
        abstracts += 1
    else:  # if files exist rename them to PMID_i.pdf and move them one path level up
        pdfs = glob.glob(tmp_dir + '*.pdf')
        for pi, pdf in enumerate(pdfs):
            if pi == 0:
                index = ''
            else:
                index = '_{}'.format(pi+1)
            new_path = save_dir + pmid + index + '.pdf'
            os.rename(pdf, new_path)
        full_article += 1

    print "DONE."

# eliminate any duplicate files and left over empty dirs:
fd_cmd = "fdupes -rdN {} && find . -type d -empty -delete ".format(save_dir)  # test manually to check if working
subprocess.call([fd_cmd], shell=True)
# removing pdf files failing integrity check, e.g. HTML files in disguise#:
all_pdfs = glob.glob(save_dir + '*.pdf')
for candidate in all_pdfs:
    try:
         mypdf = PdfFileReader(file( 'filename', 'rb'))
    except:
         print candidate,' is invalid pdf'
         shutil.rmtree(candidate)


# finally removing tmp_dir:
# shutil.rmtree(tmp_dir)

# printing out concluding statistics:
total_time = (time.time() - to)/60
format_time = datetime.timedelta(seconds=total_time)  # format to hh:mm:ss format
print("Job took {0:0.0f} minutes to complete".format(format_time))
total_down = abstracts + full_article
avg_time = datetime.timedelta(seconds=total_time/total_down)
print("Average time to retrieve paper: {}".format(avg_time))
print('Abstracts are {} of total fetches: {}'.format(abstracts, total_down))


with open('time.txt', 'w') as out_f:
    out_f.write(format_time)
