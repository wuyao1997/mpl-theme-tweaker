from imgui_bundle import hello_imgui, imgui


from mpl_theme_tweaker._global import set_app_key


def setup_theme() -> None:
    # Apply default style
    hello_imgui.imgui_default_settings.setup_default_imgui_style()
    # Create a tweaked theme
    tweaked_theme = hello_imgui.ImGuiTweakedTheme()
    tweaked_theme.theme = hello_imgui.ImGuiTheme_.microsoft_style
    hello_imgui.apply_tweaked_theme(tweaked_theme)
    return


def load_fonts() -> None:
    hello_imgui.get_runner_params().callbacks.default_icon_font = (
        hello_imgui.DefaultIconFont.font_awesome6
    )
    hello_imgui.imgui_default_settings.load_default_font_with_font_awesome_icons()

    title_font = hello_imgui.load_font_ttf_with_font_awesome_icons(
        "fonts/Roboto/Roboto-BoldItalic.ttf", 18
    )
    set_app_key("title_font", title_font)
    return


def show_app_menu_items() -> None:
    clicked, _ = imgui.menu_item("A Custom app menu item", "", False)
    if clicked:
        hello_imgui.log(hello_imgui.LogLevel.info, "Clicked on A Custom app menu item")
    return
