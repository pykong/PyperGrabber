#!/usr/bin/env python

from imbox import Imbox
from config import *
import re
import sys


pmids = []
msgs_l = []


def mail2pmid():
    imbox = Imbox(em_server, username=em_usr, password=em_pw)

    print '\n\nFetching emails ...',
    email_gen = (imbox.messages(sent_from=sender))
    while True:    
        try:
            msgs_l.append(email_gen.next())
        except StopIteration:
            break
        except Exception as e:
            print(e)
            sys.exit(1)

    print("Done.\nSuccessfully retrieved {} messages from NCBI.".format(len(msgs_l)))
    
    msgs_str = str(msgs_l)

    pat = re.compile(r'pubmed\/(?P<pmid>\d+)')

    pmids = re.findall(pat, msgs_str)

    pmids = list(set(pmids))

    print('Found {} unique PMIDs.\n'.format(len(pmids)))

    return pmids