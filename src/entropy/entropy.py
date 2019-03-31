import pickle


class Entropy:
    def __init__(self):
        pass

    def __call__(self):
        pass


if __name__ == '__main__':
    pickle_in = open("../../data/intermediate/2_freq_grams.pickle", "rb")
    freq_ngrams = pickle.load(pickle_in)
    pickle_in.close()

