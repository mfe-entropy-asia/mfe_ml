import re
import os
import numpy as np
import pickle


class DataCleaner:
    def __init__(self, language, input_file_lst, output_path):
        """
        Class name: DataCleaner

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
        # To filter language
        self.find_en = re.compile("\"language\": \"" + self.language + "\"")

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

    def __call__(self):
        print(self.__repr__())
        self.remove_output_file()  # Remove the output file if it exists
        self.filter_all_conditions()
        self.gen_data()

    def data_clean(self, string: str):
        """
        Function which will do the data clean
        Remove the parentheses
        :param string: the input string data
        :return: string after data clean
        """
        string = self.remove_brackets(string)
        string = string.replace('\\n', '\n').replace('\\"', '').replace('\\r', '\r').replace('*', '')
        return string.lower()

    def gen_data(self):
        """
        :return: list and dictionary needed for NGRAM model
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
                    self.headline_lst.append(self.data_clean(m_headline))
                    self.body_lst.append(self.data_clean(m_body))
                    m_time = np.datetime64(m_time[:10])
                    if m_time not in self.m_dict:
                        self.m_dict[m_time] = []
                    self.m_dict[m_time].append(self.data_clean(m_body))
        pickle_out = open(self.output_path + "dict.pickle", "wb")
        pickle.dump(self.m_dict, pickle_out)
        pickle_out.close()

    def filter_all_conditions(self):
        """
        This is the function to filter the English language article, for articles with the same article ID,
        we keep the first one in the chain.
        :return: "0_filterd.dat" file which contains the data section of the raw data with only English document and
        unique ID articles
        """
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
        Function to tell if the headline is wanted

        :param data: Input string
        :return: Boolean to indicate if the headline is our target headline
        """
        return '"headline": "TABLE-' not in data and "*TOP NEWS*" not in data and "DIARY-" not in data

    def remove_brackets(self, data: str):
        """

        Remove ((.*)) and [.*] and <.*> and nested parentheses

        :param data:  Input string data
        :return: String data after processing.
        """

        # data = self.find_double_parentheses.sub(r'', data)
        # data = self.find_parentheses.sub(r'', data)
        data = self.find_bracket.sub(r'', data)
        data = self.find_angle_quotation.sub(r'', data)
        data = self.remove_nested_parentheses(data)
        return data

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

    def new_story (self, unique_altid, data):
        """

        :param unique_altid:
        :param data: Input string
        :return: Boolean to indicate if the altId has appeared only once
        """
        m_new_story = self.find_altId.search(data)
        alt_id = m_new_story.group(1)
        if alt_id in unique_altid:
            # print (alt_id + "\n")
            return False
        else:
            unique_altid.add(alt_id)
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

    def __repr__(self):
        """
        :return: The information of the class instance
        """
        return "Data Cleaner Class initiates with \nLanguage: " + self.language.upper() + "\n" + "Input Files: " +\
               str(self.input_file_lst) + "\nOutputs: " + self.output_file


#  Executed only when data_cleaner is called as the main function, this part of code is for debug purpose
if __name__ == '__main__':
    dat_clean = DataCleaner("en", ["./data/raw/News.RTRS.201806.0214.txt", "./data/raw/News.RTRS.201807.0214.txt",
                                   "./data/raw/News.RTRS.201808.0214.txt"], "./data/intermediate/")
    dat_clean()
    # for i in range(8):
    #     print(dat_clean.headline_lst[i])
    # tokens = [word_tokenize(sentence) for sentence in sent_tokenize(dat_clean.body_lst[4])]
    # for i in tokens:
    #     print(i)

    for key in dat_clean.m_dict:
        if key == np.datetime64('2018-06-01'):
            print(dat_clean.m_dict[key][3])

