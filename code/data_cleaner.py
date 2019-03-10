import re
import os
import numpy as np


class DataCleaner:
    """
    Class name: DataCleaner
    CLass Member: TBA

    """
    def __init__(self, language, input_file_lst, output_path):
        """

        :param language: Language we are interested in, English by default
        :param input_file_lst: list of files paths
        :param output_path: output file path
        """
        self.headline_lst = []
        self.body_lst = []
        self.m_dict = {}
        self.language = language
        self.input_file_lst = input_file_lst
        self.output_path = output_path
        self.output_file = output_path + "en_output.dat"
        self.intermediate_filtered = output_path + "0_filtered.dat"
        self.find_en = re.compile("\"language\": \"" + self.language + "\"")
        self.find_altId = re.compile('"altId": "(.*?)",')
        self.find_headline = re.compile('"headline": "(.*?)", "takeSequence"')
        self.find_body = re.compile('"body": "(.*?)", "mimeType"')
        self.find_data = re.compile("\"data\": {(.*?)}}")
        self.find_time = re.compile('"versionCreated": "(.*?)"')
        self.find_double_parentheses = re.compile(r'\(\(.*?\)\)') 
        # self.find_parentheses = re.compile(r'\(.*?\)')  # Wrong !!!! Not applicable for nested parentheses 
        self.find_bracket = re.compile(r'\[.*?\]')
        self.find_angle_quotation = re.compile(r'<.*?>')

    def __call__(self):
        self.remove_output_file()  # Remove the output file if it exists
        self.filter_all_conditions()
        self.gen_data()
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
    # @staticmethod
    def data_regx_clean(self, string: str):
        """
        Function that contains all the data processing:
        \n \r
        remove quotation
        remove stars
        call remove_brackets
        """
        string = self.remove_brackets(string)
        string = string.replace('\\n', '\n').replace('\\"', '').replace('\\r', '\r').replace('*', '')
        return string

    def gen_data(self):
        """

        :return: unction: list and dictionary needed for NGRAM model
        """
        with open(self.intermediate_filtered, encoding="utf-8") as f:
            for line in f:
                m_headline = self.find_headline.search(line)
                m_headline = m_headline.group(1)
                m_body = self.find_body.search(line)
                m_body = m_body.group(1)
                m_time = self.find_time.search(line)
                m_time = m_time.group(1)
                if m_body != '':
                    self.headline_lst.append(self.data_regx_clean(m_headline))
                    self.body_lst.append(self.data_regx_clean(m_body))
                    m_time = np.datetime64(m_time).astype('datetime64[D]')
                    if m_time not in self.m_dict:
                        self.m_dict[m_time] = []
                        self.m_dict[m_time].append(self.data_regx_clean(m_body))
                    else:
                        self.m_dict[m_time].append(self.data_regx_clean(m_body))

    def filter_all_conditions(self):
        unique_alt_id = set()
        for input_file in self.input_file_lst:
            with open(input_file, encoding="utf-8") as f:
                output = open(self.intermediate_filtered, "a+", encoding="utf-8")
                for line in f:
                    if self.not_english(line):
                        m_data = self.find_data.search(line)
                        data = m_data.group(1)
                        if self.target_headline(data) and self.new_story(unique_alt_id, data):
                            output.write(data + "\n")
                # print("uniqueAltId" + ', '.join(unique_alt_id))  # For debug purpose, printing out all article ID
                output.close()

    def not_english(self, line):
        """

        :param line: Input line
        :return: True or False to indicate if the language is English
        """
        return self.find_en.search(line)

    @staticmethod
    def target_headline(data):
        """

        :param data: Input string
        :return: Boolean to indicate if the headline is our target headline
        """
        return '"headline": "TABLE-' not in data and "*TOP NEWS*-Front Pag" not in data and "DIARY-" not in data

    def remove_brackets(self, data: str):
        """
        Remove ((.*)) and [.*] and <.*> and nested parentheses
        """
        # if self.find_double_parentheses.match(data):
        #     print("yes")
        data = self.find_double_parentheses.sub(r'', data)
        # data = self.find_parentheses.sub(r'', data)
        data = self.find_bracket.sub(r'', data)
        data = self.find_angle_quotation.sub(r'', data)
        data = self.remove_nested_parentheses(data)
        return data

    @staticmethod
    def remove_nested_parentheses(data: str):
        """

        :param data: input string
        :return: data with all parentheses removesd
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

    def new_story (self, unique_altId, data):
        """

        :param unique_altId:
        :param data: Input string
        :return: Boolean to indicate if the altId has appeared only once
        """
        m_new_story = self.find_altId.search(data)
        alt_id = m_new_story.group(1)
        if alt_id in unique_altId:
            # print (alt_id + "\n")
            return False
        else:
            unique_altId.add(alt_id)
            return True

    def remove_output_file(self):
        """

        :return: Remove the output file if already exists
        """
        for the_file in os.listdir(self.output_path):
            file_path = os.path.join(self.output_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)
        print("Output File Removed!")
