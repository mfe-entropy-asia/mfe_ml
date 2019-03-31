from src.fourgram.four_gram_model import FourGramModel
# from data_cleaner import DataCleaner
import pickle
import numpy as np
import pandas as pd
import os
import time
# from multiprocessing import Pool
# from multiprocessing import Manager
import multiprocessing as mp
from functools import partial


def multiple_processing_func(input_data_series, input_date):
    # global fitted_models
    # global processed_news_dict
    if input_date < np.datetime64('2018-06-08'):
        return
    else:
        model = FourGramModel(input_data_series, input_date)
        try:
            model()
        except Exception as e:
            print("Training failed;" + e)
    print("Dumping Pickle file.........\n")
    pik_name = str(input_date)
    pickle_path = '../../data/intermediate/3_models/model_' + pik_name + '.pickle'
    pickle_out = open(pickle_path, "wb")
    pickle.dump({input_date: model.lm}, pickle_out)
    pickle_out.close()
    print("Finish dumping\n")


def multi_train_handler(data_series):
    p = mp.Pool()
    date_list = [np.datetime64(key).astype('datetime64[D]') for key in data_series.index]
    train_model = partial(multiple_processing_func, data_series)
    p.map_async(train_model, date_list)
    p.close()
    p.join()


if __name__ == '__main__':
    dict_pickle_path = "../../data/intermediate/1_cleaned.pickle"
    pickle_in = open(dict_pickle_path, "rb")
    processed_news_series = pickle.load(pickle_in)
    pickle_in.close()
    start = time.time()
    # for date in date_list:
    #     fitted_model = multiple_processing_func(processed_news_series, date)
    #     pik_name = str(date)
    #     pickle_path = '../../data/intermediate/model_' + pik_name + '.pickle'
    #     pickle_out = open(pickle_path, "wb")
    #     pickle.dump(fitted_model, pickle_out)
    #     pickle_out.close()
    multi_train_handler(processed_news_series)
    end = time.time()
    # fitted_models = dict(fitted_models)
    print("All models fitted, total Time:" + str(end - start))




