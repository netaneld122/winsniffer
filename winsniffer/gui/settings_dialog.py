import os
import wx
import wx.lib.sized_controls as sized_controls
import wx.lib.filebrowsebutton as filebrowsebutton

import winsniffer


class SettingsDialog(sized_controls.SizedDialog):
    def __init__(self, parent, settings):
        super(SettingsDialog, self).__init__(
            parent,
            wx.ID_ANY,
            "Settings",
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.settings = settings

        pane = self.GetContentsPane()
        pane.SetSizerType("form")

        # Row 1 - Browse parser file
        wx.StaticText(pane, -1, "Parser script: ")
        start_directory = os.path.dirname(self.settings.parser_script_path)
        file_browser = filebrowsebutton.FileBrowseButton(
            pane,
            wx.ID_ANY,
            size=(450, -1),
            initialValue=self.settings.parser_script_path,
            startDirectory=start_directory,
            labelText="*",
            fileMask="*.py",
            labelWidth=0,
            changeCallback=self.on_parser_change)
        file_browser.SetSizerProps(expand=True)

        # Row 2 - Choose a network interface
        wx.StaticText(pane, -1, "Network Interaces: ")
        network_devices = winsniffer.get_all_devices()
        interfaces_box = wx.ListBox(pane, id=wx.ID_ANY, size=(100, -1), choices=network_devices, style=wx.LB_SINGLE)
        interfaces_box.SetSizerProps(expand=True, proportion=1)
        interfaces_box.Select(interfaces_box.FindString(self.settings.network_interface))
        self.Bind(wx.EVT_LISTBOX, self.on_network_interface_select, interfaces_box)

        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))

        self.Fit()
        self.SetMinSize(self.GetSize())
        self.Center()

    def on_parser_change(self, event):
        script_path = event.GetString()
        if os.path.isfile(script_path):
            self.settings.parser_script_path = script_path

    def on_network_interface_select(self, event):
        list_box = event.GetEventObject()
        network_interface = list_box.GetStringSelection()
        self.settings.network_interface = network_interface


def show():
    from winsniffer.gui.settings import Settings

    app = wx.App()
    dialog = SettingsDialog(None, Settings('', None))
    dialog.CenterOnScreen()
    dialog.ShowModal()


if __name__ == '__main__':
    show()
