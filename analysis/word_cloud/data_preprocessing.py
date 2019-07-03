import re
import os


def processStatus(status):
    # process the status
    # Convert to lower case
    status = status.lower()
    status = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', '', status)
    status = re.sub('@[^\s]+', 'AT_USER', status)
    status = re.sub('[\s]+', ' ', status)
    status = status.strip('\'"')
    return status

stopWords = []

def replaceTwoOrMore(s):
    # look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

def getStopWordList(stopWordListFileName):
    # read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords

def getFeatureVector(status, stopWords):
    featureVector = {}
    # split status into words
    words = status.split()
    for w in words:
        # replace two or more with two ocurrences
        w = replaceTwoOrMore(w)
        # strip punctuation
        w = w.strip('\'"?,.')
        # check if the word starts with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        # ignore if it is a stop word
        if (w in stopWords or val is None):
            continue
        else:
            w = w.lower()
            if w in featureVector:
                featureVector[w] += 1
            else:
                featureVector[w] = 1
    return featureVector

home = os.path.expanduser("~")
stopwords = getStopWordList(os.path.join(home, 'Desktop/workspace/glassdoor/indeed/data/static/stopwords.txt'))
print(getFeatureVector("I am lonely as fuck. @yellow. Woooooow", stopWords))