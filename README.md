# PyperGrabber
Fetches PubMed article IDs (PMIDs) from email inbox, then crawls PubMed, Google Scholar and Sci-Hub for respective PDF files.


PubMed can send you regular update on new articles matching your specified search criteria. PyperGrabber will automatically download thoe papers, saving you much time tracking on downloading those manually. When no PDF article is found PyperGrabber will save the PubMed abstract of the respective article to PDF. All files are named after PMID for convenience.


NOTES:
- Messy code ahead! 
- Program may halt without error message. The source of this bug is yet to be determined.
- The web crawler function may be used to work with other sources of PMIDs then email (e.g. command line parameter  or file holding list of PMIDs)


Required dependencies:
sudo apt-get install wkhtmltopdf

sudo pip install pypdf

How to start:
- put in your email access data into congig.ini or prepare to be prompted (works with IMAP)
- start with: python ./PyperGrabber.py
