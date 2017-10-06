# Python Winsniffer #

This is a simple network sniffer written in Python for Windows, it comes along with a simple GUI.
Its parsing engine can be easily extended to dissect new protocols.

Usage:
```python
import winsniffer

# Choose an appropriate device to sniff from
devices = winsniffer.get_all_devices()
device = devices[0]

sniffer = winsniffer.Sniffer(device, promiscuous=True, buffering=True)
for timestamp, frame in sniffer:
    print(timestamp, repr(frame))
```


Graphical Interface:


![alt Winsniffer GUI](https://i.imgur.com/fFYqwk8.png)

Define your custom parser:

*custom_parser.py*
```python
from winsniffer.gui.parsing.packet_parser import PacketParser


class EchoParser(PacketParser):

    def condition(self, protocols, data):
        return {'ICMP'}.issubset(protocols) and data.startswith('abcdef')

    def parse(self, frame, data):
        return 'PING Echo was sent from {} to {}'.format(self.ip(frame.data.src), self.ip(frame.data.dst))


PARSERS = (
    EchoParser(),
)
```


Observe the changes as new packets are sniffed:

![alt Winsniffer GUI](https://i.imgur.com/hML2eZ3.png)


