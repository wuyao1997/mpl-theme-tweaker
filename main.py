from imgui_bundle import hello_imgui, imgui, immapp

# from imgui_bundle.demos_python import demo_utils
import matplotlib.pyplot as plt

from mpl_theme_tweaker.app_utils import setup_theme, set_window_icon, load_fonts
from mpl_theme_tweaker.figure_window import FigureWindow
from mpl_theme_tweaker.params_window import ParamsWindow
from mpl_theme_tweaker._global import assetsPath


class Application:
    def __init__(self):
        self.figure_window = FigureWindow()
        self.params_window = ParamsWindow(self.figure_window.replot)
        self.styles = [
            style for style in plt.style.available if not style.startswith("_")
        ]

        self.params = hello_imgui.RunnerParams()
        self._setup_app_window_params()
        self._setup_callbacks()
        self._setup_imgui_window_params()
        self._setup_save_settings()
        self._setup_addon()
        self._setup_layout()

    def _setup_layout(self) -> None:
        def _create_default_docking_splits() -> list[hello_imgui.DockingSplit]:
            # Define the default docking splits
            #    ___________________________________________
            #    |                                         |
            #    |            FigureSpace                  |
            #    |                                         |
            #    |-----------------------------------------|
            #    |                                         |
            #    |           MainDockSpace                 |
            #    |_________________________________________|

            split_main_misc = hello_imgui.DockingSplit()
            split_main_misc.initial_dock = "MainDockSpace"
            split_main_misc.new_dock = "FigureSpace"
            split_main_misc.direction = imgui.Dir.up
            split_main_misc.ratio = 0.25

            splits = [split_main_misc]
            return splits

        def _create_dockable_windows() -> list[hello_imgui.DockableWindow]:
            # figure window
            figure_window = hello_imgui.DockableWindow()
            figure_window.label = "Figure"
            figure_window.dock_space_name = "FigureSpace"
            figure_window.imgui_window_flags = imgui.WindowFlags_.horizontal_scrollbar
            figure_window.gui_function = self.figure_window.gui

            # rc window
            rc_window = hello_imgui.DockableWindow()
            rc_window.label = "Parameter"
            rc_window.dock_space_name = "MainDockSpace"
            rc_window.gui_function = self.params_window.gui

            return [figure_window, rc_window]

        iwp = self.params.imgui_window_params
        iwp.default_imgui_window_type = (
            hello_imgui.DefaultImGuiWindowType.provide_full_screen_dock_space
        )

        docking_params = hello_imgui.DockingParams()
        docking_params.docking_splits = _create_default_docking_splits()
        docking_params.dockable_windows = _create_dockable_windows()
        docking_params.main_dock_space_node_flags = (
            imgui.DockNodeFlags_.auto_hide_tab_bar + imgui.DockNodeFlags_.no_undocking
        )
        self.params.docking_params = docking_params
        return

    def _setup_save_settings(self) -> None:
        self.params.ini_folder_type = hello_imgui.IniFolderType.current_folder
        self.params.ini_filename = ".local/mpl-theme-tweaker.ini"
        return

    def _setup_addon(self) -> None:
        self.addon_params = immapp.AddOnsParams(with_implot=True)
        return

    def _setup_app_window_params(self) -> None:
        awp = self.params.app_window_params

        awp.window_title = "mpl-theme-tweaker"
        awp.window_geometry.size = (640, 960)
        awp.restore_previous_geometry = True
        awp.borderless = False
        awp.borderless_movable = True
        awp.borderless_resizable = True
        awp.borderless_closable = True
        return

    def _setup_imgui_window_params(self) -> None:
        iwp = self.params.imgui_window_params
        iwp.menu_app_title = "File"
        iwp.show_status_bar = True

        iwp.show_menu_bar = True
        iwp.show_menu_app = False
        iwp.show_menu_view = False

        iwp.default_imgui_window_type = (
            hello_imgui.DefaultImGuiWindowType.provide_full_screen_dock_space
        )
        iwp.enable_viewports = True
        return

    def _setup_callbacks(self) -> None:
        cb = self.params.callbacks
        cb.load_additional_fonts = load_fonts
        cb.show_status = lambda: imgui.text("CopyRight pplotter.com @ 2025")
        cb.show_menus = self.show_menu_gui
        cb.show_app_menu_items = self.show_app_menu_gui
        cb.post_init = lambda: set_window_icon()
        cb.before_exit = lambda: print("before_exit callback called")
        cb.setup_imgui_style = setup_theme
        return

    def run(self) -> None:
        immapp.run(self.params, self.addon_params)
        return

    def show_menu_gui(self) -> None:
        hello_imgui.show_app_menu(self.params)
        hello_imgui.show_view_menu(self.params)

        if imgui.begin_menu("Style"):
            if imgui.begin_menu("Official"):
                clicked, _ = imgui.menu_item("Default", "", False)
                if clicked:
                    self.params_window.reset_by_default()

                for style in self.styles:
                    clicked, _ = imgui.menu_item(style, "", False)
                    if clicked:
                        self.params_window.reset_by_style(style)
                imgui.end_menu()

            imgui.end_menu()
        return

    def show_app_menu_gui(self) -> None:
        imgui.menu_item("Open", "", False)
        imgui.menu_item("Open Recent", "", False)
        imgui.separator_text("Save")
        imgui.menu_item("Save", "", False)
        imgui.menu_item("Save As", "", False)
        imgui.menu_item("Copy to Clipboard", "", False)

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


def main():
    hello_imgui.set_assets_folder(assetsPath().as_posix())

    app = Application()
    app.run()


if __name__ == "__main__":
    main()
