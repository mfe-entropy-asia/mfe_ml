from FourGramModel import FourGramModel
from data_cleaner import DataCleaner
import pickle
import numpy as np
import os
from multiprocessing import Pool, Queue


dict_pickle_path = "./data/intermediate/dict.pickle"

if not os.path.isfile(dict_pickle_path):
        dat_clean = DataCleaner("en", ["./data/raw/News.RTRS.201806.0214.txt", "./data/raw/News.RTRS.201807.0214.txt",
                                       "./data/raw/News.RTRS.201808.0214.txt"], "./data/intermediate/")
        dat_clean()

pickle_in = open(dict_pickle_path, "rb")
processed_news_dict = pickle.load(pickle_in)

fitted_models = {}


def multiple_processing_func(input_date):
    global fitted_models
    global processed_news_dict
    if input_date < np.datetime64('2018-06-08'):
        return
    else:
        print("=====================================\n" + "Fitting model for date: " + str(input_date) +
              "...\n=====================================")
        fitted_models[input_date] = FourGramModel(processed_news_dict, input_date)
        try:
            fitted_models[input_date]()
        except Exception as e:
            print("Training failed;" + e)

        print("=====================================\n""Model for date: " + str(input_date) +
              " has been fitted!!!!!! \n" + "=====================================")


if __name__ == '__main__':
    p = Pool(3)
    p.map_async(multiple_processing_func, [key for key in processed_news_dict])
    p.close()
    p.join()

    pickle_out = open("./data/intermediate/model.pickle", "wb")
    pickle.dump(fitted_models, pickle_out)
    pickle_out.close()

# pickle_in = open("./data/intermediate/model.pickle", "rb")
# lm = pickle.load(pickle_in)
# print(lm.score('held', ['zealands', 'currency']))


