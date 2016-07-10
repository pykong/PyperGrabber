#!/usr/bin/env python

import subprocess


def pdf_print(pmid, save_dir):
    link = 'https://www.ncbi.nlm.nih.gov/pubmed/' + pmid

    filename = save_dir + pmid + '.pdf'

    # number of trials:
    trials = 7
    for trial in range(1, trials):
        try:
            cmd = 'wkhtmltopdf --quiet --page-size A4 '
            subprocess.call([cmd + link + ' ' + filename], shell=True)  # executing wkhtmltopdf command
        except IOError:
            print 'Problem with wkhtmltopdf. Trying again'
            



