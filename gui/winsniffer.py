import wx
import wx.py
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

        # TODO: Remove
        for i in range(10):
            index = self.list_control.InsertItem(self.list_control.GetItemCount(), str(i+1))
            self.list_control.SetItem(index, 1, '0.0000')
            self.list_control.SetItem(index, 2, '127.0.0.1')
            self.list_control.SetItem(index, 3, '127.0.0.1')
            self.list_control.SetItem(index, 4, 'Ethernet')
            self.list_control.SetItem(index, 5, 'IP')
            self.list_control.SetItem(index, 6, 'TCP')
            self.list_control.SetItem(index, 7, '0x11 0x11 0x11 0x11 ...')

    @staticmethod
    def set_columns(list_control):
        columns = ('No.', 'Time', 'From', 'To', 'Data Link', 'Network', 'Transport', 'Data')
        for column_index, column in enumerate(columns):
            list_control.InsertColumn(column_index, column)


def main():
    app = wx.App()
    frame = WinsnifferFrame("Winsniffer 1.0 Alpha")
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    main()
