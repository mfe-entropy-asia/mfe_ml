import re
import os
import numpy
# from nltk import word_tokenize
# from nltk import Text
# from nltk import ngrams
# from nltk import FreqDist
# from nltk.book import *


class DataCleaner:
    # This class is to do the data cleaning, and generate the input for the NGRAM model
    def __init__(self, language, input_file_lst, output_file):
        self.headline_lst = []
        self.body_lst = []
        self.language = language
        self.input_file_lst = input_file_lst
        self.output_file = output_file
        self.find_headline = re.compile('\"headline\": \"(.*?)\"')
        self.find_body = re.compile('\"body\": \"(.*?)\"')
        self.find_data = re.compile("\"data\": {(.*?)}")

    def __call__(self):
        self.remove_out_file()  # Remove the output file if it exists
        self.filter_language()
        self.gen_headline_lst()
        self.gen_body_lst()

    def gen_headline_lst(self):
        with open(self.output_file, encoding="utf-8") as f:
            for line in f:
                m_headline = self.find_headline.search(line)
                self.headline_lst.append(m_headline.group(1))   

    def gen_body_lst(self):
        with open(self.output_file, encoding="utf-8") as f:
            for line in f:
                m_body = self.find_body.search(line)
                self.body_lst.append(m_body.group(1))   

    def filter_language(self):
        # This function is to filter news in English language and to keep only the content of data section
        find_lg = re.compile("\"language\": \"" + self.language + "\"")
        for input_file in self.input_file_lst:
            with open(input_file, encoding="utf-8") as f:
                output = open(self.output_file, "a+", encoding="utf-8")
                for line in f:
                    if find_lg.search(line):
                        m_data = self.find_data.search(line)
                        output.write(m_data.group(1)+'\n')
            output.close()

    def remove_out_file(self):
        if os.path.isfile(self.output_file):
            os.remove(self.output_file)
        print("Output File Removed!")
