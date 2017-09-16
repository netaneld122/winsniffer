import wx
import wx.lib.mixins.listctrl as listmixin


class ListControl(wx.ListCtrl, listmixin.ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT)
        listmixin.ListCtrlAutoWidthMixin.__init__(self)
