from data_cleaner import DataCleaner

dat_clean = DataCleaner("en", ["news.txt", "news.txt", "news.txt"], "en_output.dat")
dat_clean()
# tokens=word_tokenize(dat_clean.body_lst[5])
# print(tokens)
