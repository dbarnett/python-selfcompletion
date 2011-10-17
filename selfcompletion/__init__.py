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
        comp_words = re.split(r'\s+', values)
        comp_word = comp_words[-1]
        all_options = sum((a.option_strings for a in parser._actions), [])
        types = [a.type for a in parser._actions if a.nargs != 0 and a.type is not None]
        for opt in all_options:
            if opt.startswith(comp_word):
                print opt+' '
        if int in types and re.match(r'^\d*$', comp_word):
            for i in xrange(10):
                print i
        parser.exit()

class SelfCompletingArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kw):
        super(SelfCompletingArgumentParser, self).__init__(*args, **kw)
        completion_action = _CompletionAction(['--_completion'])
        self._add_action(completion_action)
