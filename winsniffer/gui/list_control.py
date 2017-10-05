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

        self._results = []
        self.filter = None

    @property
    def results(self):
        return self._results

    def add_result(self, result):
        self._results.append(result)
        return self._add_result_as_item(result)

    def get_number_of_results(self):
        return len(self._results)

    def _add_result_as_item(self, result):
        row, _ = result
        if self.filter is not None and not self.filter(row):
            return False

        index = self.InsertItem(self.GetItemCount(), str(row[0]))
        for i, value in enumerate(row[1:]):
            self.SetItem(index, i + 1, str(value))

        if index % 2 == 0:
            self.SetItemBackgroundColour(index, "white")
        return True

    def delete_all_results(self):
        self._results = []

    def reload(self):
        wx.BeginBusyCursor()
        try:
            self.Freeze()
            self.DeleteAllItems()
            for result in self._results:
                self._add_result_as_item(result)
            self.Thaw()
            self.Refresh()
        finally:
            wx.EndBusyCursor()

    def set_filter(self, filter):
        self.filter = filter

    def smart_auto_scroll(self, items_added):
        scroll_position = self.GetScrollPos(wx.VERTICAL)
        visible_items_count = self.GetCountPerPage()
        scroll_bottom_position = scroll_position + visible_items_count
        item_count = self.GetItemCount()
        if scroll_bottom_position >= item_count - 2 - items_added:
            self.EnsureVisible(item_count - 1)
