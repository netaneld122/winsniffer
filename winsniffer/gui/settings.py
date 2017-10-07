import os
import sys

import winsniffer.gui.parsing.custom_parsers as custom_parsers


class Settings(object):
    def __init__(self, parser_script_path, network_interface):
        self.parser_script_path = parser_script_path
        self.network_interface = network_interface


def get_default_parser_script_path():
    # Handle pyinstaller
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'custom_parsers.py')
    script_path = os.path.abspath(custom_parsers.__file__)
    if script_path.endswith('.pyc'):
        script_path = script_path.replace('.pyc', '.py')
    return script_path
