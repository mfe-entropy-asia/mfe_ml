import pickle
import pandas as pd
import numpy as np

class Entropy:
    def __init__(self, ngram_cout_universe):
        self.ngram_cout_universe = ngram_cout_universe

    def __call__(self):
        for date in self.ngram_cout_universe:
            if date > np.datetime64('2018-06-07'):
                token_count = self.ngram_cout_universe[date]
                ngram_model = self.read_model(date)
                entropy = self.calculate_entropy(token_count, ngram_model)
                print("entropy for {} is {}".format(pd.to_datetime(str(date)).strftime('%Y-%m-%d'), entropy))

    @staticmethod
    def read_model(date):
        day = pd.to_datetime(str(date)).strftime('%Y-%m-%d')
        pickle_in = open("../../data/intermediate/3_models/model_{}.pickle".format(day), "rb")
        daily_model = pickle.load(pickle_in)
        pickle_in.close()
        return daily_model

    @staticmethod
    def calculate_entropy(daily_token_count, daily_ngram_model):
        """
        the higher, the more unusual
        """
        sum_of_counts = sum(daily_token_count.values())
        cross_entropy = 0
        for ngram in daily_token_count:
            if daily_ngram_model.score(ngram[-1], list(ngram[0:3])) == 0:
                mi = np.log2(0.25)
            else:
                mi = daily_ngram_model.logscore(ngram[-1], list(ngram[0:3]))
            pi = daily_token_count[ngram] / sum_of_counts
            cross_entropy -= pi * mi
        return cross_entropy

    def calculate_sent_pos(self, input_ngram_dict):
        sum_of_pos = 0
        for ngram in input_ngram_dict:
            if self.is_pos(ngram):
                sum_of_pos += input_ngram_dict[ngram]
            sent_pos = sum_of_pos / sum(input_ngram_dict.values())
        return sent_pos

    def is_pos(self, ngram):
        return True


if __name__ == '__main__':
    pickle_in = open("../../data/intermediate/2_freq_grams.pickle", "rb")
    freq_ngrams = pickle.load(pickle_in)
    pickle_in.close()
    entropy = Entropy(freq_ngrams)
    entropy()

