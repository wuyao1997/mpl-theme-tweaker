from abc import ABC
from typing import Any

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from imgui_bundle import imgui, imgui_toggle  # type: ignore

from mpl_theme_tweaker._global import get_app_key


class Entry(ABC):
    value: Any
    label: str
    key: str
    updated: bool

    def __init__(self, label: str, key: str, sameline: bool = False):
        self.label: str = label
        self.key: str = key
        self.updated: bool = False
        self.sameline: bool = sameline

    def gui(self) -> None:
        if self.sameline:
            imgui.same_line()

        # print(self)
        return

    def update_mpl_rcparams(self, value) -> None:
        plt.rcParams[self.key] = value
        self.value = value

        self.updated = True
        return

    def update(self) -> None:
        self.updated = False
        return

    def need_update(self) -> bool:
        return self.updated

    def reset_by_rcParams(self) -> None:
        self.value = plt.rcParams[self.key]
        return

    def __repr__(self) -> str:
        return f"{self.label}: {self.value}"

    def to_str(self) -> str:
        return f"{self.key}: {self.value}"


class SeparatorEntry(Entry):
    def __init__(self, label: str):
        super().__init__(label, "")

        self.value = None

    def gui(self) -> None:
        title_font = get_app_key("title_font")
        imgui.push_font(title_font, title_font.legacy_size)
        imgui.separator_text(self.label)
        imgui.pop_font()
        return

    def update_mpl_rcparams(self, value) -> None:
        pass

    def reset_by_rcParams(self) -> None:
        pass

    def to_str(self) -> str:
        return ""


class BoolEntry(Entry):
    def __init__(
        self, label: str, key: str, value: bool = False, sameline: bool = False
    ):
        super().__init__(label, key, sameline)
        self.value = value

    def gui(self) -> None:
        super().gui()

        # changed, new_value = imgui.checkbox(self.label, self.value)
        toggle_config = imgui_toggle.ios_style(size_scale=0.2)
        changed, new_value = imgui_toggle.toggle(
            self.label, self.value, config=toggle_config
        )
        if changed:
            if new_value != self.value:
                self.update_mpl_rcparams(new_value)
        return


class IntEntry(Entry):
    """
    dict info should like:
    {
        "value": 0,
        "vmin": 0,
        "vmax": 100,
        "step": 1,
        "stepfast": 10,
    }
    """

    def __init__(
        self,
        label: str,
        key: str,
        info: dict[str, Any],
        sameline: bool = False,
    ):
        super().__init__(label, key, sameline)

        self.value = info.get("value", 0)
        self.vmin = info.get("vmin")
        self.vmax = info.get("vmax")
        self.step = info.get("step", 1)
        self.stepfast = info.get("stepfast", self.step)

    def gui(self) -> None:
        super().gui()

        changed, new_value = imgui.input_int(
            self.label, self.value, self.step, self.stepfast
        )

        if changed:
            if not (self.vmin is None or self.vmax is None):
                new_value = max(self.vmin, min(new_value, self.vmax))

            if new_value != self.value:
                self.update_mpl_rcparams(new_value)

        return


class FloatEntry(Entry):
    """
    dict info should like:
    {
        "value": 0.0,
        "vmin": 0.0,
        "vmax": 100.0,
        "step": 1.0,
        "stepfast": 10.0,
        "format": "%.3f",
    }
    """

    def __init__(
        self,
        label: str,
        key: str,
        info: dict[str, Any],
        sameline: bool = False,
    ):
        super().__init__(label, key, sameline)

        self.value = info.get("value", 0.0)
        self.vmin = info.get("vmin")
        self.vmax = info.get("vmax")
        self.step = info.get("step", 1.0)
        self.stepfast = info.get("stepfast", self.step)
        self.format = info.get("format", "%.3f")

    def gui(self) -> None:
        super().gui()

        changed, new_value = imgui.input_float(
            self.label,
            self.value,
            self.step,
            self.stepfast,
            self.format,
        )
        if changed:
            if not (self.vmin is None or self.vmax is None):
                new_value = max(self.vmin, min(new_value, self.vmax))

            if new_value != self.value:
                self.update_mpl_rcparams(new_value)
        return

    def reset_by_rcParams(self) -> None:
        value = plt.rcParams[self.key]
        if isinstance(value, float):
            self.value = value
        return

    def to_str(self) -> str:
        return f"{self.key}: {self.value:.4f}"


class Float2Entry(Entry):
    """
    dict info should like:
    {
        "value": [0.0, 0.0],
        "vmin": 0.0,
        "vmax": 100.0,
        "format": "%.3f",
    }
    """

    def __init__(
        self,
        label: str,
        key: str,
        info: dict[str, Any],
        sameline: bool = False,
    ):
        super().__init__(label, key, sameline)

        self.value = info.get("value", 0.0)
        self.vmin = info.get("vmin")
        self.vmax = info.get("vmax")
        self.format = info.get("format", "%.3f")

    def gui(self) -> None:
        super().gui()

        changed, new_value = imgui.input_float2(self.label, self.value, self.format)
        if changed:
            if not (self.vmin is None or self.vmax is None):
                new_value = max(self.vmin, min(new_value, self.vmax))

            if new_value != self.value:
                self.update_mpl_rcparams(new_value)
        return

    def reset_by_rcParams(self) -> None:
        value = plt.rcParams[self.key]
        if isinstance(value, list) and len(value) == 2:
            try:
                value = [float(v) for v in value]
            except ValueError:
                return
            self.value = value
        return

    def to_str(self) -> str:
        return f"{self.key}: {self.value[0]:.4f}, {self.value[1]:.4f}"


class Float4Entry(Entry):
    pass


class StrEntry(Entry):
    """
    dict info should like:
    {
        "value": 0,
        "items": ["AA", "BB", "CC", "DD"],
    }
    """

    def __init__(self, label: str, key: str, info: dict[str, Any]):
        super().__init__(label, key)
        self.value = info.get("value", 0)
        self.items: list[str] = info.get("items", [])

    def gui(self) -> None:
        super().gui()

        changed, new_value = imgui.combo(self.label, self.value, self.items)
        if changed:
            if new_value != self.value:
                self.update_mpl_rcparams(new_value)
        return

    def update_mpl_rcparams(self, value) -> None:
        self.value = value
        plt.rcParams[self.key] = self.items[self.value]

        self.updated = True
        return

    def reset_by_rcParams(self) -> None:
        value = plt.rcParams[self.key]
        if self.key == "font.family":
            value = value[0] if value else value

        if value in self.items:
            self.value = self.items.index(value)
        return

    def to_str(self) -> str:
        return f'{self.key}: "{self.items[self.value]}"'


class ColorEntry(Entry):
    """
    dict info should like:
    {
        "value": [1,1,1,1],
    }
    """

    def __init__(
        self,
        label: str,
        key: str,
        info: dict[str, Any] | None = None,
        sameline: bool = False,
    ):
        super().__init__(label, key, sameline)
        self.value = info.get("value", [1, 1, 1, 1]) if info else [1, 1, 1, 1]

        self.color_flags = imgui.ColorEditFlags_.no_inputs.value
        # imgui.ColorEditFlags_.no_label.value

    def gui(self) -> None:
        super().gui()

        changed, new_value = imgui.color_edit4(
            self.label, self.value, flags=self.color_flags
        )
        if changed:
            delta = [abs(new - old) for new, old in zip(new_value, self.value)]
            if any(d > 0.0005 for d in delta):
                self.update_mpl_rcparams(new_value)

        return

    def reset_by_rcParams(self) -> None:
        value = plt.rcParams[self.key]

        # handle "auto" and "inherit" cases
        if value == "auto":
            if self.key in ["lines.markerfacecolor", "axes.edgecolor"]:
                value = plt.rcParams["lines.color"]
            elif self.key == "axes.titlecolor":
                value = plt.rcParams["text.color"]
        elif value == "inherit":
            if self.key == "xtick.labelcolor":
                value = plt.rcParams["xtick.color"]
            elif self.key == "ytick.labelcolor":
                value = plt.rcParams["ytick.color"]
            elif self.key == "legend.facecolor":
                value = plt.rcParams["axes.facecolor"]

        try:
            rgba = mcolors.to_rgba(value)
        except ValueError:
            print(f"Invalid color value for {self.key}: {value}, use white instead.")
            rgba = [1.0, 1.0, 1.0, 1.0]
            return

        self.value = rgba
        return

    def to_str(self) -> str:
        return f'{self.key}: "{mcolors.to_hex(self.value)}"'
