import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer, WordNetLemmatizer


class TextPreprocessor:
    def __init__(self, method='stemming'):
        self.method = method
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def preprocess(self, text):
        text = self.to_lowercase(text)
        text = self.remove_non_words(text)
        text = self.remove_numbers(text)
        text = self.remove_specific_word(text, word='wsba')
        tokens = self.tokenize(text)
        tokens = self.filter_single_letters(tokens)
        tokens = self.remove_stopwords(tokens)
        if self.method == 'stemming':
            tokens = self.stem_words(tokens)
        elif self.method == 'lemmatization':
            tokens = self.lemmatize_tokens(tokens)
        return ' '.join(tokens)  # Return processed text as a single string

    @staticmethod
    def to_lowercase(text):
        return text.lower()

    @staticmethod
    def remove_non_words(text):
        return pd.Series(text).replace(to_replace=r'[^\w\s]', value='', regex=True).item()

    @staticmethod
    def remove_numbers(text):
        return pd.Series(text).replace(to_replace=r'\d', value='', regex=True).item()

    @staticmethod
    def remove_specific_word(text, word):
        return ' '.join([t for t in text.split() if t.lower() != word])

    @staticmethod
    def tokenize(text):
        return word_tokenize(text)

    @staticmethod
    def filter_single_letters(tokens):
        return [token for token in tokens if len(token) > 1]

    def remove_stopwords(self, tokens):
        return [word for word in tokens if word not in self.stop_words]

    def stem_words(self, tokens):
        return [self.stemmer.stem(word) for word in tokens]

    def lemmatize_tokens(self, tokens):
        def get_wordnet_pos(word):
            tag = nltk.pos_tag([word])[0][1][0].upper()
            tag_dict = {"J": wordnet.ADJ, "N": wordnet.NOUN, "V": wordnet.VERB, "R": wordnet.ADV}
            return tag_dict.get(tag, wordnet.NOUN)
        return [self.lemmatizer.lemmatize(token, get_wordnet_pos(token)) for token in tokens]
