from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import numpy as np
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('punkt')


app = Flask(__name__)
api = Api(app)


stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))


vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')


def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


parser = reqparse.RequestParser()
parser.add_argument('text1')
parser.add_argument('text2')


class Calculate_score(Resource):
    def get(self):
        args = parser.parse_args()
        text_1 = args['text1']
        text_2 = args['text2']

        output = {'similarity score': cosine_sim(text_1, text_2)}
        return output


api.add_resource(Calculate_score, '/')


if __name__ == '__main__':
    app.run(debug=True)