import binascii


def prettify_mac_address(mac_address):
    return ':'.join(map(binascii.hexlify, mac_address))


def get_frame_data_preview(frame):
    protocol = frame

    while not isinstance(protocol, str):
        protocol = protocol.data

    threshold = 20

    data_preview = protocol[:min(threshold, len(protocol) - 1)]
    data_preview = ' '.join(map(lambda s: binascii.hexlify(s).upper(), data_preview))
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
