import wx
import wx.lib.mixins.listctrl as listmixin


class ListControl(wx.ListCtrl, listmixin.ListCtrlAutoWidthMixin):
    def __init__(self, parent, content_provider):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT)
        listmixin.ListCtrlAutoWidthMixin.__init__(self)

        # Insert columns
        for column_index, (column, width) in enumerate(content_provider.get_columns()):
            self.InsertColumn(column_index, column, width=width)

        # Style
        self.SetBackgroundColour(wx.Colour(230, 230, 250))

    def add_row(self, row):
        index = self.InsertItem(self.GetItemCount(), str(row[0]))
        for i, value in enumerate(row[1:]):
            self.SetItem(index, i + 1, str(value))

    def smart_auto_scroll(self):
        scroll_position = self.GetScrollPos(wx.VERTICAL)
        visible_items_count = self.GetCountPerPage()
        scroll_bottom_position = scroll_position + visible_items_count
        item_count = self.GetItemCount()
        if scroll_bottom_position >= item_count - 2:
            self.EnsureVisible(item_count - 1)
