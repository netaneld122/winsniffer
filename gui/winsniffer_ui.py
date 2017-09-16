import wx
import wx.py
import time
import threading
import binascii
import winsniffer

from list_control import ListControl


class WinsnifferFrame(wx.Frame):
    def __init__(self, title):
        super(WinsnifferFrame, self).__init__(None, wx.ID_ANY, title, size=(850, 600))

        # Create top level panel
        panel = wx.Panel(self)

        # Add list control
        self.list_control = ListControl(panel)

        # Add python interpreter panel
        self.interpreter_panel = wx.py.crust.Crust(panel, size=(0, 250))

        # Set a vertical sizer
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        vertical_sizer.Add(self.list_control, 4, wx.EXPAND)
        vertical_sizer.Add(self.interpreter_panel, 1, wx.EXPAND)
        panel.SetSizer(vertical_sizer)

        # Set our columns
        self.set_columns(self.list_control)

        # Center the window
        self.Center()

        self.start_populating_list()

    @staticmethod
    def set_columns(list_control):
        columns = ('No.', 'Time', 'From', 'To', 'Stack[0]', 'Stack[1]', 'Stack[2]', 'Data')
        for column_index, column in enumerate(columns):
            list_control.InsertColumn(column_index, column, width=wx.LIST_AUTOSIZE)

    def start_populating_list(self):
        thread = threading.Thread(target=self.populate_list)
        thread.start()

    @staticmethod
    def prettify_mac_address(mac_address):
        return ':'.join(map(binascii.hexlify, mac_address))

    @staticmethod
    def prettify_frame_data(frame):
        protocol = frame
        while not isinstance(protocol, str):
            protocol = protocol.data
        return binascii.hexlify(protocol[:min(20, len(protocol) - 1)]).upper()

    @staticmethod
    def get_protocol_name(frame, depth):
        protocol = frame

        while hasattr(protocol, 'data') and depth > 0:
            if isinstance(protocol.data, str):
                return ''

            protocol = protocol.data
            depth -= 1

        return protocol.__class__.__name__

    def add_item(self, i, timestamp, frame):
        index = self.list_control.InsertItem(self.list_control.GetItemCount(), str(i + 1))
        self.list_control.SetItem(index, 1, str(timestamp))
        self.list_control.SetItem(index, 2, self.prettify_mac_address(frame.src))
        self.list_control.SetItem(index, 3, self.prettify_mac_address(frame.dst))
        self.list_control.SetItem(index, 4, self.get_protocol_name(frame, 0))
        self.list_control.SetItem(index, 5, self.get_protocol_name(frame, 1))
        self.list_control.SetItem(index, 6, self.get_protocol_name(frame, 2))
        self.list_control.SetItem(index, 7, self.prettify_frame_data(frame))

        # Auto scroll only when the user is scrolled to the bottom
        self.smart_auto_scroll()

    def smart_auto_scroll(self):
        scroll_position = self.list_control.GetScrollPos(wx.VERTICAL)
        visible_items_count = self.list_control.GetCountPerPage()
        scroll_bottom_position = scroll_position + visible_items_count
        item_count = self.list_control.GetItemCount()
        if scroll_bottom_position >= item_count - 2:
            self.list_control.EnsureVisible(item_count - 1)

    def populate_list(self):
        initial_timestamp = time.time()
        sniffer = winsniffer.Sniffer(winsniffer.get_all_devices()[3])
        for i, (timestamp, frame) in enumerate(sniffer):
            wx.CallAfter(self.add_item, i, timestamp - initial_timestamp, frame)


def main():
    app = wx.App()
    frame = WinsnifferFrame("Winsniffer 1.0 Alpha")
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
