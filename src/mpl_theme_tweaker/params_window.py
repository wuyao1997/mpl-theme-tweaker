import os
import platform
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Literal

from imgui_bundle import icons_fontawesome_6, imgui, imgui_toggle  # type: ignore
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager

from mpl_theme_tweaker.app_utils import get_downloads_folder
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


def is_valid_filename(filename: str) -> bool:
    if not filename or filename.strip() == "":
        return False

    if platform.system() == "Windows":
        illegal_chars = {"<", ">", ":", '"', "/", "\\", "|", "?", "*"}
        reserved_names = {
            "CON",
            "PRN",
            "AUX",
            "NUL",
            "COM1",
            "COM2",
            "COM3",
            "COM4",
            "COM5",
            "COM6",
            "COM7",
            "COM8",
            "COM9",
            "LPT1",
            "LPT2",
            "LPT3",
            "LPT4",
            "LPT5",
            "LPT6",
            "LPT7",
            "LPT8",
            "LPT9",
        }
        name_without_ext = Path(filename).stem.upper()
        if name_without_ext in reserved_names:
            return False
        if any(char in illegal_chars for char in filename):
            return False
        if filename.strip()[-1] in (" ", "."):
            return False
    else:
        if "/" in filename or "\0" in filename:
            return False

    try:
        temp_path = Path(os.path.join(os.getenv("TEMP", "/tmp"), filename))
        temp_path.resolve(strict=False)
        if temp_path.name != filename:
            return False
        return True
    except (OSError, ValueError):
        return False


def is_valid_file_path(file_path: str) -> bool:
    if not file_path:
        return False
    try:
        Path(file_path).resolve(strict=False)
        return True
    except (OSError, ValueError, TypeError):
        return False


def _title(title: str) -> None:
    imgui.push_font(_TITLE_FONT_, _TITLE_FONT_.legacy_size)  # type: ignore
    imgui.separator_text(title)
    imgui.pop_font()


@dataclass
class Preferences:
    style_name: str = ""
    duplicate_name_policy: Literal["overwrite", "numeric suffix"] = "numeric suffix"
    download_directory: str = ""
    custom_style_directory: str = ""
    target_directory: str = ""
    download_to_target: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "style_name": self.style_name,
            "duplicate_name_policy": self.duplicate_name_policy,
            "download_directory": self.download_directory,
            "custom_style_directory": self.custom_style_directory,
            "target_directory": self.target_directory,
            "download_to_target": self.download_to_target,
        }

    def from_dict(self, data: dict[str, Any]) -> None:
        self.style_name = data.get("style_name", "")

        policy = data.get("duplicate_name_policy", "numeric suffix")
        if policy not in ["overwrite", "numeric suffix"]:
            policy = "numeric suffix"
        self.duplicate_name_policy = policy  # type: ignore

        directory = data.get("download_directory", "")
        if directory:
            self.download_directory = directory
        else:
            self.download_directory = get_downloads_folder().as_posix()

        self.custom_style_directory = data.get("custom_style_directory", "")
        self.target_directory = data.get("target_directory", "")
        self.download_to_target = bool(data.get("download_to_target", False))

        return

    def get_write_path(self) -> Path:
        filename = self.style_name if self.style_name else "matplotlibrc"

        if self.download_to_target:
            return Path(self.target_directory) / filename
        else:
            return Path(self.download_directory) / filename

    def gui(self) -> None:
        global _TITLE_FONT_
        if _TITLE_FONT_ is None:
            _TITLE_FONT_ = get_app_key("title_font")

        _title("Style Name")
        _, style_name = imgui.input_text_with_hint(
            "Style Name", "Style name", self.style_name
        )
        if is_valid_filename(style_name):
            self.style_name = style_name

        _title("Duplicate name policy")
        if imgui.radio_button("Ovewrite", self.duplicate_name_policy == "overwrite"):
            self.duplicate_name_policy = "overwrite"
        imgui.same_line()
        if imgui.radio_button(
            "Numeric suffix", self.duplicate_name_policy == "numeric suffix"
        ):
            self.duplicate_name_policy = "numeric suffix"

        _title("Default Directory")
        _, self.download_directory = imgui.input_text_with_hint(
            "Download",
            "C:\\Users\\username\\Downloads",
            self.download_directory,
        )
        _, self.custom_style_directory = imgui.input_text_with_hint(
            "Custom Style",
            "C:\\Users\\username\\Documents\\matplotlib\\style",
            "",
        )
        _, self.target_directory = imgui.input_text_with_hint(
            "Target",
            "C:\\Users\\username\\Desktop\\workspace",
            self.target_directory,
        )
        toggle_config = imgui_toggle.ios_style(size_scale=0.2)
        _, self.download_to_target = imgui_toggle.toggle(
            "Download to Target",
            self.download_to_target,
            config=toggle_config,
        )
        return


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
        self.preferences = Preferences()

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
        if imgui.begin_tab_bar("RcParams"):
            if imgui.begin_tab_item("Preferences")[0]:
                self.preferences.gui()
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

    def gui_app_menu(self) -> None:
        imgui.menu_item(f"{icons_fontawesome_6.ICON_FA_FILE} Open", "", False)
        imgui.separator()
        # ======================== Save =====================
        save_clicked, _ = imgui.menu_item(
            f"{icons_fontawesome_6.ICON_FA_FLOPPY_DISK} Save", "", False
        )
        # ====================== Save As ====================
        saveas_clicked, _ = imgui.menu_item(
            f"{icons_fontawesome_6.ICON_FA_FILE_EXPORT} Save As", "", False
        )
        # ===================== Download ====================
        download_clicked, _ = imgui.menu_item(
            f"{icons_fontawesome_6.ICON_FA_FILE_ARROW_DOWN} Download", "", False
        )
        if download_clicked:
            filepath = self.preferences.get_write_path()
            directory = filepath.parent
            if not directory.exists():
                print(f"Downloads folder ``{directory}`` does not exist")
                return

            if (
                filepath.exists()
                and self.preferences.duplicate_name_policy == "numeric suffix"
            ):
                n = 1
                while True:
                    new_filepath = filepath.with_name(
                        f"{filepath.stem}({n}){filepath.suffix}"
                    )
                    if not new_filepath.exists():
                        filepath = new_filepath
                        break
                    n += 1
            style_str = self.get_style_str()
            filepath.write_text(style_str)
            print(f"Style saved to ``{filepath}``")

        # ================ Copy to Clipboard ================
        copy_clicked, _ = imgui.menu_item(
            f"{icons_fontawesome_6.ICON_FA_COPY} Copy to Clipboard", "", False
        )
        if copy_clicked:
            style_str = self.get_style_str()
            imgui.set_clipboard_text(style_str)

        # shortcut must be put in main loop or gui always show
        # if imgui.is_key_chord_pressed(imgui.Key.mod_ctrl | imgui.Key.s):
        #     print("Ctrl + S pressed")

        # clicked, _ = imgui.menu_item("A Custom app menu item", "", False)
        # if clicked:
        #     print("Clicked on A Custom app menu item")
        #     hello_imgui.log(
        #         hello_imgui.LogLevel.info, "Clicked on A Custom app menu item"
        #     )
        return

    def get_app_settings(self) -> dict[str, Any]:
        return self.preferences.to_dict()

    def load_app_settings(self, settings: dict) -> None:
        self.preferences.from_dict(settings)
