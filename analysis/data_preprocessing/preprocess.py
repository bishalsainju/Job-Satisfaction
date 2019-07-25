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


stopwords = open(root_path + "/data/static/preprocessing/stopwords", mode='r', encoding='utf8').\
        read().splitlines()
more_stopwords = ['apple', 'amazon', 'job', 'company']
stopwords.extend(more_stopwords)
stopwords2 = open(root_path + "/data/static/stopwords.txt", mode='r', encoding='utf8').\
    read().splitlines()
stopwords.extend(stopwords2)
stopwords = sorted(stopwords)


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

def is_useful_ngram(ngrams, ngram):
    """
    Returns True if the bigram is in thesorted list of bigrams else False
    """
    return in_sorted_list(ngrams, ngram)


def generate_ngrams(text, ngram=1, save_filename=root_path + '/data/static/preprocessing/useful_ngrams.txt',
                    read_percent=1, ngram_total = 100, count_store=False, sort=False, save_file=False):
    text = text.lower()
    text = text[:int(len(text) * read_percent)]
    text = clean_data(text)

    words = word_tokenize(text)
    words = [word for word in words if not is_stopwords(stopwords, word)]
    words = [stemmer.stem(word) for word in words]

    if(ngram==1):
        unigrams_counter = Counter(words).most_common(int(ngram_total))
        n_grams = []
        for unigram, count in unigrams_counter:
            if not count_store:
                n_grams.append(unigram)
            else:
                n_grams.append(str(f'({unigram}, {count})'))
    elif(ngram==2):
        bigrams = nltk.bigrams(words)
        bigrams = ["_".join(bigram) for bigram in bigrams]
        bigrams_counter = Counter(bigrams).most_common(int(ngram_total))
        n_grams = []
        for bigram, count in bigrams_counter:
            a, b = bigram.split("_")
            if not (is_stopwords(stopwords, a) or is_stopwords(stopwords, b)):
                if not count_store:
                    n_grams.append(bigram)
                else:
                    n_grams.append(str(f'({bigram}, {count})'))
    elif(ngram==3):
        trigrams = nltk.trigrams(words)
        trigrams = ["_".join(trigram) for trigram in trigrams]
        trigrams_counter = Counter(trigrams).most_common(int(ngram_total))
        n_grams = []
        for trigram, count in trigrams_counter:
            a, b, c = trigram.split("_")
            if not (is_stopwords(stopwords, a) or is_stopwords(stopwords, b)):
                if not count_store:
                    n_grams.append(trigram)
                else:
                    n_grams.append(str(f'({trigram}, {count})'))

    if sort:
        n_grams = sorted(n_grams)

    if save_file:
        with open(save_filename, mode='w', encoding='utf8') as file:
            file.write("\n".join(n_grams))

    return n_grams


def data_preprocess_company(company_index, sentences):
    unigram_company = generate_ngrams()
    processed_sentences = []
    for sentence in sentences:
        sent_grams = []
        unigrams = generate_ngrams(sentence, ngram=1, sorted=True)
        unigrams = [unigram for unigram in unigrams if is_useful]
        bigrams = generate_ngrams(sentence, ngram=2, sorted=True)
        trigrams = generate_ngrams(sentence, ngram=3, sorted=True)
        sent_grams.extend(unigrams)
        sent_grams.extend(bigrams)
        sent_grams.extend(trigrams)
        bigrams = [bigram for bigram in bigrams if is_useful_bigram(self.useful_bigrams, bigram)]
        sentence += bigrams

        sentence = " ".join(sentence)
        processed_sentences.append(sentence)

    return processed_sentences


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


# if __name__ == '__main__':
    # text = "My name is Bishal Sainju"
    # text = open(root_path + "/data/static/preprocessing/corpus.txt", mode='r', encoding='utf8')\
    #     .read().lower()\
    #     .replace('\n', ' ')
    # print(generate_trigrams("My name is Bishal Sainju. I love dancing and singing.", read_percent=1, trigram_total=100))
    # pp = Preprocess(bigrams=True)
    # print(pp.preprocess(['My name is Bishal Sainju peace', 'I love playing and dancing']))

if __name__ == '__main__':
    # generate_ngrams(text, ngram=1, save_filename=root_path + '/data/static/preprocessing/useful_ngrams.txt',
    #                 read_percent=1, ngram_total=100, count_store=False, sorted=False, save_file=False)
    print(generate_ngrams("My name is Bishal Sainju. I love dancing and singing.", ngram=1, read_percent=1, sort=True))