def calculate_entropy(input_ngram_dict, ngram_model):
    sum_of_counts = sum(input_ngram_dict.values())
    entropy = 0
    for ngram in input_ngram_dict:
        if ngram_model.score[ngram[-1], list(ngram[0:3])] == 0:
            mi = 0.25
        else:
            mi = ngram.logscore[ngram[-1], list(ngram[0:3])]
        pi = input_ngram_dict[ngram] / sum_of_counts
    entropy += -pi * mi
    return entropy


def calculate_sent_pos(input_ngram_dict):
    sum_of_pos = 0
    for ngram in input_ngram_dict:
        if is_pos(ngram):
            sum_of_pos += input_ngram_dict[ngram]
        sent_pos = sum_of_pos / sum(input_ngram_dict.values())
    return sent_pos


def is_pos(ngram):
    return True
