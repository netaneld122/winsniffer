import os
import sys


class ParserLoader(object):
    def __init__(self, settings):
        self.parsers = []
        self.settings = settings

    def reload(self):
        try:
            # The script must set the local PARSERS
            script_locals = dict()
            execfile(self.settings.parser_script_path, dict(), script_locals)
            assert 'PARSERS' in script_locals, "The parser script {} did not define PARSERS".format(
                self.settings.parser_script_path)
            self.parsers = script_locals['PARSERS']
            print('Reloaded parsers: ' + str(self.parsers))
        except RuntimeError:
            import traceback
            print traceback.format_exc()

    def get_parsers(self):
        return self.parsers
