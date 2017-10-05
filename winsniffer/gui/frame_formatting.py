import binascii
import string

from winsniffer.gui.parsing.custom_parsers import ALL_PARSERS
from winsniffer.gui.parsing.default_parser import DefaultParser


def prettify_mac_address(mac_address):
    return ':'.join(map(binascii.hexlify, mac_address))


def get_protocol_name(frame, depth):
    protocol = frame

    while hasattr(protocol, 'data') and depth > 0:
        if isinstance(protocol.data, str):
            return ''

        protocol = protocol.data
        depth -= 1

    return protocol.__class__.__name__


def find_parser(frame, data):
    protocol_stack_set = {
        get_protocol_name(frame, 0),
        get_protocol_name(frame, 1),
        get_protocol_name(frame, 2),
        get_protocol_name(frame, 3)
    }

    for parser in ALL_PARSERS:
        if parser.condition(protocol_stack_set, data):
            return parser
    return DefaultParser()


def get_unparsed_frame_data(frame):
    while not isinstance(frame, str):
        frame = frame.data
    return frame


def get_frame_data_preview(frame):
    data = get_unparsed_frame_data(frame)
    parser = find_parser(frame, data)
    return len(data), parser.parse(frame, data)

