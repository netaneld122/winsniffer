import wx


def create_id_generator():
    wx_id = wx.ID_HIGHEST + 1
    while True:
        yield wx_id
        wx_id += 1


id_generator = create_id_generator()

# Toolbar buttons
ID_SAVE_BUTTON = id_generator.next()
ID_SETTINGS_BUTTON = id_generator.next()
ID_RELOAD_PARSER_BUTTON = id_generator.next()
ID_TOGGLE_CAPTURING_BUTTON = id_generator.next()
ID_AUTO_SCROLL_BUTTON = id_generator.next()
ID_CLEAR_BUTTON = id_generator.next()

ID_FILTER_CONTROL = id_generator.next()
ID_PARSER_SCRIPT_CONTROL = id_generator.next()
