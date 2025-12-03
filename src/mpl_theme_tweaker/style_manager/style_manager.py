"""StyleManager

Functionality:
    - Find all style files in the directory recursively.
      Use a dict to save filename and path.


"""

from pathlib import Path

import matplotlib.pyplot as plt
from imgui_bundle import imgui

from mpl_theme_tweaker._global import get_app_key


def search_mplstyle_files(search_dir: str | Path) -> dict[str, list[str]]:
    """Search all .mplstyle files in the directory recursively.

    Args:
        search_dir (str | Path): The directory to search.

    Returns:
        dict[str, list[str]]: A dict with directory name as key and a list of style file paths as value.
    """
    root_path = Path(search_dir).absolute()
    result: dict[str, list[str]] = {}
    for file_path in root_path.rglob("*.mplstyle"):
        if not file_path.is_file():
            continue

        # Get the relative path of the file directory
        file_dir = file_path.parent
        rel_dir = file_dir.relative_to(root_path)

        dict_key = "root" if rel_dir == Path(".") else str(rel_dir)
        if dict_key not in result:
            result[dict_key] = []
        result[dict_key].append(str(file_path.absolute()))

    return result


class StyleManager:
    directory: Path
    styles_map: dict[str, list[Path]] = {}

    def __init__(self):
        pass

    def set_path(self, path: Path | str) -> None:
        self.directory = Path(path).absolute()
        self.reload()
        return

    def reload(self) -> None:
        result = search_mplstyle_files(self.directory)
        self.styles_map = {k: [Path(v) for v in vs] for k, vs in result.items()}
        return

    def get_path(self) -> Path:
        return self.directory

    def menu_gui(self) -> None:
        for dir_name, style_files in self.styles_map.items():
            if imgui.begin_menu(dir_name):
                for style_file in style_files:
                    menu_label = style_file.stem
                    clicked, _ = imgui.menu_item(menu_label, "", False)
                    if clicked:
                        plt.style.use(style_file)
                        # will call FigureWindow.replot_func automatically
                        _func = get_app_key("ParamsWindow.reset_by_rcParams")
                        if _func is not None:
                            _func()
                imgui.end_menu()
        return
