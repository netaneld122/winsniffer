import wx
import wx.py
import time
import threading
import winsniffer
import winsniffer.gui.frame_formatting as frame_formatting
import winsniffer.gui.ids as ids

from list_control import ListControl


class WinsnifferFrame(wx.Frame):
    def __init__(self, title):
        super(WinsnifferFrame, self).__init__(None, wx.ID_ANY, title, size=(1000, 700))

        # Create top level panel
        panel = wx.Panel(self)

        # Add list control
        self.list_control = ListControl(panel)
        self.list_control.SetBackgroundColour(wx.Colour(245, 245, 248))

        # Set a vertical sizer
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        vertical_sizer.Add(self.list_control, 1, wx.EXPAND)
        panel.SetSizer(vertical_sizer)

        self.set_tool_bar()

        # Set our columns
        self.set_columns(self.list_control)

        # Center the window
        self.Center()

        self.should_stop = True
        self.populate_list_thread = None

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def set_tool_bar(self):
        tool_bar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_NODIVIDER)

        image = wx.Bitmap("icons/ic_save_black_24dp_2x.png", wx.BITMAP_TYPE_ANY)
        tool_bar.AddTool(ids.ID_SAVE_BUTTON, "", image, wx.NullBitmap, wx.ITEM_NORMAL, "Save")

        image = wx.Bitmap("icons/ic_play_arrow_black_24dp_2x.png", wx.BITMAP_TYPE_ANY)
        tool_bar.AddTool(ids.ID_START_CAPTURING_BUTTON, "", image, wx.NullBitmap, wx.ITEM_NORMAL, "Start Capturing")

        image = wx.Bitmap("icons/ic_stop_black_24dp_2x.png", wx.BITMAP_TYPE_ANY)
        tool_bar.AddTool(ids.ID_STOP_CAPTURING_BUTTON, "", image, wx.NullBitmap, wx.ITEM_NORMAL, "Stop Capturing")

        image = wx.Bitmap("icons/ic_vertical_align_bottom_black_24dp_2x.png", wx.BITMAP_TYPE_ANY)
        tool_bar.AddTool(ids.ID_AUTO_SCROLL_BUTTON, "", image, wx.NullBitmap, wx.ITEM_NORMAL, "Auto scroll")

        tool_bar.AddStretchableSpace()

        image = wx.Bitmap("icons/ic_delete_sweep_black_24dp_2x.png", wx.BITMAP_TYPE_ANY)
        tool_bar.AddTool(ids.ID_CLEAR_BUTTON, "", image, wx.NullBitmap, wx.ITEM_NORMAL, "Clear")

        tool_bar.Realize()

        self.Bind(wx.EVT_TOOL, self.on_save, id=ids.ID_SAVE_BUTTON)
        self.Bind(wx.EVT_TOOL, self.on_start_capturing, id=ids.ID_START_CAPTURING_BUTTON)
        self.Bind(wx.EVT_TOOL, self.on_stop_capturing, id=ids.ID_STOP_CAPTURING_BUTTON)
        self.Bind(wx.EVT_TOOL, self.on_auto_scroll, id=ids.ID_AUTO_SCROLL_BUTTON)
        self.Bind(wx.EVT_TOOL, self.on_clear, id=ids.ID_CLEAR_BUTTON)

    def on_save(self, event):
        def doit():
            item_count = self.list_control.GetItemCount()
            column_count = self.list_control.GetColumnCount()
            output = ''
            for i in range(0, item_count):
                row = [self.list_control.GetItemText(i, j) for j in range(0, column_count)]
                output += ', '.join(row) + '\n'
            print(output)
        wx.CallAfter(doit)

    def on_start_capturing(self, event):
        if not self.should_stop:
            return

        self.should_stop = False

        if self.populate_list_thread is not None:
            self.populate_list_thread.join()
        self.populate_list_thread = threading.Thread(target=self.populate_list)
        self.populate_list_thread.start()

    def on_stop_capturing(self, event):
        self.should_stop = True

    def on_auto_scroll(self, event):
        item_count = self.list_control.GetItemCount()
        self.list_control.EnsureVisible(item_count - 1)

    def on_clear(self, event):
        self.list_control.DeleteAllItems()

    def on_close(self, event):
        self.should_stop = True
        self.Destroy()

    @staticmethod
    def set_columns(list_control):
        columns = (
            ('No.', 50),
            ('Time', 80),
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
        sniffer = winsniffer.Sniffer(winsniffer.get_all_devices()[3])
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


def show():
    app = wx.App()
    frame = WinsnifferFrame("Winsniffer 1.0 Pre-Alpha")
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    show()
