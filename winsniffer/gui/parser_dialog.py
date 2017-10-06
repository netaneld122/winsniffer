import os
import wx
import wx.lib.sized_controls as sized_controls
import wx.lib.filebrowsebutton as filebrowsebutton


class ParserDialog(sized_controls.SizedDialog):
    def __init__(self, parent, parser_loader):
        super(ParserDialog, self).__init__(
            parent,
            wx.ID_ANY,
            "Set Parser Script",
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.parser_loader = parser_loader

        pane = self.GetContentsPane()
        pane.SetSizerType("form")

        # Browse file
        self._parser_script_path = self.parser_loader.parser_script_path
        start_directory = os.path.dirname(self._parser_script_path)
        filebrowsebutton.FileBrowseButton(
            pane,
            wx.ID_ANY,
            size=(550, -1),
            initialValue=self._parser_script_path,
            startDirectory=start_directory,
            labelText="Parser script: ",
            fileMask="*.py",
            changeCallback=self.on_change)

        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))

        self.Fit()
        self.SetMinSize(self.GetSize())

    @property
    def parser_script_path(self):
        return self._parser_script_path

    def on_change(self, event):
        script_path = event.GetString()
        if os.path.isfile(script_path):
            self._parser_script_path = script_path


def show():
    app = wx.App()
    frame = ParserDialog(None)
    frame.CenterOnScreen()
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    show()
