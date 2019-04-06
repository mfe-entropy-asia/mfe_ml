import pickle
import string
from collections import Counter
import numpy as np
from nltk import ngrams
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import pandas as pd

class FreqToken:
    def __init__(self, cleaned_news, top=5000):
        self.cleaned_news = cleaned_news
        self.translator = str.maketrans('', '', string.punctuation)  # To get rid of the punctuations
        self.frequent_grams = {}
        self.top = top

    def __call__(self):
        for date in self.cleaned_news.keys():
            print("processing: %s" % pd.to_datetime(str(date)).strftime('%Y-%m-%d'))
            sen_tokens = []
            for content in self.cleaned_news[date]:
                for sentence in sent_tokenize(content):
                    sen_tokens += [word_tokenize(sentence.translate(self.translator))]
            flat_tokens = []
            for tokens in sen_tokens:
                flat_tokens += list(ngrams(tokens, 4))
            today_frequent_tokens = self.take_frequent_tokens(flat_tokens)
            self.frequent_grams[np.datetime64(date)] = today_frequent_tokens

    def take_frequent_tokens(self, flat_tokens):
        today_frequent_tokens = {}
        counter = Counter(flat_tokens)
        top_tokens = counter.most_common(self.top)
        for pair in top_tokens:
            if pair[1] > 1:
                today_frequent_tokens[pair[0]] = pair[1]
        return today_frequent_tokens
        # self.frequent_tokens = list(list(zip(*top_tokens))[0])


def run():
    pickle_in = open("../../data/intermediate/1_cleaned.pickle", "rb")
    cleaned_news = pickle.load(pickle_in)
    pickle_in.close()
    freToken = FreqToken(cleaned_news)
    freToken()
    # {Timestamp('2018-06-08 00:00:00'): {('0', '0', '0', '0'): 439, ('shares', 'on', 'buy', 'side'): 172,
    pickle_out = open("../../data/intermediate/3_freq_grams.pickle", "wb")
    pickle.dump(freToken.frequent_grams, pickle_out)
    pickle_out.close()


if __name__ == '__main__':
    run()
