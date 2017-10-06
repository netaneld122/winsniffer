cd %~dp0
rmdir /S /Q build
rmdir /S /Q dist
del winsniffer.spec
pyinstaller winsniffer\gui\winsniffer_frame.py -n winsniffer --onefile --clean ^
 --add-binary dependencies\pcap.pyd;. ^
 --add-binary %systemroot%\SysWOW64\wpcap.dll;. ^
 --add-binary winsniffer\gui\icons;icons ^
 --add-data winsniffer\gui\parsing\custom_parsers.py;.