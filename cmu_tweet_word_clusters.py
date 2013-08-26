#use  CMU tweet work group clusters
#source: http://www.ark.cs.cmu.edu/TweetNLP/clusters/50mpaths2

DEFAULT_PATH = '/Users/doug/SW_Dev/NLTK_Experiments/cmu_ark_50mpaths2.txt'

def load_word_clusters(path=DEFAULT_PATH):
    result = {}
    # load previously tokenized/clasified  tweet Corpus
    for line in open(path, 'rb'):
        tokens = line.split()
        if len(tokens) == 3:
            result[tokens[1]] = tokens[0]
        else:
            print 'skipped: ', line
    return result
CMU_WORD_GROUPS = load_word_clusters()

def cmu_classify(word):
    if word in CMU_WORD_GROUPS:
        return CMU_WORD_GROUPS[word]
    else:
        return word
