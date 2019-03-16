import numpy as np
from data_cleaner import DataCleaner
# from nltk.util import ngrams
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

# print(dat_clean.body_lst[4])
# print(sent_tokenize(dat_clean.body_lst[4]))
text = []
for body in dat_clean.m_dict[np.datetime64('2018-06-01')]:
    # if body != '':
    text += [word_tokenize(sentence.translate(translator)) for sentence in sent_tokenize(body)]

# tokens = [word_tokenize(sentence.translate(translator)) for sentence in sent_tokenize(dat_clean.body_lst[4])]
# print(tokens)
# for i in tokens:
#     print(i)
train, vocab = padded_everygram_pipeline(4, text)  # This will generate unigram, bigram, trigram and fourgram
lm = MLE(4)
lm.fit(train, vocab)
# for i in lm.vocab:
#     print(i)

# for i in lm.counts[4]:  # print all the 3 grams
#     print(i)

print(len(lm.vocab))
print(lm.counts)
