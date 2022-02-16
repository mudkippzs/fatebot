import re

def split_text(text):
    """
    Split a long string into a list.
    len() of each list element should be equal or less than 500 and only split on the end of a sentence.
    """
    text = text.replace('\n', ' ')

    # remove multiple spaces
    text = re.sub(r' +', ' ', text)

    # split on period, comma, question mark and exclamation mark
    sentences = re.split(r'[\.\?!]', text)

    # remove empty strings ('') from the list
    sentences = [s for s in sentences if s != '']

    return ". ".join(sentences) + "."

if __name__ == "__main__":
    pass