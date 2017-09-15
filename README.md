# Python winsniffer #

This is a simple network sniffer written in Python for Windows.
Its parsing engine can be easily extended to dissect new protocols, it also has a basic wxPython based GUI.

Example:
```python
sniffer = winsniffer.Sniffer(promiscuous=True)
for frame in sniffer:
    print(frame)
```
