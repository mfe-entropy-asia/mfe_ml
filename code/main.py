from data_cleaner import DataCleaner
# from nltk import ngrams
# from nltk import FreqDist
# from nltk import word_tokenize
# from nltk import sent_tokenize
# from nltk import Text
dat_clean = DataCleaner("en", ["./data/raw/News.RTRS.201806.0214.txt"], "./data/intermediate/")
dat_clean()
# for i in range(8):
#     print(dat_clean.headline_lst[i])
# tokens = [word_tokenize(sentence) for sentence in sent_tokenize(dat_clean.body_lst[4])]
# for i in tokens:
#     print(i)

for key in dat_clean.m_dict:
    print(dat_clean.m_dict[key][3])