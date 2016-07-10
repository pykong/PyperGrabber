from Bio import Entrez
from string_funcs import rem_whitespace


# get title by polling NVBI with PMID as input
def get_title(query, email):
    Entrez.email = email  # Always tell NCBI who you are

    try:
        esear_handle = Entrez.esearch(db="pubmed",
                                      sort='relevance',
                                      retmax='1',
                                      retmode='xml',
                                      term=query
                                      )
        r1 = Entrez.read(esear_handle)
        # print 'results1: ', r1

        if int(r1['Count']) >= 1:
            list = r1["IdList"]

            for index in range(0, len(list)):
                listid = list[index]

                esum_handle = Entrez.esummary(db="pubmed",
                                              sort='relevance',
                                              retmax='1',
                                              retmode='xml',
                                              id=listid
                                              )
                r2 = Entrez.read(esum_handle)
                ''' generates dic entry in the form: {'PMID':'title'},
                (duplicate, leading, trailing) whitespaces are removed
                '''

                try:
                    title = "'{}'".format(rem_whitespace(r2[0]['Title']))
                except:
                    title = None

                return title

        else:
            return None

    except:
        # in case of server error try to redo it by recursion:
        get_title(query, email)