import unittest
import winsniffer


class TestSniffer(unittest.TestCase):

    def test_sanity(self):
        devices = winsniffer.get_all_devices()
        sniffer = winsniffer.Sniffer(devices[3])
        for timestamp, frame in sniffer:
            self.assertGreaterEqual(sniffer.get_number_of_received_frames(), 1)
            break
