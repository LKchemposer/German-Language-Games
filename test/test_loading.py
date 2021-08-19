import unittest
from unittest.mock import patch

from duolingo import DuolingoException
from src.database import Database


class TestLoading(unittest.TestCase):

    def test__load_duolingo(self):
        '''Good standard.'''
        database = Database()
        database.load_duolingo('./data/good_config.json')

        self.assertTrue(database.verbs)
        self.assertTrue(database.nouns)
        self.assertTrue(database.adjectives)

    def test__load_duolingo__wrong_username_password(self):
        '''File with bad/wrong username, password.'''
        database = Database()
        database.load_duolingo('./data/bad_config.json')

        self.assertRaises(DuolingoException)

    def test__load_duolingo__file_not_found(self):
        '''File doesn't exist.'''
        database = Database()
        database.load_duolingo('./data/nonexistent_config.json')

        self.assertRaises(FileNotFoundError)

    def test__load_pfverbs(self):
        '''Good standard.'''
        database = Database()
        database.load_pfverbs_csv('./data/good_pfverbs.csv')

        self.assertTrue(database.pfverbs)

    def test__load_pfverbs__file_not_found(self):
        '''File doesn't exist.'''
        database = Database()
        database.load_pfverbs_csv('./data/nonexistent_pfverbs.csv')

        self.assertRaises(FileNotFoundError)

    def test__load_pfverbs__empty_csv(self):
        '''No data.'''
        database = Database()
        database.load_pfverbs_csv('./data/empty_pfverbs.csv')

        self.assertRaises(Exception)

    def test__load_pfverbs__missing_parsable_columns(self):
        '''Missing headings to parse later.'''
        database = Database()
        database.load_pfverbs_csv('./data/missing_headings_pfverbs.csv')

        self.assertRaises(Exception)

    def test__save_vocab(self):
        '''Good strandard.'''
        database = Database()
        database.save_vocab_json('./data/vocab.json')

    def test__save_vocab__path_not_exists(self):
        '''Path doesn't exist.'''
        database = Database()
        database.save_vocab_json('./nonexistent_path/vocab.json')

        self.assertRaises(FileNotFoundError)

    def test__save_vocab__file_already_exists(self):
        '''If file already exists, confirm replace.'''
        database = Database()
        database.save_vocab_json('./data/replace_vocab.json')

        self.assertRaises(FileExistsError)

    def test__load_vocab(self):
        '''Good standard.'''
        database = Database()
        database.load_vocab_json('./data/vocab.json')

        self.assertTrue(database.verbs)
        self.assertTrue(database.nouns)
        self.assertTrue(database.adjectives)
        self.assertTrue(database.pfverbs)

    def test__load_vocab__file_not_found(self):
        '''Path doesn't exist.'''
        database = Database()
        database.load_vocab_json('./nonexistent_path/vocab.json')

        self.assertRaises(FileNotFoundError)


unittest.main()
