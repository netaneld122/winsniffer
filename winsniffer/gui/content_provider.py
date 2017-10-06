import wx
import time
import winsniffer
import winsniffer.gui.frame_formatting as frame_formatting


class ContentProvider(object):
    def __init__(self):
        self.initial_timestamp = time.time()
        self.sniffer = winsniffer.Sniffer(winsniffer.get_all_devices()[3], buffering=True, timeout_ms=100)
        self.index = 0
        self.should_stop = False

    @staticmethod
    def get_columns():
        return (
            ('[ ]', 50),
            ('Time', 80),
            ('From', 110),
            ('To', 110),
            ('Stack[0]', 70),
            ('Stack[1]', 70),
            ('Stack[2]', 70),
            ('Length', 70),
            ('Data Preview', wx.LIST_AUTOSIZE)
        )

    def get_next_result(self):
        result = next(self.sniffer)
        if result is None:
            return None

        timestamp, frame = result
        length, data_preview = frame_formatting.get_frame_data_preview(frame)
        protocol_stack = frame_formatting.get_protocol_stack(frame) + [''] * 2
        row = (
            self.index,
            "{0:.7f}".format(timestamp - self.initial_timestamp),
            frame_formatting.prettify_mac_address(frame.src),
            frame_formatting.prettify_mac_address(frame.dst),
            protocol_stack[0],
            protocol_stack[1],
            protocol_stack[2],
            str(length) + " Bytes",
            data_preview
        )
        self.index += 1
        return row, frame
