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

model_dir = '../../data/intermediate/2_models'

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
    pickle_path = model_dir + '/model_' + pik_name + '.pickle'
    pickle_out = open(pickle_path, "wb")
    pickle.dump(model.lm, pickle_out)
    pickle_out.close()
    print("Finish dumping\n")


def multi_train_handler(data_series):
    p = mp.Pool()
    date_list = [np.datetime64(key).astype('datetime64[D]') for key in data_series.index]
    train_model = partial(multiple_processing_func, data_series)
    p.map_async(train_model, date_list)
    p.close()
    p.join()


def run():
    if not os.path.exists(model_dir):
        print("\ncreating dir: ", model_dir, "\n")
        os.makedirs(model_dir)
    dict_pickle_path = "../../data/intermediate/1_cleaned.pickle"
    pickle_in = open(dict_pickle_path, "rb")
    processed_news_series = pickle.load(pickle_in)
    pickle_in.close()
    start = time.time()
    multi_train_handler(processed_news_series)
    end = time.time()
    print("All models fitted, total Time:" + str(end - start))

if __name__ == '__main__':
    run()


