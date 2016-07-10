from ConfigParser import SafeConfigParser
from os.path import expanduser
import getpass

parser = SafeConfigParser()
parser.read('config.ini')

VERSION = parser.get('general', 'version')

# email access:
em_server = parser.get('email_auth', 'em_server')
em_usr = parser.get('email_auth', 'em_usr')
em_pw = parser.get('email_auth', 'em_pw')
sender = parser.get('email_auth', 'sender')

# prompting for email user name and password in case not provided by config.ini
if len(em_usr) == 0:
    em_usr = getpass.getpass(prompt='Input username for email account: ')
if len(em_pw) == 0:
    em_pw = getpass.getpass()



# most common user agent according to: https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
USER_AGENT = parser.get('crawler', 'usr_agent')
email = parser.get('crawler', 'email')
cr_parser = parser.get('crawler', 'cr_parser')
pubmed_base_url = parser.get('crawler', 'pubmed_base_url')
scihub_base_url = parser.get('crawler', 'scihub_base_url')
schola_base_url = parser.get('crawler', 'schola_base_url')

# dir to save files to:
home = expanduser("~")
save_dir = home + parser.get('paths', 'save_to')
tmp_dir = save_dir + '.tmp/'  # hidden
