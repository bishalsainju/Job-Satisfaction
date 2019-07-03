from collections import Counter
import os
from bisect import bisect_left
from analysis.data_preprocessing.data_clean import clean_data
import config.config as config

import nltk
from nltk import WordPunctTokenizer, PunktSentenceTokenizer, PorterStemmer
from nltk.tokenize import word_tokenize

sent_tokenizer = PunktSentenceTokenizer()
word_tokenizer = WordPunctTokenizer()
stemmer = PorterStemmer()

config = config.Config()
root_path = config.project_root


def in_sorted_list(lists, item):
    """
    Returns True if the item is in thesorted list else False
    """
    index = bisect_left(lists, item)
    if lists[min(index, len(lists) - 1)] == item:
        return True
    else:
        return False


def is_stopwords(stopwords, word):
    """
    Returns True if the word is in thesorted list of stopwords else False
    """
    return in_sorted_list(stopwords, word)

# print(is_stopwords(['a', 'b'], 'a'))
def is_useful_bigram(bigrams, bigram):
    """
    Returns True if the bigram is in thesorted list of bigrams else False
    """
    return in_sorted_list(bigrams, bigram)

def generate_unigrams(text, save_filename=root_path + '/data/static/preprocessing/useful_bigrams.txt',\
                        read_percent=1, unigram_total=100, count_store = False):
    stopwords = open(root_path + "/data/static/preprocessing/stopwords", mode='r', encoding='utf8'). \
        read().splitlines()
    stopwords.append('apple')
    stopwords2 = open(root_path + "/data/static/stopwords.txt", mode='r', encoding='utf8').\
        read().splitlines()
    stopwords.extend(stopwords2)
    stopwords = sorted(stopwords)
    assert is_stopwords(stopwords, "yourselves")

    text = text.lower()
    text = text[:int(len(text) * read_percent)]
    text = clean_data(text)

    words = word_tokenize(text)
    words = [word for word in words if not is_stopwords(stopwords, word)]
    words = [stemmer.stem(word) for word in words]

    if count_store:
        unigram = Counter(words).most_common(int(unigram_total))
    else:
        unigram = words

    unigram = [str(uni) for uni in unigram]

    with open(save_filename, mode='w', encoding='utf8') as file:
        file.write("\n".join(unigram))

    return unigram


def generate_bigrams(text, save_filename=root_path + '/data/static/preprocessing/useful_bigrams.txt',\
                        read_percent=1, bigram_total=100, count_store = False):
    """
    Given text, generate pairs of useful bigrams
    :returns : list of useful bigrams
    >> [a_b, c_d, ]
    """
    stopwords = open(root_path + "/data/static/preprocessing/stopwords", mode='r', encoding='utf8').\
        read().splitlines()
    stopwords.append('apple')
    stopwords2 = open(root_path + "/data/static/stopwords.txt", mode='r', encoding='utf8').\
        read().splitlines()
    stopwords.extend(stopwords2)
    stopwords = sorted(stopwords)
    assert is_stopwords(stopwords, "yourselves")

    text = text.lower()
    text = text[:int(len(text) * read_percent)]
    text = clean_data(text)

    words = word_tokenize(text)
    words = [word for word in words if not is_stopwords(stopwords, word)]
    # print(len(words), " words")
    # print(words)

    words = [stemmer.stem(word) for word in words]

    bigrams = nltk.bigrams(words)
    bigrams = ["_".join(bigram) for bigram in bigrams]
    # print(bigrams)

    # print("Filtering from {} bigrams".format(len(bigrams)))
    bigrams_counter = Counter(bigrams).most_common(int(bigram_total))
    # print(bigrams_counter)

    useful_bigrams = []
    for bigram, count in bigrams_counter:
        # print(bigram)
        a, b = bigram.split("_")
        if not (is_stopwords(stopwords, a) or is_stopwords(stopwords, b)):
            if not count_store:
                useful_bigrams.append(bigram)
            else:
                useful_bigrams.append(str(f'({bigram}, {count})'))

    # print("Selected a total of {} bigrams".format(len(useful_bigrams)))

    # useful_bigrams = sorted(useful_bigrams)
    with open(save_filename, mode='w', encoding='utf8') as file:
        file.write("\n".join(useful_bigrams))

    return useful_bigrams


def generate_trigrams(text, save_filename=root_path + '/data/static/preprocessing/useful_trigrams.txt', \
                      read_percent=1, trigram_total=100, count_store = False):
    """
    Given text, generate pairs of useful bigrams
    :returns : list of useful bigrams
    >> [a_b, c_d, ]
    """
    stopwords = open(root_path + "/data/static/preprocessing/stopwords", mode='r', encoding='utf8').\
        read().splitlines()
    stopwords.append('apple')
    stopwords2 = open(root_path + "/data/static/stopwords.txt", mode='r', encoding='utf8').\
        read().splitlines()
    stopwords.extend(stopwords2)
    stopwords = sorted(stopwords)
    assert is_stopwords(stopwords, "yourselves")

    text = text.lower()
    text = text[:int(len(text) * read_percent)]
    text = clean_data(text)

    words = word_tokenize(text)
    words = [word for word in words if not is_stopwords(stopwords, word)]
    # print(len(words), " words")
    # print(words)

    words = [stemmer.stem(word) for word in words]

    trigrams = nltk.trigrams(words)
    trigrams = ["_".join(trigram) for trigram in trigrams]

    trigrams_counter = Counter(trigrams).most_common(int(trigram_total))

    useful_trigrams = []
    for trigram, count in trigrams_counter:
        # print(bigram)
        a, b, c = trigram.split("_")
        if not (is_stopwords(stopwords, a) or is_stopwords(stopwords, b)):
            if not count_store:
                useful_trigrams.append(trigram)
            else:
                useful_trigrams.append(str(f'({trigram}, {count})'))

    with open(save_filename, mode='w', encoding='utf8') as file:
        file.write("\n".join(useful_trigrams))

    return useful_trigrams


class Preprocess:
    def __init__(self, bigram_filename=root_path + "/data/static/preprocessing/useful_bigrams.txt",
                 bigrams=False, vocab_size=None, remove_stopwords=True):
        self.bigram_filename = bigram_filename
        self.vocab_size = vocab_size
        self.bigrams = bigrams
        self.stopwords = open(root_path + "/data/static/preprocessing/stopwords", mode='r', encoding='utf8').readlines()
        self.remove_stopwords = remove_stopwords

        self.useful_bigrams = []
        if os.path.exists(bigram_filename):
            self.useful_bigrams = open(bigram_filename, mode='r', encoding='utf8').read().splitlines()
            self.useful_bigrams = sorted(self.useful_bigrams)

    def build_vocab(self, text, stem=True):
        """
        :param vocab_size : size of vocabulary to consider other words will be replaced with UNK
            total_vocab_size = vocab_size + 1
            vocab_size of -1 means consider all the words
        :param text : text from which to build vocabulary
        type string
        """
        text = text.lower()
        self.words = word_tokenizer.tokenize(text)

        all_vocab = set(self.words)

        if stem:
            lemmatized_vocab = [stemmer.stem(word) for word in all_vocab]
            self.lemmatized_dict = dict(zip(all_vocab, lemmatized_vocab))
            self.words = [self.lemmatized_dict[word] for word in self.words]

        word_counter = Counter(self.words)

        vocab_size = self.vocab_size
        if not self.vocab_size:
            vocab_size = len(word_counter)
        vocab = word_counter.most_common(vocab_size)

        self.vocab = set([word for word, count in vocab])

    def preprocess(self, sentences):
        """
        :param bigrams: True or False. Should bigrams be generated or not?
        :param bigram_filename: filename containing the useful bigrams to consider
        :return: vocab, X, Y, label
        Steps:
            Split into sentences
            Split sentence into words
            Remove stopwords and lemmatize / stem words
            Generate ngrams
        "I need my credit card." -> "I need my credit card credit_card"
        """
        processed_sentences = []
        for sentence in sentences:
            sentence = word_tokenizer.tokenize(sentence)
            sentence = [word for word in sentence if not is_stopwords(self.stopwords, word)]

            sentence = [stemmer.stem(word) for word in sentence]

            if self.vocab_size:
                sentence = [word if word in self.vocab else 'unk' for word in sentence]

            if self.bigrams:
                bigrams = list(nltk.bigrams(sentence))
                bigrams = ["_".join(bigram) for bigram in bigrams]
                bigrams = [bigram for bigram in bigrams if is_useful_bigram(self.useful_bigrams, bigram)]
                sentence += bigrams

            sentence = " ".join(sentence)
            processed_sentences.append(sentence)

        return processed_sentences


if __name__ == '__main__':
    # text = "My name is Bishal Sainju"
    # text = open(root_path + "/data/static/preprocessing/corpus.txt", mode='r', encoding='utf8')\
    #     .read().lower()\
    #     .replace('\n', ' ')
    print(generate_trigrams("My name is Bishal Sainju. I love dancing and singing.", read_percent=1, trigram_total=100))
    # pp = Preprocess(bigrams=True)
    # print(pp.preprocess(['My name is Bishal Sainju peace', 'I love playing and dancing']))
