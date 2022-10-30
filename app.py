from distutils.log import debug
from flask import Flask, render_template, redirect, url_for, request
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('punkt')


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sim_score', methods=['GET', 'POST'])
def sim_score():
    stemmer = nltk.stem.porter.PorterStemmer()
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

    def stem_tokens(tokens):
        return [stemmer.stem(item) for item in tokens]

    '''remove punctuation, lowercase, stem'''
    def normalize(text):
        return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

    def cosine_sim(text1, text2):
        tfidf = vectorizer.fit_transform([text1, text2])
        output =  ((tfidf * tfidf.T).A)[0,1]
        return output
    
    if request.method == 'POST':
        text_1 = request.form.get('inp1')
        print(text_1)
        text_2 = request.form.get('inp2')
        print(text_2)
        outcome = cosine_sim(text_1, text_2)
        print(outcome)
        return render_template('index.html', score=outcome)

if __name__ == "__main__":
    app.run(debug=True)