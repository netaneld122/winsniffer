import wx
import wx.dataview

from winsniffer.gui.data_view_virtual_list_model import DataViewVirtualListModel


class DataViewControl(wx.dataview.DataViewCtrl):
    def __init__(self, parent, content_provider):
        super(DataViewControl, self).__init__(
            parent,
            style=wx.BORDER_THEME | wx.dataview.DV_ROW_LINES | wx.dataview.DV_VERT_RULES | wx.dataview.DV_SINGLE)

        self.content_provider = content_provider

        self.data_view_model = DataViewVirtualListModel()
        self.AssociateModel(self.data_view_model)

        for i, (column, width) in enumerate(content_provider.get_columns()):
            self.AppendTextColumn(column,  i, width=width)

    def add_row(self, row):
        self.data_view_model.get_data().append(row)
        self.data_view_model.RowAppended()

    def smart_auto_scroll(self):
        scroll_position = self.GetScrollPos(wx.VERTICAL)
        scroll_bottom_position = scroll_position # + visible_items_count
        item_count = self.data_view_model.GetCount()
        if scroll_bottom_position >= item_count - 1:
            self.SetScrollPos(wx.VERTICAL, item_count - 1)

    def get_total_items_count(self):
        return len(self.data_view_model.get_data())

    def get_displayed_items_count(self):
        return self.data_view_model.GetCount()

    def clear_all(self):
        self.data_view_model.replace_data([])
        self.data_view_model.Reset(0)