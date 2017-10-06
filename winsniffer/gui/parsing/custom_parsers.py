from winsniffer.gui.parsing.packet_parser import PacketParser


class EchoParser(PacketParser):

    def condition(self, protocols, data):
        return {'ICMP'}.issubset(protocols) and data.startswith('abcdef')

    def parse(self, frame, data):
        return 'PING Echo was sent from {} to {}'.format(self.ip(frame.data.src), self.ip(frame.data.dst))


PARSERS = (
    EchoParser(),
)
