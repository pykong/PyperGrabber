# PyperGrabber
Fetches PubMed article IDs (PMIDs) from email inbox, then crawls PubMed, Google Scholar and Sci-Hub for respective PDF files.

PubMed can send you regular update on new articles matching your specified search criteria.

PyperGrabber will automatically download thoe papers, saving you much time tracking on downloading those manually.

Required dependencies:



NOTE:
- Messy code ahead! 
- Program may halt without error message. The source of this bug is yet to be determined.
- The web crawler function may be used to work with other sources of PMIDs then email (e.g. command line parameter  or file holding list of PMIDs)
