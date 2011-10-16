import argparse
import re

class SelfCompletingArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kw):
        argparse.ArgumentParser.__init__(self, *args, **kw)
        self._completion_parser = argparse.ArgumentParser()
        self._completion_parser.add_argument('--_completion', type=str)

    def parse_args(self, *args, **kw):
        comp_args = self._completion_parser.parse_args(*args, **kw)
        if comp_args._completion is not None:
            comp_words = re.split(r'\s+', comp_args._completion)
            comp_word = comp_words[-1]
            all_options = sum((a.option_strings for a in self._actions), [])
            types = [a.type for a in self._actions if a.nargs != 0 and a.type is not None]
            for opt in all_options:
                if opt.startswith(comp_word):
                    print opt+' '
            if int in types and re.match(r'^\d*$', comp_word):
                for i in xrange(10):
                    print i

            self.exit(0)
        else:
            return argparse.ArgumentParser.parse_args(self, *args, **kw)
