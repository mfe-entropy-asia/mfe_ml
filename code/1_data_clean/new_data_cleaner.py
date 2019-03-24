# -*- coding: utf-8 -*-
import re
import os
import numpy as np
import pandas as pd
import time
import pickle


class DataCleaner:
    def __init__(self):
        self.m_dict = {}
        self.m_data_series = pd.Series()
        # self.input_file_lst = input_file_lst
        # self.output_path = output_path
        # self.output_file = output_path + "en_output.dat"
        # self.intermediate_filtered = output_path + "0_filtered.dat"
        # To filter language
        self.find_en = re.compile('"language": "en"')

        # To find uniq article ID
        self.find_altId = re.compile('"altId": "(.*?)",')

        # To match the headline content
        self.find_headline = re.compile('"headline": "(.*?)", "takeSequence"')

        # To match the body content
        self.find_body = re.compile('"body": "(.*?)", "mimeType"')

        # To extract data section
        self.find_data = re.compile("\"data\": {(.*?)}}")

        # Time
        self.find_time = re.compile('"versionCreated": "(.*?)"')
        # The Reuters footnote(e.g. ((Diaries@thomsonreuters.com))) needs to be removed
        # self.find_double_parentheses = re.compile(r'\(\(.*?\)\)')   # The Reuters footnote needs to be removed

        # self.find_parentheses = re.compile(r'\(.*?\)')  # Wrong !!!! Not applicable for nested parentheses 
        self.find_bracket = re.compile(r'\[.*?\]')

        self.find_angle_quotation = re.compile(r'<.*?>')

        self.find_header = re.compile(r'^.* - ')

        self.invalid_headline = re.compile(r'headline": "TABLE-" '
                                           r'| "headline": "*TOP NEWS*" '
                                           r'| "headline": "DIARY-" '
                                           r'| "headline": "SHH .* Margin Trading" '
                                           r'| "headline": "North American power transmission outage update - PJM" '
                                           r'| "headline": "UPDATE 1"')
        self.unique_alt_id = set()

    def __call__(self, data, article_dict):
        if self.valid_english_story(article_dict, data):
            # print("This line is valid!")
            self.gen_dict(data)
            return True
        else:
            return False
            # print("This line is not valid!!!!")

    def gen_dict(self, data):
        m_body = self.find_body.search(data)
        m_body = m_body.group(1)
        m_time = self.find_time.search(data)
        m_time = m_time.group(1)
        m_time = np.datetime64(m_time[:10])
        # print("Time is %s" % m_time)
        if m_time not in self.m_data_series.index:
            # print("Time %s is not in dictionary" % m_time)
            # self.m_dict[m_time] = []
            self.m_data_series.at[m_time] = []
        # self.m_dict[m_time].append(self.1_data_clean(m_body))
        self.m_data_series.at[m_time].append(self.data_clean(m_body))

    def data_clean(self, string: str):
        """
        Function which will do the data clean
        Remove the parentheses
        :param string: the input string data
        :return: string after data clean
        """
        string = self.remove_brackets(string)
        string = self.remove_header(string)
        string = string.replace('\\n', ' ')\
            .replace('\\\"', '')\
            .replace('\\r', ' ')\
            .replace('*', '')\
            .replace('“', '')\
            .replace('”', '')
        return string.lower()

    def valid_english_story(self, article_dict, data):
        return self.if_body_not_empty(data) and self.if_en(data) and self.target_headline(data) \
               and self.new_story(article_dict, data)
        
    def if_en(self, data):
        if self.find_en.search(data):
            return True
        else:
            return False

    def if_body_not_empty(self, data):
        m_body = self.find_body.search(data)
        m_body = m_body.group(1)
        if m_body != '':
            return True
        else:
            return False

    # def target_headline(self, data):
    #     return not self.invalid_headline.search(data)

    @staticmethod
    def target_headline(data):
        invalid_headline = ['"headline": "TABLE-', '"headline": "*TOP NEWS*', '"headline": "DIARY-',
                            '"headline": "SHH Daily Margin Trading', '"headline": "SHH Margin Trading',
                            '"headline": "North American power transmission outage update - PJM',
                            '"headline": "UPDATE 1', '"headline": " BOJ:', '"headline": "CRBIndex']
        if any(x in data for x in invalid_headline):
            return False
        else:
            return True

    def new_story(self, article_dict, data):
        m_new_story = self.find_altId.search(data)
        alt_id = m_new_story.group(1)
        if alt_id in article_dict:
            # print (alt_id + "\n")
            return False
        else:
            article_dict[alt_id] = 1
            return True
            
    @staticmethod
    def remove_nested_parentheses(data: str):
        """

        :param data: input string
        :return: data with all parentheses removed
        """
        result = ''
        depth = 0
        for letter in data:
            if letter == '(':
                depth += 1
            elif letter == ')':
                depth -= 1
            elif depth == 0:
                result += letter
        return result

    @staticmethod
    def remove_nested_brackets(data: str):
        """

        :param data: input string
        :return: data with all parentheses removed
        """
        result = ''
        depth = 0
        for letter in data:
            if letter == '[':
                depth += 1
            elif letter == ']':
                depth -= 1
            elif depth == 0:
                result += letter
        return result

    @staticmethod
    def remove_nested_square_brackets(data: str):
        """

        :param data: input string
        :return: data with all parentheses removed
        """
        result = ''
        depth = 0
        for letter in data:
            if letter == '{':
                depth += 1
            elif letter == '}':
                depth -= 1
            elif depth == 0:
                result += letter
        return result

    def remove_brackets(self, data):
        """

        Remove ((.*)) and [.*] and <.*> and nested parentheses

        :param data:  Input string data
        :return: String data after processing.
        """

        data = self.find_bracket.sub(r'', data)
        data = self.find_angle_quotation.sub(r'', data)
        data = self.remove_nested_parentheses(data)
        data = self.remove_nested_brackets(data)
        data = self.remove_nested_square_brackets(data)
        return data

    def remove_header(self, data):
        data = self.find_header.sub(r'', data)
        return data


if __name__ == '__main__':
    print("data_cleaner.py called directly!!!")
    Dat_clean = DataCleaner()
    start = time.time()
    print("Cleaning data, starting time: %s ..." % start)
    output_file = open("../../data/intermediate/out_single_process.dat", "w", encoding="utf-8")
    input_file_list = ["../../data/raw/News.RTRS.201806.0214.txt", "../../data/raw/News.RTRS.201807.0214.txt",
                       "../../data/raw/News.RTRS.201808.0214.txt"]
    unique_altid_dict = {}
    # for file in input_file_list:
    #     with open(file, encoding="utf-8") as f:
    #         next(f)
    #         for line in f:
    #             if Dat_clean(line, unique_altid_dict):
    #                 m_data = Dat_clean.find_data.search(line)
    #                 write_line = m_data.group(1)
    #                 output_file.write(write_line + "\n")

    for file in input_file_list:
        with open(file, encoding="utf-8") as f:
            next(f)
            for line in f:
                Dat_clean(line, unique_altid_dict)
                
    for i in Dat_clean.m_data_series:
        # print(len(i))
        for body in i:
            output_file.write(body + '\n')
    output_file.close()
    end = time.time()
    print("Cleaning finished!!!  Total time: %s seconds" % (end - start))
    # print(Dat_clean.m_data_series.at[np.datetime64('2018-06-08')][1])
    pickle_out = open("../../data/intermediate/series_with_new_cleaner_single_process.pickle", "wb")
    pickle.dump(Dat_clean.m_data_series, pickle_out)
    pickle_out.close()


