import os

import winsniffer.gui.parsing.custom_parsers as custom_parsers


class ParserLoader(object):
    def __init__(self):
        self.parsers = []
        self.script_path = self._default_parser_script_path

    def reload(self, parsers_python_script_path=None):
        if parsers_python_script_path is not None:
            self.script_path = parsers_python_script_path
        try:
            # The script must set the local PARSERS
            locals = dict()
            execfile(self.script_path, dict(), locals)
            assert 'PARSERS' in locals, "The parser script {} did not define PARSERS".format(self.script_path)
            self.parsers = locals['PARSERS']
            print 'Reloaded parsers:', self.parsers
        except RuntimeError:
            import traceback
            print traceback.format_exc()

    def get_parsers(self):
        return self.parsers

    @property
    def _default_parser_script_path(self):
        return os.path.abspath(custom_parsers.__file__)

    @property
    def parser_script_path(self):
        return self.script_path
