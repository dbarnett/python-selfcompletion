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

    def test_input_nothing_after_opt(self):
        word_options = self.parser.get_valid_next_words(['--value', ''])
        self.assertItemsEqual(word_options, [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        ])

class TestTakesManyIntsOrOptNothing(unittest.TestCase):
    def setUp(self):
        self.parser = selfcompletion.SelfCompletingArgumentParser()
        self.parser.add_argument('integers', metavar='N', type=int, nargs='+')
        self.parser.add_argument('--flag', action='store_true')

    def test_input_no_args(self):
        word_options = self.parser.get_valid_next_words([''])
        self.assertItemsEqual(word_options, [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                '-h ', '--help ',
                '--flag ',
                '--_completion ', '-- ',
            ])

    def test_input_nothing_after_opt(self):
        word_options = self.parser.get_valid_next_words(['--flag', ''])
        self.assertItemsEqual(word_options, [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                '-h ', '--help ',
                '--flag ',
                '--_completion ', '-- ',
        ])

class TestTakesManyOfChoice(unittest.TestCase):
    def setUp(self):
        self.parser = selfcompletion.SelfCompletingArgumentParser()
        self.parser.add_argument('strs', nargs='+', choices=['foo', 'bar', 'baz'])

    def test_input_no_args(self):
        word_options = self.parser.get_valid_next_words([''])
        self.assertItemsEqual(word_options, [
                'foo ', 'bar ', 'baz ',
                '-h ', '--help ',
                '--_completion ', '-- ',
            ])

    def test_input_letter_b(self):
        word_options = self.parser.get_valid_next_words(['b'])
        self.assertItemsEqual(word_options, [
                'bar ', 'baz ',
            ])

class TestTakesIntsOrOptMaybeArg(unittest.TestCase):
    def setUp(self):
        self.parser = selfcompletion.SelfCompletingArgumentParser()
        self.parser.add_argument('integers', metavar='N', type=int, nargs='+')
        self.parser.add_argument('--str', nargs='?', choices=['foo', 'bar', 'baz'])

    def test_input_no_args(self):
        word_options = self.parser.get_valid_next_words([''])
        self.assertItemsEqual(word_options, [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                '-h ', '--help ',
                '--str ',
                '--_completion ', '-- ',
            ])

    def test_input_nothing_after_opt(self):
        word_options = self.parser.get_valid_next_words(['--str', ''])
        self.assertItemsEqual(word_options, [
                'foo ', 'bar ', 'baz ',
                '-h ', '--help ',
                '--str ',
                '--_completion ', '-- ',
            ])

class TestTakesChoiceAThenChoiceB(unittest.TestCase):
    def setUp(self):
        self.parser = selfcompletion.SelfCompletingArgumentParser()
        self.parser.add_argument('a', choices=['a1', 'a2', 'a3'])
        self.parser.add_argument('b', choices=['b1', 'b2', 'b3'])

    def test_input_no_args(self):
        word_options = self.parser.get_valid_next_words([''])
        self.assertItemsEqual(word_options, [
                'a1 ', 'a2 ', 'a3 ',
                '-h ', '--help ',
                '--_completion ', '-- ',
            ])

    def test_input_nothing_after_a1(self):
        word_options = self.parser.get_valid_next_words(['a1', ''])
        self.assertItemsEqual(word_options, [
                'b1 ', 'b2 ', 'b3 ',
                '-h ', '--help ',
                '--_completion ', '-- ',
            ])

class TestTakesChoiceAThenChoiceBThenChoiceC(unittest.TestCase):
    def setUp(self):
        self.parser = selfcompletion.SelfCompletingArgumentParser()
        self.parser.add_argument('a', choices=['a1', 'a2', 'a3'])
        self.parser.add_argument('b', choices=['b1', 'b2', 'b3'])
        self.parser.add_argument('c', choices=['c1', 'c2', 'c3'])

    def test_input_no_args(self):
        word_options = self.parser.get_valid_next_words([''])
        self.assertItemsEqual(word_options, [
                'a1 ', 'a2 ', 'a3 ',
                '-h ', '--help ',
                '--_completion ', '-- ',
            ])

    def test_input_nothing_after_a1_b1(self):
        word_options = self.parser.get_valid_next_words(['a1', 'b1', ''])
        self.assertItemsEqual(word_options, [
                'c1 ', 'c2 ', 'c3 ',
                '-h ', '--help ',
                '--_completion ', '-- ',
            ])

class TestTakesStarChoiceAThenChoiceB(unittest.TestCase):
    def setUp(self):
        self.parser = selfcompletion.SelfCompletingArgumentParser()
        self.parser.add_argument('a', choices=['a1', 'a2', 'a3'], nargs='*', default='a1')
        self.parser.add_argument('b', choices=['b1', 'b2', 'b3'])

    def test_input_no_args(self):
        word_options = self.parser.get_valid_next_words([''])
        self.assertItemsEqual(word_options, [
                'a1 ', 'a2 ', 'a3 ',
                'b1 ', 'b2 ', 'b3 ',
                '-h ', '--help ',
                '--_completion ', '-- ',
            ])

class TestTakesOpt2Args(unittest.TestCase):
    def setUp(self):
        self.parser = selfcompletion.SelfCompletingArgumentParser()
        self.parser.add_argument('--values', type=int, nargs=2)

    def test_input_no_args(self):
        word_options = self.parser.get_valid_next_words([''])
        self.assertItemsEqual(word_options, [
                '--values ',
                '-h ', '--help ',
                '--_completion ', '-- ',
            ])

    def test_input_nothing_after_opt_arg(self):
        word_options = self.parser.get_valid_next_words(['--values', '1', ''])
        self.assertItemsEqual(word_options, [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            ])

class TestHandlesSubParsers(unittest.TestCase):
    def setUp(self):
        self.parser = selfcompletion.SelfCompletingArgumentParser()
        self.subparsers = self.parser.add_subparsers(help='commands')
        self.subparser = self.subparsers.add_parser('foo')
        self.subparser.add_argument('--something')

    def test_command(self):
        word_options = self.parser.get_valid_next_words([''])
        self.assertItemsEqual(word_options, [
                'foo ',
                '-h ', '--help ',
                '--_completion ', '-- ',
            ])

    def test_sub_command(self):
        word_options = self.parser.get_valid_next_words(['cmd', 'foo', ''])
        self.assertItemsEqual(word_options, [
                '--something ',
                '-h ', '--help ',
                '--_completion ', '-- ',
            ])
