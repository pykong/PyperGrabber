from string import punctuation, whitespace


def rem_whitespace(string):
    """ careful to keep this order of patterns or duplicate whitespace created in first round
    will not be removed
    """
    unwanted_chars = punctuation + whitespace

    pat_l = [r'[' + unwanted_chars + ']',
             r'\s+',
             r'  ',
             r' \\',
             r' \ '
             ]

    for p in pat_l:
        rx = re.compile(p)
        string = re.sub(rx, ' ', string)

    return string.strip()


def encode(ustr):
    return ustr.encode('utf8')
