# Python winsniffer #

This is a simple network sniffer written in Python for Windows.
The parsing engine can be easily extended to dissect new protocols.

Usage:
```python
import winsniffer

sniffer = winsniffer.Sniffer(promiscuous=True)
for frame in sniffer:
    print(frame)
```
