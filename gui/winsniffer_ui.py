import wx
import wx.py
import time
import threading
import winsniffer
import frame_formatting

from list_control import ListControl


class WinsnifferFrame(wx.Frame):
    def __init__(self, title):
        super(WinsnifferFrame, self).__init__(None, wx.ID_ANY, title, size=(1000, 700))

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

        self.should_stop = False

        self.populate_list_thread = threading.Thread(target=self.populate_list)
        self.populate_list_thread.start()

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.should_stop = True
        self.populate_list_thread.join(timeout=2)
        self.Destroy()

    @staticmethod
    def set_columns(list_control):
        columns = (
            ('No.', 50),
            ('Time', 70),
            ('From', 110),
            ('To', 110),
            ('Stack[0]', 70),
            ('Stack[1]', 70),
            ('Stack[2]', 70),
            ('Length', 70),
            ('Data Preview', wx.LIST_AUTOSIZE)
        )
        for column_index, (column, width) in enumerate(columns):
            list_control.InsertColumn(column_index, column, width=width)

    def add_item(self, row):
        index = self.list_control.InsertItem(self.list_control.GetItemCount(), str(row[0]))
        for i, value in enumerate(row[1:]):
            self.list_control.SetItem(index, i + 1, str(value))

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
        sniffer = winsniffer.Sniffer(winsniffer.get_all_devices()[1])
        for i, (timestamp, frame) in enumerate(sniffer):
            if self.should_stop:
                break

            length, data_preview = frame_formatting.get_frame_data_preview(frame)
            row = (
                i + 1,
                "{0:.7f}".format(timestamp - initial_timestamp),
                frame_formatting.prettify_mac_address(frame.src),
                frame_formatting.prettify_mac_address(frame.dst),
                frame_formatting.get_protocol_name(frame, 0),
                frame_formatting.get_protocol_name(frame, 1),
                frame_formatting.get_protocol_name(frame, 2),
                str(length) + " Bytes",
                data_preview
            )
            wx.CallAfter(self.add_item, row)


def main():
    app = wx.App()
    frame = WinsnifferFrame("Winsniffer 1.0 Pre-Alpha")
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
