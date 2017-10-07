import wx


class StatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, wx.ID_ANY)

        self.SetFieldsCount(4)
        self.SetStatusWidths([0, 200, 400, -1])

    def update_frame_count(self, text):
        self.SetStatusText(text, 1)

    def update_filter_status(self, text):
        self.SetStatusText(text, 2)

    def update_network_interface_status(self, text):
        self.SetStatusText(text, 3)
