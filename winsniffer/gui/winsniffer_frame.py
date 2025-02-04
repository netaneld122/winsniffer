import os
import time
import threading
import wx
import wx.py

import winsniffer
import winsniffer.gui.ids as ids
import winsniffer.gui.icons as icons

from winsniffer.gui.content_provider import ContentProvider
from winsniffer.gui.list_control import ListControl
from winsniffer.gui.status_bar import StatusBar
from winsniffer.gui.settings_dialog import SettingsDialog
from winsniffer.gui.parsing.parser_loader import ParserLoader
from winsniffer.gui.settings import Settings, get_default_parser_script_path


# Python shell global variables
frames = []


class WinsnifferFrame(wx.Frame):
    def __init__(self, title):
        super(WinsnifferFrame, self).__init__(None, wx.ID_ANY, title, size=(1150, 700))

        # Configure initial settings
        self.settings = Settings(get_default_parser_script_path(), winsniffer.get_all_devices()[0])
        if not self.open_settings_dialog(self.settings):
            self.Destroy()
            return

        # Initialize parser and content provider
        self.parser_loader = ParserLoader(self.settings)
        self.parser_loader.reload()
        self.content_provider = self.initialize_content_provider(self.settings, self.parser_loader)

        # Create top level panel
        panel = wx.Panel(self)

        # Add filter control
        filter_control = wx.SearchCtrl(panel, id=ids.ID_FILTER_CONTROL, size=(-1, 30), style=wx.TE_PROCESS_ENTER)
        filter_control.SetFont(wx.Font(wx.FontInfo(12).FaceName("Trebuchet MS")))
        filter_control.SetSearchBitmap(wx.Bitmap(icons.FILTER))
        filter_control.SetDescriptiveText("Filter")
        bright_blue = wx.Colour(240, 240, 240)
        filter_control.SetBackgroundColour(bright_blue)

        # Create a splitter window for the list and shell
        splitter = wx.SplitterWindow(panel)

        # Add list control
        self.list_control = ListControl(splitter, self.content_provider)
        self.list_control.SetBackgroundColour(wx.Colour(245, 245, 248))

        # Add python shell
        self.shell = wx.py.shell.Shell(splitter, introText='Winsniffer Python Shell')

        splitter.SplitHorizontally(self.list_control, self.shell)
        splitter.SetSashGravity(0.75)

        # Set a vertical sizer
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        vertical_sizer.Add(filter_control, 0, wx.EXPAND)
        vertical_sizer.Add(splitter, 1, wx.EXPAND | wx.ALL)
        panel.SetSizer(vertical_sizer)

        self.set_tool_bar()

        # Set status bar
        self.status_bar = StatusBar(self)
        self.SetStatusBar(self.status_bar)
        self.status_bar.update_network_interface_status(self.settings.network_interface)

        # Center the window
        self.Center()

        # Bindings
        self.list_control.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_filter, id=ids.ID_FILTER_CONTROL)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Start a new capturing thread
        self.should_stop = False
        self.content_provider_lock = threading.Lock()
        self.capture_thread = threading.Thread(target=self.start_capturing)
        self.capture_thread.start()

    @staticmethod
    def initialize_content_provider(settings, parser_loader):
        sniffer = winsniffer.Sniffer(settings.network_interface, buffering=True, timeout_ms=100)
        return ContentProvider(sniffer, parser_loader)

    def set_tool_bar(self):
        tool_bar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_NODIVIDER)

        # Define buttons
        tool_bar.AddTool(ids.ID_SETTINGS_BUTTON, "", wx.Bitmap(icons.SETTINGS), wx.NullBitmap, wx.ITEM_NORMAL,
                         "Settings")

        tool_bar.AddTool(ids.ID_RELOAD_PARSER_BUTTON, "", wx.Bitmap(icons.RELOAD_PARSER), wx.NullBitmap,
                         wx.ITEM_NORMAL, "Reload Parser")

        tool_bar.AddSeparator()

        tool_bar.AddTool(ids.ID_SAVE_BUTTON, "", wx.Bitmap(icons.SAVE), wx.NullBitmap, wx.ITEM_NORMAL,
                         "Save")
        tool_bar.AddTool(ids.ID_TOGGLE_CAPTURING_BUTTON, "", wx.Bitmap(icons.PAUSE), wx.NullBitmap, wx.ITEM_NORMAL,
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
        self.Bind(wx.EVT_TOOL, self.on_settings_set, id=ids.ID_SETTINGS_BUTTON)
        self.Bind(wx.EVT_TOOL, self.on_reload_parsers, id=ids.ID_RELOAD_PARSER_BUTTON)
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
            self.status_bar.update_filter_status(u"Filter '{}'".format(text))

    def on_save(self, event):
        def doit():
            item_count = self.list_control.GetItemCount()
            column_count = self.list_control.GetColumnCount()
            output = ''
            for i in range(0, item_count):
                row = [self.list_control.GetItemText(i, j) for j in range(0, column_count)]
                output += ','.join(row) + '\n'
            file_name = '{}.{}.csv'.format(time.strftime('%Y.%m.%d.%H.%M.%S'), int(round((time.time() % 1) * 1000)))
            with open(file_name, 'w') as f:
                f.write(output)
            print('Saved ' + os.path.abspath(file_name))
        wx.CallAfter(doit)

    def open_settings_dialog(self, settings):
        settings_dialog = SettingsDialog(self, settings)
        if settings_dialog.ShowModal() == wx.ID_OK:
            self.settings = settings_dialog.settings
            return True
        return False

    def on_settings_set(self, event):
        network_interface_before_dialog = self.settings.network_interface
        if self.open_settings_dialog(self.settings):
            self.parser_loader.reload()
            self.status_bar.update_network_interface_status(self.settings.network_interface)

            # Invalidate the capture if a different network interface was chosen
            if network_interface_before_dialog != self.settings.network_interface:
                with self.content_provider_lock:
                    self.content_provider = self.initialize_content_provider(self.settings, self.parser_loader)
                self.list_control.delete_all_results()
                self.list_control.DeleteAllItems()

    def on_reload_parsers(self, event):
        self.parser_loader.reload()

    def on_item_selected(self, event):
        list_control = event.GetEventObject()
        item_index = list_control.GetFirstSelected()
        result_id = list_control.GetItemText(item_index, 0)
        global frames
        self.shell.run('frames[%d]' % int(result_id))

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
        self.list_control.delete_all_results()
        self.list_control.DeleteAllItems()

    def on_close(self, event):
        self.should_stop = True
        if self.capture_thread is not None:
            self.capture_thread.join(0.5)
        self.Destroy()

    def update_status_bar_frame_count(self):
        total_rows = self.list_control.get_number_of_results()
        total_displayed_rows = self.list_control.GetItemCount()
        self.status_bar.update_frame_count("Displaying {} / {} frames".format(total_displayed_rows, total_rows))

    def add_results_and_scroll(self, results):
        result_success_codes = [self.list_control.add_result(result) for result in results]
        if any(result_success_codes):
            self.list_control.smart_auto_scroll(len(result_success_codes))
        self.update_status_bar_frame_count()

        # Update the interpreter global frames
        global frames
        frames.extend((result[1] for result in results))

    def start_capturing(self):
        results = []
        start = time.time()
        while not self.should_stop:
            result = None
            with self.content_provider_lock:
                result = self.content_provider.get_next_result()
            if result is not None:
                results.append(result)

            # Is it flush time?
            if len(results) > 0 and time.time() - start > 0.15:
                wx.CallAfter(self.add_results_and_scroll, results[:])
                results = []
                start = time.time()


def show():
    app = wx.App()
    frame = WinsnifferFrame("Winsniffer 1.0 Pre-Alpha")
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    show()
