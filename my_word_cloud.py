from sklearn.feature_extraction.text import CountVectorizer
import sys
sys.path.append('/Users/doug/SW_Dev/NLTK_Experiments/word_cloud-master/')
import wordcloud
import tempfile
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cbook as cbook

def compute_wordcloud_stats(sources):
    lines = []
    for s in sources:
        with open(s) as f:
            lines.extend(f.readlines())
    text = "".join(lines)

    cv = CountVectorizer(min_df=1, decode_error="ignore",
                         stop_words="english", max_features=200)
    counts = cv.fit_transform([text]).toarray().ravel()
    words = np.array(cv.get_feature_names())
    # throw away some words, normalize
    words = words[counts > 1]
    counts = counts[counts > 1]
    return words, counts

def display_wordcloud(words, counts):
    with tempfile.NamedTemporaryFile(suffix='.png') as tmp:
        temp_filename = tmp.name
        counts = wordcloud.make_wordcloud(words, counts, temp_filename, font_path='/Library/Fonts/Georgia.ttf',width=800, height=800, ranks_only=False)
        image_file = cbook.get_sample_data(temp_filename)
        image = plt.imread(image_file)

        fig, ax = plt.subplots()
        im = ax.imshow(image)
        plt.axis('off')
        plt.show()
