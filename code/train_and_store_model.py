from four_gram_model import FourGramModel
from data_cleaner import DataCleaner
import pickle
import numpy as np
import os
import time
from multiprocessing import Pool, Queue


dict_pickle_path = "../data/intermediate/dict.pickle"

if not os.path.isfile(dict_pickle_path):
        dat_clean = DataCleaner("en", ["../data/raw/News.RTRS.201806.0214.txt", "../data/raw/News.RTRS.201807.0214.txt",
                                       "../data/raw/News.RTRS.201808.0214.txt"], "../data/intermediate/")
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
        model = FourGramModel(processed_news_dict, input_date)
        try:
            model()
            fitted_models[input_date] = model.lm
        except Exception as e:
            print("Training failed;" + e)


if __name__ == '__main__':
    p = Pool(2)
    start = time.time()
    p.map_async(multiple_processing_func, [key for key in processed_news_dict])
    p.close()
    p.join()
    end = time.time()
    print("All models fitted, total Time:" + str(end - start))

    print("Dumping Pickle file.........\n")
    pickle_out = open("../data/intermediate/model.pickle", "wb")
    pickle.dump(fitted_models, pickle_out)
    pickle_out.close()
    print("Finish dumping\n")



