import re
import numpy as np
import pandas as pd
import time
import pickle


class DataFilter:
    def __init__(self):
        self.m_dict = {}
        self.m_data_series = pd.Series()
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
        self.invalid_headline = re.compile(r'headline": "TABLE-" '
                                           r'| "headline": "*TOP NEWS*" '
                                           r'| "headline": "DIARY-" '
                                           r'| "headline": "SHH .* Margin Trading" '
                                           r'| "headline": "North American power transmission outage update - PJM" '
                                           r'| "headline": "UPDATE 1"')
        self.unique_alt_id = set()

    def __call__(self, data_line, article_dict):
        if self.valid_english_story(article_dict, data_line):
            self.create_universe(data_line)
            return True

    def create_universe(self, data_line):
        m_time = self.find_time.search(data_line)
        m_time = m_time.group(1)
        m_time = np.datetime64(m_time[:10])
        if m_time not in self.m_data_series.index:
            self.m_data_series.at[m_time] = []
        self.m_data_series.at[m_time].append(data_line)

    def valid_english_story(self, article_dict, data):
        return not self.body_looks_like_a_table(data) \
               and self.if_body_not_empty(data) \
               and self.if_en(data) \
               and self.target_headline(data) \
               and self.new_story(article_dict, data)

    def if_en(self, data):
        if self.find_en.search(data):
            return True
        else:
            return False

    def body_looks_like_a_table(self, data):
        m_body = self.find_body.search(data)
        m_body = m_body.group(1)
        return '---------' in m_body or '_____________' in m_body or '---     ---' in m_body

    def if_body_not_empty(self, data):
        m_body = self.find_body.search(data)
        m_body = m_body.group(1)
        if m_body != '':
            return True
        else:
            return False

    @staticmethod
    def target_headline(data):
        invalid_headline = ['"headline": "TABLE-',
                            '"headline": "*TOP NEWS*',
                            '"headline": "DIARY-',
                            '"headline": "SHH Daily Margin Trading',
                            '"headline": "SHH Margin Trading',
                            '"headline": "North American power transmission outage update - PJM',
                            '"headline": "UPDATE 1',
                            '"headline": " BOJ:',
                            '"headline": "CRBIndex',
                            '"headline": "Asia Pacific Daily Earnings Hits & Misses',
                            '"headline": "CBOT agriculture futures est vol/open int -',
                            '"headline": "Rajkot Foodgrain Prices',
                            '"headline": "Rajkot Oilseeds Complex',
                            '"headline": "Rajkot Castor seeds',
                            '"headline": "Europe Daily Earnings Hits & Misses',
                            '"headline": "Power plant unit status -',
                            '"headline": "CBOT preliminary vol/open int totals for May 31"']
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
