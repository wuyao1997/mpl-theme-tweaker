from pathlib import Path

import dearpygui.dearpygui as dpg

from .path import resourcePath


def setup_font():
    font_path = resourcePath() / "font/NotoSans-Regular.ttf"

    with dpg.font_registry():
        with dpg.font(font_path.as_posix(), 32) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Korean)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Thai)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Vietnamese)
        dpg.bind_font(default_font)
    return


def setup_docking() -> None:
    """Setup the docking layout."""
    docking_file = resourcePath() / "data/docking.ini"
    dpg.configure_app(
        docking=True,
        docking_space=True,
        # load_init_file=docking_file,
    )
    dpg.configure_app(init_file=docking_file)
    return
