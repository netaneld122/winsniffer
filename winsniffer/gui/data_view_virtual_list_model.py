import wx
import wx.dataview


class DataViewVirtualListModel(wx.dataview.DataViewVirtualListModel):
    def __init__(self):
        super(DataViewVirtualListModel, self).__init__()
        self.data = []
        self.filtered_indexes = []

    def GetValueByRow(self, row, col):
        return self.data[row][col]

    def GetColumnCount(self):
        return len(self.data[0])

    def GetCount(self):
        return len(self.data)

    def replace_data(self, data):
        self.data = data

    def get_data(self):
        return self.data
