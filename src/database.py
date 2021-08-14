import pandas as pd
import duolingo
from pattern import de
import json


class Database():
    nouns: list = []
    verbs: list = []
    adjectives: list = []
    pfverbs: list = []

    def load_duolingo(self, username='KhoaLam12', password='Hnivaohk1'):
        duo = duolingo.Duolingo(username, password)
        vocab = duo.get_vocabulary('de')['vocab_overview']
        words = [(w['word_string'], w['pos'], w.get(
            'gender'), w.get('infinitive')) for w in vocab]

        df = pd.DataFrame(words, columns=['word', 'pos', 'gender', 'inf'])

        self.verbs = [v for v in df['inf'].unique() if v]
        self.adjectives = df[df['pos'] == 'Adjective']['word'].to_list()

        df['gender'] = df['gender'].apply(
            lambda v: v[0].lower() if v else None)
        df['noun'] = df.apply(lambda v: de.singularize(
            v['word']).lower() if v['pos'] == 'Noun' else None, axis=1)
        self.nouns = df[df['pos'] == 'Noun'][[
            'noun', 'gender']].to_dict('records')

    # def load_duolingo_dev(self):
    #     self.nouns = [{'noun': 'Hund', 'gender': 'm'}, {
    #         'noun': 'Katze', 'gender': None}, {'noun': 'Kind', 'gender': 'n'}]
    #     self.verbs = ['sein', 'kochen', 'essen']
    #     self.adjectives = ['schön', 'traurig', 'neugierig']

    def load_pfverbs_csv(self, csv_path='../data/pfverbs.csv'):
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.lower()
        self.pfverbs = df.to_dict('records')

    def save_vocab_json(self, vocab_path: str = '../data/vocab.json'):
        vocab = dict(zip(['nouns', 'verbs', 'adjectives', 'pfverbs'], [
                     self.nouns, self.verbs, self.adjectives, self.pfverbs]))
        with open(vocab_path, 'w') as js:
            js.write(json.dumps(vocab))

    def load_vocab_json(self, vocab_path: str = '../data/vocab.json'):
        with open(vocab_path, 'r') as js:
            vocab = json.load(js)

        self.nouns, self.verbs, self.adjectives, self.pfverbs = vocab.values()
