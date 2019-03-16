import numpy as np
from data_cleaner import DataCleaner
from nltk.util import ngrams
# from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
# from nltk.util import pad_sequence
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
import string
# from nltk import Text
translator = str.maketrans('', '', string.punctuation)  # To get rid of the punctuations
dat_clean = DataCleaner("en", ["./data/raw/News.RTRS.201806.0214.txt"], "./data/intermediate/")
dat_clean()

text = []
for i in range(3):
    for body in dat_clean.m_dict[np.datetime64('2018-06-01')+i]:
        # if body != '':
        text += [word_tokenize(sentence.translate(translator)) for sentence in sent_tokenize(body)]

date = np.datetime64('2018-06-01') + 4
present_day_text = []
for body in dat_clean.m_dict[date]:
    present_day_text += [word_tokenize(sentence.translate(translator)) for sentence in sent_tokenize(body)]
text_fourgram = [ngrams(sent, 4) for sent in present_day_text]

train, vocab = padded_everygram_pipeline(4, text)  # This will generate unigram, bigram, trigram and fourgram


lm = MLE(4)
lm.fit(train, vocab)
# 'verdascos', 'early', 'charge'), FreqDist({'he': 1})


# a = sorted(lm.counts[4].items())
# print(a[::-400])
for i in lm.counts[4]:  # print all the 3 grams
    print(i)
print(lm.score('</s>', ['your', 'scheduler', '</s>']))
# print(len(lm.vocab))
# print(lm.counts)
