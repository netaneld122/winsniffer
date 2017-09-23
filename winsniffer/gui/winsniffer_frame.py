import wx
import wx.py
import time
import threading

import winsniffer.gui.ids as ids
import winsniffer.gui.icons as icons

from winsniffer.gui.content_provider import ContentProvider
from winsniffer.gui.list_control import ListControl
from winsniffer.gui.status_bar import StatusBar


class WinsnifferFrame(wx.Frame):
    def __init__(self, title):
        super(WinsnifferFrame, self).__init__(None, wx.ID_ANY, title, size=(1150, 700))

        # Create top level panel
        panel = wx.Panel(self)

        # Add filter control
        filter_control = wx.SearchCtrl(panel, id=ids.ID_FILTER_CONTROL, size=(-1, 30), style=wx.TE_PROCESS_ENTER)
        filter_control.SetFont(wx.Font(wx.FontInfo(12).FaceName("Trebuchet MS")))
        filter_control.SetSearchBitmap(wx.Bitmap(icons.FILTER))
        filter_control.SetDescriptiveText("Filter")
        bright_blue = wx.Colour(240, 240, 240)
        filter_control.SetBackgroundColour(bright_blue)

        # Add list control
        self.content_provider = ContentProvider()
        self.list_control = ListControl(panel, self.content_provider)
        self.list_control.SetBackgroundColour(wx.Colour(245, 245, 248))

        # Set a vertical sizer
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        vertical_sizer.Add(filter_control, 0, wx.EXPAND)
        vertical_sizer.Add(self.list_control, 1, wx.EXPAND | wx.ALL)
        panel.SetSizer(vertical_sizer)

        self.set_tool_bar()

        # Set status bar
        self.status_bar = StatusBar(self)
        self.SetStatusBar(self.status_bar)

        # Center the window
        self.Center()

        self.should_stop = True
        self.capture_thread = None

        # Bindings
        self.Bind(wx.EVT_TEXT_ENTER, self.on_filter, id=ids.ID_FILTER_CONTROL)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def set_tool_bar(self):
        tool_bar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_NODIVIDER)

        # Define buttons
        tool_bar.AddTool(ids.ID_ADD_BUTTON, "", wx.Bitmap(icons.ADD), wx.NullBitmap, wx.ITEM_NORMAL,
                         "Add Template")
        tool_bar.AddTool(ids.ID_SAVE_BUTTON, "", wx.Bitmap(icons.SAVE), wx.NullBitmap, wx.ITEM_NORMAL,
                         "Save")
        tool_bar.AddTool(ids.ID_TOGGLE_CAPTURING_BUTTON, "", wx.Bitmap(icons.START), wx.NullBitmap, wx.ITEM_NORMAL,
                         "Start Capturing")
        tool_bar.AddTool(ids.ID_AUTO_SCROLL_BUTTON, "", wx.Bitmap(icons.AUTO_SCROLL), wx.NullBitmap, wx.ITEM_NORMAL,
                         "Auto scroll")

        tool_bar.AddStretchableSpace()
        tool_bar.AddTool(ids.ID_CLEAR_BUTTON, "", wx.Bitmap(icons.CLEAR), wx.NullBitmap, wx.ITEM_NORMAL, "Clear")

        # Draw the tool bar
        dark_blue = wx.Colour(70, 100, 160)
        tool_bar.SetBackgroundColour(dark_blue)
        tool_bar.Realize()

        # Bindings
        self.Bind(wx.EVT_TOOL, self.on_save, id=ids.ID_SAVE_BUTTON)
        self.Bind(wx.EVT_TOOL, self.on_add, id=ids.ID_ADD_BUTTON)
        self.Bind(wx.EVT_TOOL, self.on_toggle_capturing, id=ids.ID_TOGGLE_CAPTURING_BUTTON)
        self.Bind(wx.EVT_TOOL, self.on_auto_scroll, id=ids.ID_AUTO_SCROLL_BUTTON)
        self.Bind(wx.EVT_TOOL, self.on_clear, id=ids.ID_CLEAR_BUTTON)

    def on_filter(self, event):
        filter_control = event.GetEventObject()
        text = filter_control.GetValue()
        self.list_control.set_filter(lambda row: text.lower() in ' '.join(map(str, row)).lower())
        self.list_control.reload()

        self.update_status_bar_frame_count()

        if text == '':
            self.status_bar.update_filter_status("")
        else:
            self.status_bar.update_filter_status("Filter '{}'".format(text))

    def on_save(self, event):
        def doit():
            item_count = self.list_control.GetItemCount()
            column_count = self.list_control.GetColumnCount()
            output = ''
            for i in range(0, item_count):
                row = [self.list_control.GetItemText(i, j) for j in range(0, column_count)]
                output += ','.join(row) + '\n'
            print(output)
        wx.CallAfter(doit)

    def on_add(self, event):
        # Enforce one window
        add_structure_frame = self.FindWindowById(ids.ID_ADD_STRUCTURE_FRAME)
        if add_structure_frame is not None:
            add_structure_frame.SetFocus()
            return

        add_structure_frame = wx.Frame(self, ids.ID_ADD_STRUCTURE_FRAME, "Add Structures")
        wx.Panel(add_structure_frame)
        add_structure_frame.Center()
        add_structure_frame.Show()

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
        self.list_control.delete_all_rows()
        self.list_control.DeleteAllItems()

    def on_close(self, event):
        self.should_stop = True
        if self.capture_thread is not None:
            self.capture_thread.join(0.5)
        self.Destroy()

    def update_status_bar_frame_count(self):
        total_rows = self.list_control.get_number_of_rows()
        total_displayed_rows = self.list_control.GetItemCount()
        self.status_bar.update_frame_count("Displaying {} / {} frames".format(total_displayed_rows, total_rows))

    def add_rows_and_scroll(self, rows):
        results = [self.list_control.add_row(row) for row in rows]
        if any(results):
            self.list_control.smart_auto_scroll(len(results))
            self.update_status_bar_frame_count()

    def start_capturing(self):
        rows = []
        start = time.time()
        while not self.should_stop:
            row = self.content_provider.get_next_row()
            if row is not None:
                rows.append(row)

            # Is it flush time?
            if len(rows) > 0 and time.time() - start > 0.2:
                wx.CallAfter(self.add_rows_and_scroll, rows[:])
                rows = []
                start = time.time()


def show():
    app = wx.App()
    frame = WinsnifferFrame("Winsniffer 1.0 Pre-Alpha")
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    show()
