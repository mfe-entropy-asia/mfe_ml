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
import time
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
# from nltk import Text
# from data_cleaner import DataCleaner
# from nltk.util import pad_sequence
# from nltk.util import ngrams
# from nltk import FreqDist


class FourGramModel:
    def __init__(self, input_data_frame, input_date):
        """
        To instantiate the 4-gram model, we need to provide the dataframe , and the date of interest

        :param input_data_frame: input data_frame, which has the same format as the output oof DataCleaner
        :type input_data_frame: data_frame
        :param input_date: date of interesting
        :type input_date: np.datetime64,['D']
        """
        self.input_data_frame = input_data_frame
        self.input_date = input_date
        self.train = []
        self.vocab = []
        self.lm = MLE(4)
        self.translator = str.maketrans('', '', string.punctuation)  # To get rid of the punctuations
        self.stopWords = set(stopwords.words('english'))
        return

    def __call__(self):
        start = time.time()
        print("Fitting model for date: " + str(self.input_date) + "\n")
        self.train_model()
        end = time.time()
        print("Model for date: " + str(self.input_date) + " has been fitted \n" +
              "Time taking: " + str(end-start) + "\n")

    def stop_words_and_stem(self, word_list):
        """
        This is the function which will remove the stop words and do the word stemming
        :param word_list: a list of words to be processed
        :return:
        """
        return_list = []
        ps = PorterStemmer()
        for w in word_list:
            if w not in self.stopWords:
                return_list.append(ps.stem(w))
        return return_list

    def train_model(self):
        """
        Train the model with data one week before

        :return: A fitted 4gram model
        """
        training_text = []
        for idx in range(7):
            for content in self.input_data_frame[self.input_date - idx - 1]:
                training_text += [self.stop_words_and_stem(word_tokenize(sentence.translate(self.translator)))
                                  for sentence in sent_tokenize(content)]
        # print(training_text[1])
        # self.train, self.vocab = padded_everygram_pipeline(4, training_text)
        every_gram, vocab = padded_everygram_pipeline(4, training_text)  # This will generate unigram, bigram,
        # trigram and fourgram
        three_gram = []
        four_gram = []
        for sent in list(every_gram):
            for item in sent:
                # if len(item) == 3:
                #     three_gram.append(item)
                # elif len(item) == 4:
                #     four_gram.append(item)
                if len(item) == 4:
                    four_gram.append(item)
        # three_gram = [item for sent in list(every_gram) for item in sent if len(item) == 3]
        # four_gram = [item for sent in list(every_gram) for item in sent if len(item) == 4]
        train = [four_gram]
        self.lm.fit(train, vocab)


#  Only executed when this file is called directly, this part of code is for debug purpose only
if __name__ == '__main__':
    translator = str.maketrans('', '', string.punctuation)  # To get rid of the punctuations
    pickle_in = open("../../data/intermediate/1_cleaned.pickle", "rb")
    processed_news_dataframe = pickle.load(pickle_in)
    model_1 = FourGramModel(processed_news_dataframe, np.datetime64('2018-06-08'))
    model_1()
    pickle_out = open("../../data/intermediate/2_model.pickle", "wb")
    pickle.dump({np.datetime64('2018-06-08 00:00:00'): model_1.lm}, pickle_out)
    pickle_out.close()
