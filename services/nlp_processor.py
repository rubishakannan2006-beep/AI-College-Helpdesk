import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

_nlp_ready = False

def ensure_nltk():
    global _nlp_ready
    if _nlp_ready:
        return
    try:
        nltk.data.find('tokenizers/punkt')
    except Exception:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except Exception:
        nltk.download('stopwords')
    _nlp_ready = True


def preprocess(text):
    ensure_nltk()
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", ' ', text)
    tokens = nltk.word_tokenize(text)
    stops = set(stopwords.words('english'))
    ps = PorterStemmer()
    tokens = [ps.stem(t) for t in tokens if t not in stops]
    return ' '.join(tokens)
