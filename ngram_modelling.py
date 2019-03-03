from data_cleaner import DataCleaner
# from nltk.util import ngrams
# from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
# from nltk.util import pad_sequence
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
# from nltk import Text
dat_clean = DataCleaner("en", ["news.txt"], "en_output.dat")
dat_clean()
# for i in range(8):
#     print(dat_clean.headline_lst[i])
print(dat_clean.body_lst[4])
tokens = [word_tokenize(sentence) for sentence in sent_tokenize(dat_clean.body_lst[4])]
# print(tokens)
for i in tokens:
    print(i)
train, vocab = padded_everygram_pipeline(4, tokens)
lm = MLE(4)
lm.fit(train, vocab)
# for i in lm.vocab:
#     print(i)
# print(len(lm.vocab))
# print(lm.counts)
