import os


def icon(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', filename)


SAVE = icon("ic_save_white_24dp_2x.png")
ADD = icon("ic_playlist_add_white_24dp_2x.png")
START = icon("ic_play_arrow_white_24dp_2x.png")
PAUSE = icon("ic_pause_white_24dp_2x.png")
AUTO_SCROLL = icon("ic_vertical_align_bottom_white_24dp_2x.png")
CLEAR = icon("ic_delete_sweep_white_24dp_2x.png")
FILTER = icon("ic_filter_list_black_24dp_1x.png")
SET_PARSER = icon("ic_tune_white_24dp_2x.png")
RELOAD_PARSER = icon("ic_refresh_white_24dp_2x.png")
