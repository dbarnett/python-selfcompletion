try:
    import unittest2 as unittest
except ImportError, e:
    import unittest

import selfcompletion

class TestTakesNoArgs(unittest.TestCase):
    def setUp(self):
        self.parser = selfcompletion.SelfCompletingArgumentParser()

    def test_input_no_args(self):
        word_options = self.parser.get_valid_next_words([''])
        self.assertItemsEqual(word_options, [
                '-h ', '--help ',
                '--_completion ', '-- ',
            ])

    def test_input_single_dash(self):
        word_options = self.parser.get_valid_next_words(['-'])
        self.assertItemsEqual(word_options, [
                '-h ', '--help ',
                '--_completion ', '-- ',
            ])

    def test_input_invalid_letter(self):
        word_options = self.parser.get_valid_next_words(['a'])
        self.assertEqual(word_options, [])

class TestTakesManyInts(unittest.TestCase):
    def setUp(self):
        self.parser = selfcompletion.SelfCompletingArgumentParser()
        self.parser.add_argument('integers', metavar='N', type=int, nargs='+')

    def test_input_no_args(self):
        word_options = self.parser.get_valid_next_words([''])
        self.assertItemsEqual(word_options, [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                '-h ', '--help ',
                '--_completion ', '-- ',
            ])

    def test_input_one(self):
        word_options = self.parser.get_valid_next_words(['1'])
        self.assertItemsEqual(word_options, [
                '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
            ])

    def test_input_single_dash(self):
        word_options = self.parser.get_valid_next_words(['-'])
        self.assertItemsEqual(word_options, [
                '-h ', '--help ',
                '--_completion ', '-- ',
            ])

    def test_input_nothing_after_dashdash(self):
        word_options = self.parser.get_valid_next_words(['--', ''])
        self.assertItemsEqual(word_options, [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            ])

class TestTakesManyIntsOrOptInt(unittest.TestCase):
    def setUp(self):
        self.parser = selfcompletion.SelfCompletingArgumentParser()
        self.parser.add_argument('integers', metavar='N', type=int, nargs='+')
        self.parser.add_argument('--value', type=int)

    def test_input_no_args(self):
        word_options = self.parser.get_valid_next_words([''])
        self.assertItemsEqual(word_options, [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                '-h ', '--help ',
                '--value ',
                '--_completion ', '-- ',
            ])

