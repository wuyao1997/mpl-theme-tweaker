from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from imgui_bundle import icons_fontawesome_6, imgui, imgui_toggle
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager

from mpl_theme_tweaker.mpl_entry.section import (
    Section,
    AxesSection,
    BoxplotSection,
    FigureSection,
    ImageSection,
    TextSection,
    TicksSection,
    LegendSection,
    LinesSection,
)
from mpl_theme_tweaker._global import get_app_key

_TABLE_FLAGS = imgui.TableFlags_.borders + imgui.TableFlags_.resizable
_FONT_NAMES = ["None"] + sorted(set(fontManager.get_font_names()))
_TITLE_FONT_ = None


def _title(title: str) -> None:
    imgui.push_font(_TITLE_FONT_, _TITLE_FONT_.legacy_size)  # type: ignore
    imgui.separator_text(title)
    imgui.pop_font()


@dataclass
class _Font:
    index: int = 0
    name: str = "None"


@dataclass
class _FontFamilyManager:
    family_names: list[str] = field(
        default_factory=lambda: [
            "serif",
            "sans-serif",
            "cursive",
            "fantasy",
            "monospace",
        ]
    )
    N: int = 5
    fonts: dict[str, list[_Font]] = field(init=False, default_factory=dict)

    def __post_init__(self):
        for family in self.family_names:
            self.fonts[family] = [_Font() for _ in range(self.N)]

    def apply(self) -> None:
        for key, fonts in self.fonts.items():
            font_names = [font.name for font in fonts if font.name != "None"]
            plt.rcParams[f"font.{key}"] = font_names

        replot_func = get_app_key("FigureWidow.replot_func")
        if replot_func is not None:
            replot_func()
        return

    def gui(self) -> None:
        if imgui.begin_table("Font", 5, _TABLE_FLAGS):
            imgui.table_headers_row()

            title_font = get_app_key("title_font")
            imgui.push_font(title_font, title_font.legacy_size)
            for j, family_name in enumerate(self.family_names):
                imgui.table_set_column_index(j)
                imgui.text(family_name)
            imgui.pop_font()

            for i in range(self.N):
                imgui.table_next_row()
                for j, family_name in enumerate(self.family_names):
                    imgui.table_set_column_index(j)
                    current_font = self.fonts[family_name][i]

                    imgui.push_item_width(-1)
                    changed, new_index = imgui.combo(
                        f"##font_{i}_{j}", current_font.index, _FONT_NAMES
                    )
                    if changed:
                        current_font.index = new_index
                        current_font.name = _FONT_NAMES[new_index]
                    imgui.pop_item_width()

            imgui.end_table()

        if imgui.button(f"Apply {icons_fontawesome_6.ICON_FA_ROCKET}", [-1, 0]):
            self.apply()

        return

    def reset_by_rcParams(self) -> None:
        for family_name in self.family_names:
            font_names = plt.rcParams[f"font.{family_name}"]
            row = 0
            for i, font_name in enumerate(font_names):
                if row >= self.N:
                    break
                if font_name in _FONT_NAMES:
                    index = _FONT_NAMES.index(font_name)
                    self.fonts[family_name][row].index = index
                    self.fonts[family_name][row].name = font_name
                    row += 1
        return


class ParamsWindow:
    def __init__(self, callback: Callable):
        self.callback: Callable = callback
        self.font_family_manager = _FontFamilyManager()

        self.sections: list[Section] = [
            FigureSection(),
            AxesSection(),
            TicksSection(),
            LinesSection(),
            LegendSection(),
            TextSection(),
            BoxplotSection(),
            ImageSection(),
        ]

        self.reset_by_default(call_callback=False)

    def gui(self) -> None:
        global _TITLE_FONT_
        if _TITLE_FONT_ is None:
            _TITLE_FONT_ = get_app_key("title_font")

        if imgui.begin_tab_bar("RcParams"):
            if imgui.begin_tab_item("Preferences")[0]:
                _title("Style Name")
                imgui.input_text_with_hint("Style Name", "Style name", "")

                _title("Duplicate name policy")
                imgui.radio_button("Ovewrite", False)
                imgui.same_line()
                imgui.radio_button("Numeric suffix", True)

                _title("Default Directory")
                imgui.input_text_with_hint(
                    "Download", "C:\\Users\\username\\Downloads", ""
                )
                imgui.input_text_with_hint(
                    "Custom Style",
                    "C:\\Users\\username\\Documents\\matplotlib\\style",
                    "",
                )
                imgui.input_text_with_hint(
                    "Target",
                    "C:\\Users\\username\\Desktop\\workspace",
                    "",
                )
                toggle_config = imgui_toggle.ios_style(size_scale=0.2)
                imgui_toggle.toggle("Download to Target", True, config=toggle_config)

                imgui.end_tab_item()

            for section in self.sections:
                if imgui.begin_tab_item(section.get_name())[0]:
                    section.gui()
                    imgui.end_tab_item()

            if imgui.begin_tab_item("Font")[0]:
                self.font_family_manager.gui()
                imgui.end_tab_item()
            imgui.end_tab_bar()

        self.update_check()
        return

    def update_check(self):
        need_update = [section.need_update() for section in self.sections]
        if any(need_update):
            self.callback()
            for section in self.sections:
                section.update()
        return

    def reset_by_rcParams(self, call_callback: bool = True) -> None:
        for section in self.sections:
            section.reset_by_rcParams()

        self.font_family_manager.reset_by_rcParams()

        if call_callback:
            self.callback()
        return

    def reset_by_default(self, call_callback: bool = True) -> None:
        plt.style.use("default")
        self.reset_by_rcParams(call_callback)
        return

    def reset_by_style(self, style_name: str) -> None:
        plt.style.use("default")
        plt.style.use(style_name)
        self.reset_by_rcParams()
        return

    def save2matlotlibrc(self, filepath: str) -> None:
        print("# Not Implemented Yet")
        return

    def get_style_str(self) -> str:
        text = "## written by mpl-theme-tweaker, version 0.1.0\n"
        for section in self.sections:
            text += section.to_str() + "\n\n"
        return text
