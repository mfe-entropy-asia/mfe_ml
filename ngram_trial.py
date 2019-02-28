from nltk import ngrams
from nltk import FreqDist
from nltk.book import *
a = ["la", "du", "l", "u", "k", "e"]
b = ngrams(a, 2)
c = FreqDist(b)
print(c[("l", "u")])
for i in c:
    print("The 2-gram is:" + str(i) + ", and the count is:" + str(c[i]))
from nltk import word_tokenize
from nltk import Text
tokens=word_tokenize("Here is some not very interesting text")
text=Text(tokens)