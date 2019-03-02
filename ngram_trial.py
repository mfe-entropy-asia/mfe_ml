from nltk.util import ngrams
from nltk import FreqDist
# from nltk.book import *
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import Text
from nltk.lm import NgramCounter
a = [["la", "du", "l", "u", "k", "e", "s"], ["j", 'e', 's', 's', 'i', 'c', 'a']]
bi_gram = [ngrams(sent, 2) for sent in a]
tri_gram = [ngrams(sent, 3) for sent in a]
for items in bi_gram:
    print(list(items))
print(bi_gram)
ngram_counts = NgramCounter(bi_gram + tri_gram)
print(ngram_counts['e', 's']['s'])
print(ngram_counts.N())

# c = FreqDist(b)
# print(c[("l", "u")])
# for i in c:
#     print("The 2-gram is:" + str(i) + ", and the count is:" + str(c[i]))
# sent_token = sent_tokenize()
# tokens = word_tokenize("Here is some not very interesting text")
# text = Text(tokens)
# print(tokens)
