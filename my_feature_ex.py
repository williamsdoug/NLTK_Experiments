import cmu_tweet_word_clusters
import nltk
from nltk.stem import WordNetLemmatizer

"""
Feature extraction routines:
- extract_tokens()            -- simple set of tokens, ignoring stop words and non-word tokens
- extract_lemmatize_tokens()  -- extends above using lemmatized tokens in place of actual tokens
- extract_bigrams()           -- bigrams of simple tokens using above filtering rules
- extract_lemmatize_bigrams() -- extends above using lemmatized tokens in place of actual tokens
"""

stop_words = nltk.corpus.stopwords.words('english')

#definition of categories can be found at: http://www.ark.cs.cmu.edu/TweetNLP/annot_guidelines.pdf
pos_nominal = ['N', 'O', '^', 'S', 'Z']
pos_noun = ['N', '^', 'Z']
pos_other_open_class = ['V', 'A', 'R', '!']
pos_other_closed_calss = ['D', 'P', '&', 'Y', 'X']
pos_twitter = ['#', '@', '~', 'U', 'E']
pos_misc = ['$', ',', 'G']
pos_compound = ['L', 'M', 'Y']
pos_all = pos_nominal + pos_other_open_class + pos_other_closed_calss + pos_twitter + pos_misc + pos_compound
pos_default_filter = set(pos_all).difference((',', 'U', 'G', 'E', '$'))

def filter_token(t,p,f, filter='default', exclude=[]):
    if filter == 'default':
        pos_filter = pos_default_filter
    elif filter == 'all':
        pos_filter = pos_all
    elif filter == 'nominal':
        pos_filter = pos_nominal
    elif filter == 'noun':
        pos_filter = pos_noun
    elif filter == 'twitter':
        pos_filter = pos_twitter
    elif filter == 'hashtag':
        pos_filter = ['#']        
    else:
        raise Error(filter)
    return t.lower() not in stop_words and t.lower() not in exclude and p in pos_filter

def reset_features(tweets):
    for tweet in tweets:
         tweet['tokens'] = []


def extract_tokens(tweets, filter='default', exclude=[]):
    for tweet in tweets:
         tweet['tokens'] = tweet['tokens'] + [t.lower() for t,p,f in tweet['pos'] if filter_token(t,p,f,filter=filter, exclude=exclude)]

def extract_lemmatize_tokens(tweets, filter='default', exclude=[]):
    wnl = WordNetLemmatizer()
    for tweet in tweets:
         tweet['tokens'] = tweet['tokens'] + [wnl.lemmatize(t.lower()) for t,p,f in tweet['pos'] if filter_token(t,p,f,filter=filter, exclude=exclude)]

def extract_group_tokens(tweets, filter='default', exclude=[]):
    for tweet in tweets:
         tweet['tokens'] = tweet['tokens'] + [cmu_tweet_word_clusters.cmu_classify(t.lower()) for t,p,f in tweet['pos'] if filter_token(t,p,f,filter=filter, exclude=exclude)]

def extract_bigrams(tweets, filter='default', exclude=[]):
    for tweet in tweets:
        bigrams = zip(tweet['pos'][0:-1], tweet['pos'][1:])
        tweet['tokens'] = tweet['tokens'] + ['{}_{}'.format(pos1[0].lower(), pos2[0].lower()) for pos1, pos2 in bigrams if filter_token(*pos1,filter=filter,exclude=exclude) and filter_token(*pos2,filter=filter,exclude=exclude)]
 
def extract_lemmatize_bigrams(tweets, filter='default', exclude=[]):
    wnl = WordNetLemmatizer()
    for tweet in tweets:
        bigrams = zip(tweet['pos'][0:-1], tweet['pos'][1:])
        tweet['tokens'] = tweet['tokens'] + ['{}_{}'.format(wnl.lemmatize(pos1[0].lower()), wnl.lemmatize(pos2[0].lower())) for pos1, pos2 in bigrams if filter_token(*pos1,filter=filter,exclude=exclude) and filter_token(*pos2,filter=filter,exclude=exclude)]
 
def extract_group_bigrams(tweets, filter='default', exclude=[]):
    wnl = WordNetLemmatizer()
    for tweet in tweets:
        bigrams = zip(tweet['pos'][0:-1], tweet['pos'][1:])
        tweet['tokens'] = tweet['tokens'] + ['{}_{}'.format(cmu_tweet_word_clusters.cmu_classify(pos1[0].lower()), cmu_tweet_word_clusters.cmu_classify(pos2[0].lower())) for pos1, pos2 in bigrams if filter_token(*pos1,filter=filter,exclude=exclude) and filter_token(*pos2,filter=filter,exclude=exclude)]
