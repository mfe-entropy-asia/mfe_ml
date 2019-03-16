"""
This is the module to train the ngram model, and generate the fitted model for each day.
"""
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE
import string
import pickle
# from nltk import Text
# from data_cleaner import DataCleaner
# from nltk.util import pad_sequence
# from nltk.util import ngrams
# from nltk import FreqDist


class FourGramModel:
    def __init__(self, input_dict, input_date):
        """
        To instantiate the 4-gram model, we need to provide the dictionary of data , and the date of interest

        :param input_dict: input dictionary, which has the same format as the output oof DataCleaner
        :type input_dict: Dictionary
        :param input_date: date of interesting
        :type input_date: np.datetime64,['D']
        """
        self.input_dict = input_dict
        self.input_date = input_date
        self.train = []
        self.vocab = []
        self.lm = MLE(4)
        self.translator = str.maketrans('', '', string.punctuation)  # To get rid of the punctuations
        return

    def __call__(self):
        self.train_model()

    def train_model(self):
        """
        Train the model with data one week before

        :return: A fitted 4gram model
        """
        training_text = []
        for idx in range(7):
            for content in self.input_dict[self.input_date - idx - 1]:
                training_text += [word_tokenize(sentence.translate(self.translator))
                                  for sentence in sent_tokenize(content)]
        self.train, self.vocab = padded_everygram_pipeline(4, training_text)
        self.lm.fit(self.train, self.vocab)


#  Only executed when this file is called directly, this part of code is for debug purpose only
if __name__ == '__main__':
    translator = str.maketrans('', '', string.punctuation)  # To get rid of the punctuations
    pickle_in = open("./data/intermediate/dict.pickle", "rb")
    processed_news_dict = pickle.load(pickle_in)
    model_1 = FourGramModel(processed_news_dict, np.datetime64('2018-06-08'))
    model_1()

    pickle_out = open("./data/intermediate/model.pickle", "wb")
    pickle.dump(model_1.lm, pickle_out)
    pickle_out.close()
    a = sorted(model_1.lm.counts[3].items())
    print(a[::-400])
    # text = []
    # for i in range(3):
    #     for body in processed_news_dict[np.datetime64('2018-06-01')+i]:
    #         # if body != '':
    #         text += [word_tokenize(sentence.translate(translator)) for sentence in sent_tokenize(body)]
    #
    # date = np.datetime64('2018-06-01') + 4
    # present_day_text = []
    # for body in processed_news_dict[date]:
    #     present_day_text += [word_tokenize(sentence.translate(translator)) for sentence in sent_tokenize(body)]
    # text_fourgram = [ngrams(sent, 4) for sent in present_day_text]
    # train, vocab = padded_everygram_pipeline(4, text)  # This will generate unigram, bigram, trigram and fourgram
    # lm = MLE(4)
    # lm.fit(train, vocab)
    # a = sorted(lm.counts[4].items())
    # print(a[::-400])
    # for i in lm.counts[4]:  # print all the 3 grams
    #     print(i)
    # print(lm.score('almost', ['yields', 'have', 'fallen']))
    # print(len(lm.vocab))
    # print(lm.counts)
