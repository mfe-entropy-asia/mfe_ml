from nltk.lm import MLE
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import time
import pickle
import string
import numpy as np
from functools import partial
from multiprocessing import Pool


def train_fourgram_model(text_body, mle_model):
        translator = str.maketrans('', '', string.punctuation)
        training_content = []
        training_content += [word_tokenize(sentence.translate(translator)) for sentence in sent_tokenize(text_body)]
        every_gram, vocab = padded_everygram_pipeline(4, training_content)  # This will generate unigram, bigram,
        three_gram = []
        four_gram = []
        for sent in list(every_gram):
            for item in sent:
                if len(item) == 3:
                    three_gram.append(item)
                elif len(item) == 4:
                    four_gram.append(item)
        train = [three_gram, four_gram]
        mle_model.vocab.update(vocab)
        mle_model.fit(train)

# def train_daily_data(input_dict, day, model):
#     training_content = ''
#     for text_body in input_dict[day]:
#         training_content += text_body
#     train_fourgram_model(training_content, model)
#
#
# def train_monthly_data(input_dict, month, model):
#     # training_content = ''
#     date_of_that_month = [key for key in input_dict if
#                           key.astype('datetime64[M]') == month]
#     for month_date in date_of_that_month:
#         # for body in input_dict[month_date]:
#         #     training_content += body
#         train_daily_data(input_dict, month_date, model)

    # train_fourgram_model(training_content, model)


def gen_daily_data_corpus(input_dict, day):
    training_content = ''
    for text_body in input_dict[day]:
        training_content += text_body
    return training_content


def gen_monthly_corpus(input_dict, month):
    training_content = ''
    date_of_that_month = [key for key in input_dict if
                          key.astype('datetime64[M]') == month]
    for month_date in date_of_that_month:
        for body in input_dict[month_date]:
            training_content += body
    print("Generation completed")
    return training_content


def gen_7day_corpus(input_dict, day):
    training_content = ''
    for i in range(1, 8):
        # training_content += gen_daily_data_corpus(input_dict, day-i)
        for text_body in input_dict[day-i]:
            training_content += text_body
    print("Generation completed")
    return training_content


if __name__ == '__main__':
    model1 = MLE(4)
    pickle_in = open("../../data/intermediate/cleaned_series_multiple_process.pickle", "rb")
    processed_news_data_frame = pickle.load(pickle_in)
    print(type(processed_news_data_frame))
    pickle_in.close()
    # Train as all the bodies chained
    start = time.time()
    print("Fitting model1 for date: 2018-06-01 \n")
    train_fourgram_model(gen_daily_data_corpus(processed_news_data_frame, np.datetime64('2018-06-01')), model1)
    end = time.time()
    print("Model1 for date: 2018-06-01  has been fitted \n" +
          "Time taking: " + str(end - start) + "\n")

    # # Train as all the bodies chained for month
    # model2 = MLE(4)
    # start = time.time()
    # print("=====================================\n" +
    #       "Fitting model2 for month: " + '2018-06' +
    #       "...\n=====================================\n")
    # monthly_training_corpus = gen_monthly_corpus(processed_news_data_frame, np.datetime64('2018-06'))
    # train_fourgram_model(monthly_training_corpus, model2)
    # end = time.time()
    # print("===============================================\n" +
    #       "Model2 for month: " + '2018-06' + " has been fitted!!!!!! \n" +
    #       "Time taking: " + str(end - start) + "\n"
    #                                            "===============================================\n")

    # Train 7 days ahead 2018-06-08
    model3 = MLE(4)
    weekly_training_corpus = gen_7day_corpus(processed_news_data_frame, np.datetime64('2018-06-08'))
    start = time.time()
    print("Fitting model3 for 7days before: 2018-06-08 \n")
    train_fourgram_model(weekly_training_corpus, model3)
    end = time.time()
    print("Model3 for 7 days before: 2018-06-08 has been fitted \n" +
          "Time taking: " + str(end - start) + "\n")
    print(model1.counts[4])
    # print(model2.counts[4])
    print(model3.counts[4])




