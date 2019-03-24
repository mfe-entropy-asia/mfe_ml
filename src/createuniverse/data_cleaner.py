# -*- coding: utf-8 -*-
import re
import numpy as np
import pandas as pd
import time
import pickle


class DataCleaner:
    def __init__(self, filtered):
        self.filtered = filtered
        self.m_data_series = pd.Series()
        self.find_body = re.compile('"body": "(.*?)", "mimeType"')
        self.find_time = re.compile('"versionCreated": "(.*?)"')
        self.find_keywords = re.compile(r'keywords:.*$', re.IGNORECASE)
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

    def __call__(self):
        print("%s entries", len(self.filtered.index))
        for each_time in self.filtered:
            for data_line in each_time:
                self.clean_up(data_line)

    def clean_up(self, data_line):
        m_body = self.find_body.search(data_line)
        m_body = m_body.group(1)
        m_time = self.find_time.search(data_line)
        m_time = m_time.group(1)
        m_time = np.datetime64(m_time[:10])
        if m_time not in self.m_data_series.index:
            self.m_data_series.at[m_time] = []
        self.m_data_series.at[m_time].append(self.data_clean(m_body))

    def data_clean(self, target: str):
        """
        Function which will do the data clean
        Remove the parentheses
        :param target: the input string data
        :return: string after data clean
        """
        target = self.remove_brackets(target)
        target = self.remove_header(target)
        target = self.remove_keywords(target)
        target = target.replace('\\n', ' ')\
            .replace('\\\"', '')\
            .replace('\\r', ' ')\
            .replace('*', '')\
            .replace('“', '')\
            .replace('”', '')
        return target.lower()

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

    def remove_keywords(self, data):
        return self.find_keywords.sub(r'', data)

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
