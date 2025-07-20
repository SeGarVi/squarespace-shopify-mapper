import unicodedata

def remove_accents(text):
    if text is None:
        text = ""
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

def proper_case(s=""):
    if s is None:
        s = ""
    return ' '.join(word.capitalize() for word in s.split())