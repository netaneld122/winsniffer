import pcap
import dpkt


class Sniffer(object):
    def __init__(self, device, promiscuous=False, buffering=False, timeout_ms=0):
        """
        :param device: The name of the device to sniff from
        :param promiscuous: Should the sniffer use promiscuous mode
        :param buffering: Should use buffering
        :param timeout_ms: Timeout in ms, when a timeout occurs next() will return None, 0 is no timeout
        """
        self.sniffer = pcap.pcap(name=device, promisc=promiscuous, immediate=not buffering, timeout_ms=timeout_ms)

    def next(self):
        """
        :return: A tuple of timestamp and dpkt.ethernet.Ethernet frame or None on a timeout
        """

        result = next(self.sniffer)
        if result is None:
            return None

        # Convert the result to an ethernet frame
        timestamp, frame = result
        ethernet_frame = dpkt.ethernet.Ethernet(frame)
        return timestamp, ethernet_frame

    def __iter__(self):
        return self

    def get_number_of_received_frames(self):
        received, _, _ = self.sniffer.stats()
        return received
