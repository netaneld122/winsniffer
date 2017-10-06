import binascii

from winsniffer.gui.parsing.default_parser import DefaultParser


def prettify_mac_address(mac_address):
    return ':'.join(map(binascii.hexlify, mac_address))


def get_protocol_stack(frame):
    protocols = []
    while hasattr(frame, 'data'):
        protocols.append(frame.__class__.__name__)
        frame = frame.data
    return protocols


def find_parser(frame, data, parsers):
    protocol_stack_set = set(get_protocol_stack(frame))
    for parser in parsers:
        if parser.condition(protocol_stack_set, data):
            return parser
    return DefaultParser()


def get_unparsed_frame_data(frame):
    while not isinstance(frame, str):
        frame = frame.data
    return frame


def get_frame_data_preview(frame, parsers):
    data = get_unparsed_frame_data(frame)
    parser = find_parser(frame, data, parsers)
    try:
        parsed_data = parser.parse(frame, data)
    except Exception as e:
        import traceback
        parsed_data = traceback.format_exc()
    return len(data), parsed_data

