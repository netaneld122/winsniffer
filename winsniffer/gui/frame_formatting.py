import binascii
import string


def prettify_mac_address(mac_address):
    return ':'.join(map(binascii.hexlify, mac_address))


def is_printable(_string):
    return all(c in string.printable for c in _string)


def get_frame_data_preview(frame):
    protocol = frame

    while not isinstance(protocol, str):
        protocol = protocol.data

    threshold = 40

    data_preview = protocol[:min(threshold, len(protocol) - 1)]

    if protocol == '\x00':
        data_preview = '00'
    elif len(protocol) > 0 and is_printable(data_preview):
        data_preview = unicode(data_preview)
    else:
        data_preview = ' '.join(map(lambda s: binascii.hexlify(s).upper(), data_preview))

    # We truncated the data so add a ... indicator for that
    if len(protocol) > threshold:
        data_preview += "..."

    return len(protocol), data_preview


def get_protocol_name(frame, depth):
    protocol = frame

    while hasattr(protocol, 'data') and depth > 0:
        if isinstance(protocol.data, str):
            return ''

        protocol = protocol.data
        depth -= 1

    return protocol.__class__.__name__
