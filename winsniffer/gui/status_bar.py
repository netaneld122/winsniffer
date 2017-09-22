import wx


class StatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, wx.ID_ANY)

        self.SetFieldsCount(2)

    def update_frame_count(self, text):
        self.SetStatusText(text, 0)

    def update_filter_status(self, text):
        self.SetStatusText(text, 1)