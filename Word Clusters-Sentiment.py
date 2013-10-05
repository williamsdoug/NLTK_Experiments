# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <rawcell>

# This is a refactoring of earlier Word Clusters, code moved to:
#     my_feature_ex.py
#     my_word_cloud.py

# <codecell>

%pylab inline
plt.rc('figure', figsize=(8, 8))

import cPickle as pickle

import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/')
sys.path.append('/Users/doug/SW_Dev/NLTK_Experiments/')

import pprint
import collections
import operator

import my_feature_ex as fx
import my_word_cloud as wcloud

# <codecell>

import nltk
import json
sys.path.append('/Users/doug/SW_Dev/ark-tweet-nlp-0.3.2')
import CMUTweetTagger
#print CMUTweetTagger.runtagger_parse(['example tweet 1', '@foo example tweet 2'])

RUN_TAGGER_CMD = "java -XX:ParallelGCThreads=2 -Xmx500m -jar /Users/doug/SW_Dev/ark-tweet-nlp-0.3.2/ark-tweet-nlp-0.3.2.jar"
RUN_TAGGER_CMD_PTB = "java -XX:ParallelGCThreads=2 -Xmx500m -jar /Users/doug/SW_Dev/ark-tweet-nlp-0.3.2/ark-tweet-nlp-0.3.2.jar --model /Users/doug/SW_Dev/ark-tweet-nlp-0.3.2/model.ritter_ptb_alldata_fixed.20130723.txt"
print CMUTweetTagger.runtagger_parse(['example tweet 1', 'example tweet 2'], run_tagger_cmd=RUN_TAGGER_CMD)
print CMUTweetTagger.runtagger_parse(['example tweet 1', 'example tweet 2'], run_tagger_cmd=RUN_TAGGER_CMD_PTB)

def annotate_pos(tweets, ptb=False):
    if ptb:
        tagger_cmd = RUN_TAGGER_CMD_PTB
    else:
        tagger_cmd = RUN_TAGGER_CMD
    ids = []
    texts = []
    for key, value in tweets.items():
        ids.append(key)
        texts.append(json.dumps({'text':value['text']}))
    pos = CMUTweetTagger.runtagger_parse(texts, run_tagger_cmd=tagger_cmd)
    
    if len(ids) != len(pos):
        raise Exception("Error: Tweet Tagger returned incorrect results") 

    for i in range(0, len(ids)):
        tweets[ids[i]]['pos'] = pos[i]
        tweets[ids[i]]['tokens'] = [tag[0] for tag in pos[i]]

    print pos[0]
    print [tag[0] for tag in pos[0]]

# <codecell>

def load_tweet_corpus(fname):
    tweets = dict()
    fd = open(fname)
    for json_text in fd:
        tweet = json.loads(json_text)['tweet']
        tweets[tweet['id_str']] = tweet
    print 'loaded'
    return tweets

def load_UCLA_tweet_corpus():
    fname = '/Users/doug/Desktop/NLP/sentiment/UCLA.json'
    return load_tweet_corpus(fname)

# <codecell>

UCLA_tweets = load_UCLA_tweet_corpus() 

annotate_pos(UCLA_tweets)
#annotate_pos(UCLA_tweets, ptb=True)

#subset_tweets = [t['text'] for t in UCLA_tweets.values()[:10]]
#pprint.pprint(CMUTweetTagger.runtagger_parse(subset_tweets))

# <codecell>

#import cPickle as pickle

#poutput = open('ucla_tweets.pkl', 'wb')
#pickle.dump(UCLA_tweets, poutput, -1)
#poutput.close()

# <codecell>

# load previously tokenized/clasified  tweet Corpus
#pinput = open('ucla_tweets.pkl', 'rb')
#UCLA_tweets = pickle.load(pinput)
#pinput.close()

# <codecell>

MAX_TWEETS = 100000   #subset Corpus for now to improve Clustering run time
tweet_set = [{'text':t['text'], 'pos':t['pos'], 'raw_tokens':t['tokens']} for t in UCLA_tweets.values()[0:MAX_TWEETS]]

# <codecell>

def compute_word_counts(tweet_set):
    wc = collections.defaultdict(int)
    for tweet in tweet_set:
        for tok in tweet['tokens']:
            wc[tok] += 1
    sorted_wc = sorted(wc.iteritems(), key=operator.itemgetter(1), reverse=True)
    sorted_wc = [val for val in sorted_wc if val[1]>1]   #prune singleton values
    #print len(sorted_wc)
    words = [word for word, count in sorted_wc]
    counts = [count for word, count in sorted_wc]
    return words, counts
    
def display_tweet_wordcloud(tweet_set):
    words, counts = compute_word_counts(tweet_set)
    words2 =  np.array(words[:200], np.dtype('string'))
    counts2 =  np.array(counts[:200], np.int32)
    wcloud.display_wordcloud(words2,counts2)

# <codecell>

#fx.reset_features(tweet_set)
#fx.extract_lemmatize_tokens(tweet_set, exclude=['#ucla'])
#display_tweet_wordcloud(tweet_set)

# <rawcell>

# Uses sentiment rule set in Table 3.2 of "Sentiment Analysis and Opinion Mining"  mapped from Penn Treebank POS to CMU Tweet POS

# <codecell>

# rules1 = (('A', 'N', ''),  ('R', 'V', '')) #uncond
# rules2 = (('R', 'A', 'N'), ('A', 'A', 'N'), ('N', 'A', 'N')) #cond

def get_sentiment_phrases_ptb(pos_list,lematize=False,include_pos=False):
    "Extracts sentiment phrases using approach in Liu: Sentiment Analysis and Opinion Mining sec 3.2"
    max = len(pos_list) - 1
    for i in range(0, max):
        first_tok, first_pos, first_conf = pos_list[i]
        second_tok, second_pos, second_conf = pos_list[i+1]
        third_is_noun = (i < max-1) and (pos_list[i+2][1] != 'NN') and (pos_list[i+2][1] != 'NNS')
        
        if ((first_pos == 'JJ' and (second_pos == 'NN' or second_pos == 'NNS')) or
            ((first_pos == 'RB' or first_pos == 'RBR' or first_pos == 'RBS') and 
             (second_pos == 'VB' or second_pos == 'VBD' or second_pos == 'VBN' or second_pos == 'VBG')) or
            ((first_pos == 'RB' or first_pos == 'RBR' or first_pos == 'RBS') and second_pos == 'JJ' and third_is_noun) or
            (first_pos == 'JJ' and second_pos == 'JJ' and third_is_noun) or
            ((second_pos == 'NN' or second_pos == 'NNS') and second_pos == 'JJ' and third_is_noun)):
            
            first_tok = first_tok.lower()
            second_tok = second_tok.lower()
            
            if include_pos:
                yield {'ft':first_tok, 'fp':first_pos, 'st':second_tok, 'sp':second_pos}
            else:
                yield '{} {}'.format(first_tok, second_tok)

def get_sentiment_phrases_cmu(pos_list,lematize=False,include_pos=False):
    "Extracts sentiment phrases using approach in Liu: Sentiment Analysis and Opinion Mining sec 3.2"
    max = len(pos_list) - 1
    for i in range(0, max):
        first_tok, first_pos, first_conf = pos_list[i]
        second_tok, second_pos, second_conf = pos_list[i+1]
        third_is_noun = (i < max-1) and (pos_list[i+2][1] != 'N')
        
        if ((first_pos == 'A' and second_pos == 'N') or
            (first_pos == 'R' and second_pos == 'V') or
            (first_pos == 'R' and second_pos == 'A' and third_is_noun) or
            (first_pos == 'A' and second_pos == 'A' and third_is_noun) or
            (first_pos == 'N' and second_pos == 'A' and third_is_noun)):
            
            first_tok = first_tok.lower()
            second_tok = second_tok.lower()
            
            if include_pos:
                yield {'ft':first_tok, 'fp':first_pos, 'st':second_tok, 'sp':second_pos}
            else:
                yield '{} {}'.format(first_tok, second_tok)

def extract_sentiment_bigrams_cmu(tweets,lematize=False):
    for tweet in tweets:
        tweet['tokens'] = tweet['tokens'] + [ val for val in get_sentiment_phrases_cmu(tweet['pos']) ]
        
def show_sentiment_bigrams_cmu(tweets,lematize=False):
    return [ [ val for val in get_sentiment_phrases_cmu(tweet['pos'], include_pos=False) ] for tweet in tweets]

# <codecell>

fx.reset_features(tweet_set)
show_sentiment_bigrams_cmu(tweet_set[:20])

# <codecell>

fx.reset_features(tweet_set)
#show_sentiment_bigrams(tweet_set[:20])
extract_sentiment_bigrams_cmu(tweet_set)
display_tweet_wordcloud(tweet_set)

# <rawcell>

# Try again using PTB tagging

# <codecell>

UCLA_tweets_ptb = load_UCLA_tweet_corpus() 

annotate_pos(UCLA_tweets_ptb, ptb=True)

#subset_tweets = [t['text'] for t in UCLA_tweets.values()[:10]]
#pprint.pprint(CMUTweetTagger.runtagger_parse(subset_tweets))

# <codecell>

MAX_TWEETS = 100000   #subset Corpus for now to improve Clustering run time
tweet_set = [{'text':t['text'], 'pos':t['pos'], 'raw_tokens':t['tokens']} for t in UCLA_tweets_ptb.values()[0:MAX_TWEETS]]

# <codecell>

def extract_sentiment_bigrams_ptb(tweets,lematize=False):
    for tweet in tweets:
        tweet['tokens'] = tweet['tokens'] + [ val for val in get_sentiment_phrases_ptb(tweet['pos']) ]
        
def show_sentiment_bigrams_ptb(tweets,lematize=False):
    return [ [ val for val in get_sentiment_phrases_ptb(tweet['pos'], include_pos=False) ] for tweet in tweets]

# <codecell>

fx.reset_features(tweet_set)
show_sentiment_bigrams_ptb(tweet_set[:20])

# <codecell>

fx.reset_features(tweet_set)
extract_sentiment_bigrams_ptb(tweet_set)
display_tweet_wordcloud(tweet_set)

# <codecell>


# <codecell>


