import wx
import wx.lib.mixins.listctrl as listmixin


class ListControl(wx.ListCtrl, listmixin.ListCtrlAutoWidthMixin):
    def __init__(self, parent, content_provider):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        listmixin.ListCtrlAutoWidthMixin.__init__(self)

        # Insert columns
        for column_index, (column, width) in enumerate(content_provider.get_columns()):
            self.InsertColumn(column_index, column, width=width)

        # Style
        self.SetBackgroundColour(wx.Colour(230, 230, 250))

        self.rows = []
        self.filter = None

    def add_row(self, row):
        self.rows.append(row)
        return self._add_row_as_item(row)

    def get_number_of_rows(self):
        return len(self.rows)

    def _add_row_as_item(self, row):
        if self.filter is not None and not self.filter(row):
            return False

        index = self.InsertItem(self.GetItemCount(), str(row[0]))
        for i, value in enumerate(row[1:]):
            self.SetItem(index, i + 1, str(value))

        if index % 2 == 0:
            self.SetItemBackgroundColour(index, "white")
        return True

    def delete_all_rows(self):
        self.rows = []

    def reload(self):
        wx.BeginBusyCursor()
        try:
            self.Freeze()
            self.DeleteAllItems()
            for row in self.rows:
                self._add_row_as_item(row)
            self.Thaw()
            self.Refresh()
        finally:
            wx.EndBusyCursor()

    def set_filter(self, filter):
        self.filter = filter

    def smart_auto_scroll(self):
        scroll_position = self.GetScrollPos(wx.VERTICAL)
        visible_items_count = self.GetCountPerPage()
        scroll_bottom_position = scroll_position + visible_items_count
        item_count = self.GetItemCount()
        if scroll_bottom_position >= item_count - 3:
            self.EnsureVisible(item_count - 1)
