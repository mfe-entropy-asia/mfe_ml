import pickle
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../sentiment')
from sentiment import Sentiment

class Entropy:
    def __init__(self, ngram_cout_universe):
        self.ngram_cout_universe = ngram_cout_universe
        self.st = Sentiment()

    def __call__(self):
        for date in self.ngram_cout_universe:
            if date > np.datetime64('2018-06-07'):
                token_count = self.ngram_cout_universe[date]
                ngram_model = self.read_model(date)
                entpos, entneg = self.calculate_entpos_entneg(token_count, ngram_model)
                sentpos, sentneg = self.calculate_sentpos_sentneg(token_count)
                print("{} ENTSENT_POS: {} * {} = {}   ENTSENT_NEG: {} * {} = {}".format(
                    pd.to_datetime(str(date)).strftime('%Y-%m-%d'),
                    entpos, sentpos, entpos * sentpos,
                    entneg, sentneg, entneg * sentneg,))

    @staticmethod
    def read_model(date):
        day = pd.to_datetime(str(date)).strftime('%Y-%m-%d')
        pickle_in = open("../../data/intermediate/2_models/model_{}.pickle".format(day), "rb")
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

    def positive_negative_universe(self, token_counts):
        token_counts_pos, token_counts_neg = {}, {}
        for ngram in token_counts:
            positive, negative = self.st.pos_neg(ngram)
            if positive:
                token_counts_pos[ngram] = token_counts[ngram]
            if negative:
                token_counts_neg[ngram] = token_counts[ngram]
        return token_counts_pos, token_counts_neg

    def calculate_entpos_entneg(self, daily_token_count, daily_ngram_model):
        pos_tokens, neg_tokens = self.positive_negative_universe(daily_token_count)
        entpos = Entropy.calculate_entropy(pos_tokens, daily_ngram_model)
        entneg = Entropy.calculate_entropy(neg_tokens, daily_ngram_model)
        return entpos, entneg

    def calculate_sentpos_sentneg(self, daily_token_count):
        sum_pos, sum_neg = 0, 0
        for ngram in daily_token_count:
            positive, negative = self.st.pos_neg(ngram)
            sum_pos += daily_token_count[ngram] if positive else 0
            sum_neg += daily_token_count[ngram] if negative else 0
        sentpos = sum_pos / sum(daily_token_count.values())
        sentneg = sum_neg / sum(daily_token_count.values())
        return sentpos, sentneg


def run():
    pickle_in = open("../../data/intermediate/3_freq_grams.pickle", "rb")
    freq_ngrams = pickle.load(pickle_in)
    pickle_in.close()
    entropy = Entropy(freq_ngrams)
    entropy()


if __name__ == '__main__':
    run()
