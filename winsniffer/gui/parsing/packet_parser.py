import binascii

from abc import ABCMeta, abstractmethod, abstractproperty


class PacketParser(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def condition(self, protocols, data):
        """
        Here you decide whether to parse the given packet.
        :param protocols: Set of the network protocol stack, for example: {'Ethernet', 'IP', 'TCP'}
        :param data: The raw data buffer of the last element in the network stack
        :return: bool
        """
        return False

    @abstractmethod
    def parse(self, frame, data):
        """
        :param frame: dpkt.ethernet.Ethernet
        :param data: The packet inner un-parsed raw data buffer
        :return: str with the parsed packet
        """
        return ' '.join(map(lambda s: binascii.hexlify(s).upper(), data))

    @staticmethod
    def ip(data):
        return '.'.join(str(ord(c)) for c in data)
