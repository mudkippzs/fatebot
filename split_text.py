import re
from clogger import clogger


def split_text(text):

    text = text[0]
    text_list = []
    while len(text) > 1000:
        text_list.append(text[:1000])
        text = text[1000:]
    else:
        text_list.append(text)

    return text_list


if __name__ == "__main__":
    pass
