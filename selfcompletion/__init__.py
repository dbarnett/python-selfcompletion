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
    def __init__(self, add_completion=True, *args, **kw):
        super(SelfCompletingArgumentParser, self).__init__(*args, **kw)
        if add_completion:
            completion_action = _CompletionAction(['--_completion'])
            self._add_action(completion_action)

    def get_valid_next_words(self, words):
        valid_words = []
        types = []
        word_is_optarg = False
        positionals_valid = True
        for i in xrange(len(words) - 1):
            w = words[-1-(i+1)]
            if w in self._option_string_actions:
                action = self._option_string_actions[w]
                action_nargs = (1 if action.nargs is None else action.nargs)
                if action_nargs == i+1:
                    word_is_optarg = True
                    types.append(action.type)
                    break
                if i+1 == 1 and action.nargs == '?':
                    positionals_valid = False
                    types.append(action.type)
                    if action.choices:
                        valid_words.extend([c+' ' for c in action.choices])
                    break
        if not word_is_optarg:
            if '--' not in words[:-1]:
                valid_words.append('-- ')
                for a in self._actions:
                    valid_words.extend([o+' ' for o in a.option_strings])
            if positionals_valid:
                positionals = self._get_positional_actions()
                for i in xrange(len(words)-1):
                    if len(positionals) > 0 and positionals[0].nargs in (1, None):
                        # consume first positional
                        positionals = positionals[1:]
                for action in positionals:
                    choices = action.choices
                    if hasattr(action, 'add_parser'):
                        last = None
                        for word in reversed(words):
                            if len(word) and not word.startswith('-'):
                                last = word
                                break
                        if last in choices:
                            return choices[last].get_valid_next_words(words)
                    if action.type is not None:
                        types.append(action.type)
                    if choices:
                        valid_words.extend([c+' ' for c in choices])
                    if action.nargs in (None, 1):
                        break
        if int in types:
            if re.match(r'\d*$', words[-1]):
                valid_words = ['%s%d'%(words[-1], i) for i in xrange(10)] + valid_words
        valid_words = [w for w in valid_words if w.startswith(words[-1])]
        return valid_words
