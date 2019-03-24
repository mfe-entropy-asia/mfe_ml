"""Main function to call the Data clean method with multiple process"""
from new_data_cleaner import DataCleaner
import time
import multiprocessing as mp
from functools import partial
import pandas as pd
import pickle


def clean_a_file_and_return_data(input_file, data_cleaner, article_dict):
    # result = []
    with open(input_file, encoding="utf-8") as f:
        next(f)
        for line in f:
            # print(line.encode("utf-8"))
            data_cleaner(line, article_dict)
            # if data_cleaner(line, article_dict):
            #     m_data = data_cleaner.find_data.search(line)
            #     write_line = m_data.group(1)
            #     result.append(write_line + "\n")
    return data_cleaner.m_data_series


def handler(file_list, data_cleaner, article_dict):
    p = mp.Pool(3)
    result = pd.Series()
    # with open("../../data/intermediate/out.dat", "w", encoding="utf-8") as f:
    for return_data_series in p.imap(partial(clean_a_file_and_return_data,
                                             data_cleaner=data_cleaner, article_dict=article_dict), file_list):
        result = result.append(return_data_series)
    return result


if __name__ == '__main__':
    manager = mp.Manager()
    shared_article_dict = manager.dict()
    Dat_clean = DataCleaner()
    input_file_list = ["../../data/raw/News.RTRS.201806.0214.txt", "../../data/raw/News.RTRS.201807.0214.txt",
                       "../../data/raw/News.RTRS.201808.0214.txt"]
    print("Cleaning data ...")
    start = time.time()
    my_dict = handler(input_file_list, Dat_clean, shared_article_dict)
    end = time.time()
    print("Cleaning finished!!!  Total time: %s seconds" % (end - start))

    with open("../../data/intermediate/out_multi_process.dat", "w", encoding="utf-8") as f_out:
        for i in my_dict:
            print(type(i))
            print(len(i))
            for body in i:
                f_out.write(body + '\n')

    # print(my_dict.at[np.datetime64('2018-06-08')][1])
    pickle_out = open("../../data/intermediate/series_with_new_cleaner_multiple_process.pickle", "wb")
    pickle.dump(my_dict, pickle_out)
    pickle_out.close()
    # print(Dat_clean.m_dict)
    # for key in my_dict:
    #     if key == np.datetime64('2018-06-08'):
    #         print(my_dict[key][0])
