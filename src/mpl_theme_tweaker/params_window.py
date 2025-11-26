from typing import Callable

from imgui_bundle import imgui
import matplotlib.pyplot as plt

from mpl_theme_tweaker.mpl_entry.section import (
    AxesSection,
    BoxplotSection,
    FigureSection,
    ImageSection,
    TextSection,
    TicksSection,
    LegendSection,
    LinesSection,
)


class ParamsWindow:
    def __init__(self, callback: Callable):
        self.callback: Callable = callback

        self.sections = [
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
            for section in self.sections:
                if imgui.begin_tab_item(section.get_name())[0]:
                    section.gui()
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
