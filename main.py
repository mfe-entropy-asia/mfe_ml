from data_cleaner import DataCleaner
from nltk import ngrams
from nltk import FreqDist
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import Text
dat_clean = DataCleaner("en", ["news.txt"], "en_output.dat")
dat_clean()
for i in range(8):
    print(dat_clean.headline_lst[i])
tokens = [word_tokenize(sentence) for sentence in sent_tokenize(dat_clean.body_lst[4])]
for i in tokens:
    print(i)
