import wx
import wx.py
import threading

import winsniffer.gui.ids as ids
import winsniffer.gui.icons as icons

from winsniffer.gui.content_provider import ContentProvider
from winsniffer.gui.list_control import ListControl


class WinsnifferFrame(wx.Frame):
    def __init__(self, title):
        super(WinsnifferFrame, self).__init__(None, wx.ID_ANY, title, size=(1000, 700))

        # Create top level panel
        panel = wx.Panel(self)

        # Add list control
        self.content_provider = ContentProvider()
        self.list_control = ListControl(panel, self.content_provider)
        self.list_control.SetBackgroundColour(wx.Colour(245, 245, 248))

        # Set a vertical sizer
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        vertical_sizer.Add(self.list_control, 1, wx.EXPAND)
        panel.SetSizer(vertical_sizer)

        self.set_tool_bar()

        # Center the window
        self.Center()

        self.should_stop = True
        self.capture_thread = None

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def set_tool_bar(self):
        tool_bar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_NODIVIDER)

        # Define buttons
        tool_bar.AddTool(ids.ID_SAVE_BUTTON, "", wx.Bitmap(icons.SAVE), wx.NullBitmap, wx.ITEM_NORMAL,
                         "Save")
        tool_bar.AddTool(ids.ID_TOGGLE_CAPTURING_BUTTON, "", wx.Bitmap(icons.START), wx.NullBitmap, wx.ITEM_NORMAL,
                         "Start Capturing")
        tool_bar.AddTool(ids.ID_AUTO_SCROLL_BUTTON, "", wx.Bitmap(icons.AUTO_SCROLL), wx.NullBitmap, wx.ITEM_NORMAL,
                         "Auto scroll")
        tool_bar.AddStretchableSpace()
        tool_bar.AddTool(ids.ID_CLEAR_BUTTON, "", wx.Bitmap(icons.CLEAR), wx.NullBitmap, wx.ITEM_NORMAL, "Clear")

        # Draw the tool bar
        tool_bar.SetBackgroundColour(wx.Colour(70, 100, 160))
        tool_bar.Realize()

        # Bindings
        self.Bind(wx.EVT_TOOL, self.on_save, id=ids.ID_SAVE_BUTTON)
        self.Bind(wx.EVT_TOOL, self.on_toggle_capturing, id=ids.ID_TOGGLE_CAPTURING_BUTTON)
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

    @staticmethod
    def change_toggle_button_icon(event, icon, text):
        event_object = event.GetEventObject()
        tool = event_object.GetToolByPos(event_object.GetToolPos(ids.ID_TOGGLE_CAPTURING_BUTTON))
        tool.SetNormalBitmap(wx.Bitmap(icon))
        tool.SetShortHelp(text)
        event_object.Realize()

    def on_toggle_capturing(self, event):
        if not self.should_stop:
            self.should_stop = True
            self.change_toggle_button_icon(event, icons.START, "Start Capturing")
            self.capture_thread.join()
            return

        self.should_stop = False
        self.change_toggle_button_icon(event, icons.PAUSE, "Pause Capturing")

        # Start a new capturing thread
        self.capture_thread = threading.Thread(target=self.start_capturing)
        self.capture_thread.start()

    def on_auto_scroll(self, event):
        item_count = self.list_control.GetItemCount()
        self.list_control.EnsureVisible(item_count - 1)

    def on_clear(self, event):
        self.list_control.DeleteAllItems()

    def on_close(self, event):
        self.should_stop = True
        self.Destroy()

    def add_row_and_scroll(self, row):
        self.list_control.add_row(row)
        self.list_control.smart_auto_scroll()

    def start_capturing(self):
        while not self.should_stop:
            row = self.content_provider.get_next_row()
            if row is None:
                continue
            wx.CallAfter(self.add_row_and_scroll, row)


def show():
    app = wx.App()
    frame = WinsnifferFrame("Winsniffer 1.0 Pre-Alpha")
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    show()
