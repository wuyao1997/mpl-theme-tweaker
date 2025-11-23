from abc import ABC, abstractmethod

from mpl_theme_tweaker.mpl_entry.mpl_entry import (
    ColorEntry,
    Entry,
    FloatEntry,
    IntEntry,
)


class Section(ABC):
    entries: list[Entry]
    __SECTION_NAME__: str = ""

    def __init__(self):
        self.entries = self._setup_entries()

    @abstractmethod
    def _setup_entries(self) -> list[Entry]: ...

    def gui(self) -> None:
        for entry in self.entries:
            entry.gui()
        return

    def need_update(self) -> bool:
        need_update = [entry.need_update() for entry in self.entries]
        return any(need_update)

    def update(self) -> None:
        for entry in self.entries:
            entry.update()
        return

    @classmethod
    def get_name(cls) -> str:
        return cls.__SECTION_NAME__

    def reset_by_rcParams(self) -> None:
        for entry in self.entries:
            entry.reset_by_rcParams()
        return


class FigureSection(Section):
    __SECTION_NAME__ = "Figure"

    def __init__(self):
        super().__init__()

    def _setup_entries(self) -> list[Entry]:
        dpi = FloatEntry(
            "DPI",
            "figure.dpi",
            {
                "value": 100.0,
                "vmin": 50,
                "vmax": 1200,
                "step": 2,
                "stepfast": 50,
                "format": "%.1f",
            },
        )

        facecolor = ColorEntry("face color", "figure.facecolor")
        edgecolor = ColorEntry("edge color", "figure.edgecolor", sameline=True)

        _info = {
            "value": 0.125,
            "vmin": 0.0,
            "vmax": 1.0,
            "step": 0.005,
            "stepfast": 0.05,
            "format": "%.4f",
        }
        subplot_left = FloatEntry("subplot left", "figure.subplot.left", _info)

        _info["value"] = 0.9
        subplot_right = FloatEntry("subplot right", "figure.subplot.right", _info)

        _info["value"] = 0.11
        subplot_bottom = FloatEntry("subplot bottom", "figure.subplot.bottom", _info)

        _info["value"] = 0.88
        subplot_top = FloatEntry("subplot top", "figure.subplot.top", _info)
        return [
            dpi,
            facecolor,
            edgecolor,
            subplot_left,
            subplot_right,
            subplot_bottom,
            subplot_top,
        ]


class AxesSection(Section):
    __SECTION_NAME__ = "Axes"

    def __init__(self):
        super().__init__()

    def _setup_entries(self) -> list[Entry]:
        facecolor = ColorEntry("face color", "axes.facecolor")
        edgecolor = ColorEntry("edge color", "axes.edgecolor", sameline=True)
        return [facecolor, edgecolor]
