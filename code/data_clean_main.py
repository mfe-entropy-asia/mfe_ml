"""Main function to call the Data clean method with multiple process"""
from new_data_cleaner import DataCleaner
import time
import multiprocessing as mp
from functools import partial
# import numpy as np
import pickle


def clean_a_file_and_return_data(input_file, data_cleaner, article_dict):
    result = []
    with open(input_file, encoding="utf-8") as f:
        line_nu = 0
        for line in f:
            if line_nu != 0:
                # print(line.encode("utf-8"))
                # data_cleaner(line)
                if data_cleaner(line, article_dict):
                    m_data = data_cleaner.find_data.search(line)
                    write_line = m_data.group(1)
                    result.append(write_line + "\n")
            line_nu += 1
    return data_cleaner.m_dict, result


def handler(file_list, data_cleaner, article_dict):
    p = mp.Pool(3)
    result = {}
    with open("../data/intermediate/out.dat", "w", encoding="utf-8") as f:
        for return_dict, return_list in p.imap(partial(clean_a_file_and_return_data, data_cleaner=data_cleaner,
                                                       article_dict=article_dict),
                                               file_list):
            result.update(return_dict)
            f.writelines(return_list)
    return result


if __name__ == '__main__':
    manager = mp.Manager()
    shared_article_dict = manager.dict()
    Dat_clean = DataCleaner()
    input_file_list = ["../data/raw/News.RTRS.201806.0214.txt", "../data/raw/News.RTRS.201807.0214.txt",
                       "../data/raw/News.RTRS.201808.0214.txt"]
    print("Cleaning data ...")
    start = time.time()
    my_dict = handler(input_file_list, Dat_clean, shared_article_dict)
    end = time.time()
    print("Cleaning finished!!!  Total time: %s seconds" % (end - start))
    pickle_out = open("../data/intermediate/dict_with_new_cleaner_multiple_process.pickle", "wb")
    pickle.dump(my_dict, pickle_out)
    pickle_out.close()
    # print(Dat_clean.m_dict)
    # for key in my_dict:
    #     if key == np.datetime64('2018-06-08'):
    #         print(my_dict[key][0])
