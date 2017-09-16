import wx
import wx.py
import threading
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
        columns = ('No.', 'Time', 'From', 'To', 'Data Link', 'Network', 'Transport', 'Data')
        for column_index, column in enumerate(columns):
            list_control.InsertColumn(column_index, column)

    def start_populating_list(self):
        thread = threading.Thread(target=self.populate_list)
        thread.start()

    def add_item(self, i):
        index = self.list_control.InsertItem(self.list_control.GetItemCount(), str(i + 1))
        self.list_control.SetItem(index, 1, '0.0000')
        self.list_control.SetItem(index, 2, '127.0.0.1')
        self.list_control.SetItem(index, 3, '127.0.0.1')
        self.list_control.SetItem(index, 4, 'Ethernet')
        self.list_control.SetItem(index, 5, 'IP')
        self.list_control.SetItem(index, 6, 'TCP')
        self.list_control.SetItem(index, 7, '0x11 0x11 0x11 0x11 ...')

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
        for i in range(1000):
            import time
            time.sleep(0.1)
            wx.CallAfter(self.add_item, i)


def main():
    app = wx.App()
    frame = WinsnifferFrame("Winsniffer 1.0 Alpha")
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
