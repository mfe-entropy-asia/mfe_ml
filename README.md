MFE Machine learning  project documentation
================================================

## Project title: "***Does unusual news forecast market pressure***"
The project meant to replicate the work done by the referred paper. The code mainly contains three parts:
1. Data cleaning: This part is to do the data pre-process and pass the clean data to the n-gram model
2. Ngram model: This part is to build the n-gram model, pass the training data set and generate the sentiment-entropy output.
3. Financial model: This part is to use the output of the model to do some financial forecasting


### Data cleaning
Exclude non-English news, tables and useless information

### Model
4-gram model

### Financial model
Multi-factor model


## Useful links:
https://www.nltk.org/api/nltk.lm.html#module-nltk.lm <br/>
https://stackoverflow.com/questions/37504391/train-ngrammodel-in-python

## 1st meeting minutes
Date: 2/3/2019 \
Attendees: ZZZF, LY, FZK, ZTY \
TO-DOs:
1. pre-process
	0. to use 61's preprocess code
	1. to filter news based on target company(GS for instance)
	2. to replace full name with ticker(To define the list of what to be replaced)
	3. to tokenize (one liner, NLTK should be able to do the job)
2. to calculate entropy - use lib to count 4-gram
3. sentiment analysis (use mock data to start parallely)

## 2nd meeting minutes
Date: 17/3/2019

## Final meeting
Date: 7/4/2019
