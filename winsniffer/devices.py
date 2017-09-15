import pcap


def get_all_devices():
    return pcap.findalldevs()
