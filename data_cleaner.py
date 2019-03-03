import re
import os


class DataCleaner:
    """
    Class name: DataCleaner
    CLass Methods:
        1. filter_language: This method is to filter the raw data with the language given
        2. data_clean(TBD): This method is to the data cleaning, including multiple rules
        3. gen_lst: This method is to generate lists items to pass to the ngram model
    """
    def __init__(self, language, input_file_lst, output_file):
        self.headline_lst = []
        self.body_lst = []
        self.language = language
        self.input_file_lst = input_file_lst
        self.output_file = output_file
        self.find_headline = re.compile('"headline": "(.*?)", "takeSequence"')
        self.find_body = re.compile('"body": "(.*?)", "mimeType"')
        self.find_data = re.compile("\"data\": {(.*?)}}")

    def __call__(self):
        self.remove_output_file()  # Remove the output file if it exists
        self.filter_language()
        self.gen_lst()
        # self.gen_headline_lst()
        # self.gen_body_lst()

    # def gen_headline_lst(self):
    #     with open(self.output_file, encoding="utf-8") as f:
    #         for line in f:
    #             m_headline = self.find_headline.search(line)
    #             self.headline_lst.append(m_headline.group(1))
    #
    # def gen_body_lst(self):
    #     with open(self.output_file, encoding="utf-8") as f:
    #         for line in f:
    #             m_body = self.find_body.search(line)
    #             self.body_lst.append(m_body.group(1))

    def gen_lst(self):
        """Function: To generate the lst needed for NGRAM model"""
        with open(self.output_file, encoding="utf-8") as f:
            for line in f:
                m_headline = self.find_headline.search(line)
                m_body = self.find_body.search(line)
                self.headline_lst.append(m_headline.group(1).replace('\\n', '\n'))
                self.body_lst.append(m_body.group(1).replace('\\n', '\n'))

    def filter_language(self):
        """This function is to filter news according the language and to keep only the content of data section"""
        find_lg = re.compile("\"language\": \"" + self.language + "\"")
        for input_file in self.input_file_lst:
            with open(input_file, encoding="utf-8") as f:
                output = open(self.output_file, "a+", encoding="utf-8")
                for line in f:
                    if find_lg.search(line):
                        m_data = self.find_data.search(line)
                        output.write(m_data.group(1)+'\n')
            output.close()

    def remove_output_file(self):
        if os.path.isfile(self.output_file):
            os.remove(self.output_file)
        print("Output File Removed!")
