from nltk import ngrams
from nltk import FreqDist
from nltk.book import *
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import Text
a = ["la", "du", "l", "u", "k", "e"]
b = ngrams(a, 2)
c = FreqDist(b)
print(c[("l", "u")])
for i in c:
    print("The 2-gram is:" + str(i) + ", and the count is:" + str(c[i]))
sent_token = sent_tokenize()
tokens = word_tokenize("Here is some not very interesting text")
text = Text(tokens)
print(tokens)
