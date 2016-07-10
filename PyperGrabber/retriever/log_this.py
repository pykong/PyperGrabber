import logging


# logging functions:
def log_search(msg):
    # print msg
    log_filename = 'search.log'
    logging.basicConfig(filename=log_filename,
                         level=logging.INFO,
                         format='%(asctime)s %(message)s'
                         )
    logging.info(' - ' + msg)


def log_download(msg):
    # print msg
    LOG_FILENAME = 'download.log'
    logging.basicConfig(filename=LOG_FILENAME,
                         level=logging.INFO,
                         format='%(asctime)s %(message)s'
                         )
    logging.info(' - ' + msg)
