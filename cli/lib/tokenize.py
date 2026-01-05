import string

from lib.utils import load_stopwords
from nltk.stem import PorterStemmer


def tokenize_str(query: str) -> set[str]:
    clean_query = remove_punctuation(query)
    clean_query = remove_stopwords(clean_query)
    return stemed_tokens(clean_query)


def remove_punctuation(query: str) -> str:
    punctuation_table = str.maketrans("", "", string.punctuation)
    return query.lower().translate(punctuation_table)


def remove_stopwords(query: str) -> list[str]:
    stopwords = load_stopwords()
    return [word for word in query.split() if word not in stopwords]


def stemed_tokens(tokens: list[str]) -> set:
    stemmer = PorterStemmer()
    return set([stemmer.stem(word) for word in tokens])
