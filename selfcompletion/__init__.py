import argparse
import re

class _CompletionAction(argparse.Action):
    def __init__(self,
                 option_strings,
                 dest='_completion',
                 metavar='CMD_LINE',
                 default=argparse.SUPPRESS,
                 help="Built-in command completion"):
        super(_CompletionAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            metavar=metavar,
            default=default,
            nargs=None,
            type=str,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        comp_words = re.split(r'\s+', values.lstrip())
        for valid_word in parser.get_valid_next_words(comp_words):
            print valid_word
        parser.exit()

class _StoreAction(argparse._StoreAction):
    def __eq__(self, other):
        return vars(self) == vars(other)

class SelfCompletingArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kw):
        super(SelfCompletingArgumentParser, self).__init__(*args, **kw)
        completion_action = _CompletionAction(['--_completion'])
        self._add_action(completion_action)

    def get_valid_next_words(self, words):
        valid_words = []
        if '--' not in words[:-1]:
            valid_words.append('-- ')
            for a in self._actions:
                valid_words.extend([o+' ' for o in a.option_strings])
        positionals = self._get_positional_actions()
        valid_words = [w for w in valid_words if w.startswith(words[-1])]
        if any(p.type == int for p in positionals):
            if re.match(r'\d*$', words[-1]):
                valid_words = ['%d'%(i,) for i in xrange(10)] + valid_words
        return valid_words
