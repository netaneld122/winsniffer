# Python Winsniffer #

This is a simple network sniffer written in Python for Windows, it comes along with a simple GUI.
Its parsing engine can be easily extended to dissect new protocols.

## Compiled Version Installation ##

- [Install](https://nmap.org/npcap/) the latest npcap version, upon installation specify the WinPcap compatibility flag
- [Download](https://bitbucket.org/netaneld122/winsniffer/downloads/winsniffer.zip), extract and run winsniffer.exe


## Library Usage ##
```python
import winsniffer

# Choose an appropriate device to sniff from
devices = winsniffer.get_all_devices()
device = devices[0]

sniffer = winsniffer.Sniffer(device, promiscuous=True, buffering=True)
for timestamp, frame in sniffer:
    print(timestamp, repr(frame))
```


## Graphical Interface ##


Choose the settings:

![alt Settings Dialog](https://i.imgur.com/vdqBQVD.png)

Start capturing:

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
