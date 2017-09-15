import pcap
import dpkt


class Sniffer(object):
    def __init__(self, device, promiscuous=False):
        """
        :param device: The name of the device to sniff from
        :param promiscuous: Should the sniffer use promiscuous mode
        """
        self.sniffer = pcap.pcap(name=device, promisc=promiscuous)

    def __iter__(self):
        """
        :return: A tuple of timestamp and an ethernet frame
        """
        for result in self.sniffer:
            # Skip timeouts
            if result is None:
                continue

            # Convert the result to an ethernet frame
            timestamp, frame = result
            ethernet_frame = dpkt.ethernet.Ethernet(frame)
            yield timestamp, ethernet_frame

    def get_number_of_received_frames(self):
        received, _, _ = self.sniffer.stats()
        return received
