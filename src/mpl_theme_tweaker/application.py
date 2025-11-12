import platform
from pathlib import Path
from typing import Any, Optional, TypedDict

import dearpygui.dearpygui as dpg

from mpl_theme_tweaker.logger import log
from mpl_theme_tweaker.utils import setup_docking, setup_font


class Application:
    def __init__(self):
        log.info("Application Start ...")
        self.title = "MPl Theme Tweaker"

        self.setup_dpg_context()
        self.setup_UI()

    def setup_dpg_context(self) -> None:
        if platform.system() == "Windows":
            import ctypes

            ctypes.windll.shcore.SetProcessDpiAwareness(1)

        dpg.create_context()
        setup_font()
        # setup_docking()
        dpg.create_viewport(
            title=self.title,
            width=600,
            height=1200,
            disable_close=True,
            resizable=True,
        )
        dpg.set_exit_callback(self.exit)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        return

    def setup_UI(self) -> None:
        """Setup the DearPyGUI UI."""
        with dpg.window(label="Main Window", width=1800, height=1200) as main_window:
            self.main_window = main_window
            dpg.set_primary_window(main_window, True)

        with dpg.tab_bar(parent=main_window) as self.tab_bar:
            dpg.add_tab(label="General")
            dpg.add_tab(label="Other")
            dpg.add_tab(label="Theme")

        self.setup_menu()
        return

    def setup_menu(self) -> None:
        """Setup the DearPyGUI menu bar."""
        with dpg.menu_bar(parent=self.main_window) as menu_bar:
            with dpg.menu(label="File", parent=menu_bar):
                dpg.add_menu_item(label="Exit", callback=self.exit)

            with dpg.menu(label="Help", parent=menu_bar):
                dpg.add_menu_item(label="About", callback=lambda: log.info("About"))
        return

    def run(self) -> None:
        """Run the application."""
        log.info("Start DearPyGUI loop.")
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
        return

    def exit(self) -> None:
        """Exit the application."""
        log.info("Destroy DearPyGUI context.")
        dpg.destroy_context()
        log.info("Application End Normally.")
        return
