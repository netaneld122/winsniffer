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
