import re
import string


def remove_url(text):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', text)


def remove_at(text):
    return re.sub('@[^\s]+', '', text)


def remove_hash(text):
    return text.replace("#", "")


def remove_punct(text):
    return text.translate(str.maketrans('', '', string.punctuation))


def remove_letter_repitition(text):
    return re.sub(r'(.)\1+', r'\1\1', text)


def clean_data(text):
    text = text.lower()
    text = remove_url(text)
    text = remove_at(text)
    text = remove_hash(text)
    text = remove_punct(text)
    text = remove_letter_repitition(text)
    return text


if __name__ == '__main__':
    print(clean_data("yaaaaay"))
