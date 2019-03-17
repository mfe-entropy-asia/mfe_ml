from four_gram_model import FourGramModel
import pickle
import numpy as np

pickle_in = open("./data/intermediate/dict.pickle", "rb")
processed_news_dict = pickle.load(pickle_in)

fitted_models = {}
for key in processed_news_dict:
    if key < np.datetime64('2018-06-08'):
        continue
    else:
        fitted_models[key] = FourGramModel(processed_news_dict, key)
pickle_out = open("./data/intermediate/model.pickle", "wb")
pickle.dump(fitted_models, pickle_out)
pickle_out.close()

# pickle_in = open("./data/intermediate/model.pickle", "rb")
# lm = pickle.load(pickle_in)
# print(lm.score('held', ['zealands', 'currency']))


