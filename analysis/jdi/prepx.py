from config import config
from analysis.data_preprocessing.preprocess import generate_ngrams
import pandas as pd

# Configuring the data path
config = config.Config()
data_path = config.data_path + "/jdi/"


jdi = ['work', 'pay', 'coworkers', 'promotion', 'supervision']
jdi_corpus = []
for i in jdi:
    # Open the text file
    with open(data_path+f"{i}.txt") as f:
        text = f.read()


    # Convert into unique words list
    word_list = []
    for texts in text.splitlines():
        for text in texts.split(","):
            word_list.append(text.strip())
    word_list = list(set(word_list))

    row = [i]
    corpus = []
    for words in word_list:
        corpus.extend(generate_ngrams(words, ngram=1, sort=True))
        corpus.extend(generate_ngrams(words, ngram=2, sort=True))
        corpus.extend(generate_ngrams(words, ngram=3, sort=True))
    row.append(corpus)
    jdi_corpus.append(row)


df = pd.DataFrame(jdi_corpus,
                  columns=["JDI", "Corpus"])

df.to_csv(data_path+"corpus.csv", index=False)