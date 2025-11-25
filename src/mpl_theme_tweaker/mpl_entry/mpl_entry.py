from abc import ABC, abstractmethod
from typing import Any

import matplotlib.pyplot as plt
from imgui_bundle import imgui


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


class BoolEntry(Entry):
    def __init__(
        self, label: str, key: str, value: bool = False, sameline: bool = False
    ):
        super().__init__(label, key, sameline)
        self.value = value

    def gui(self) -> None:
        super().gui()

        changed, new_value = imgui.checkbox(self.label, self.value)
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
        pass


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
        # pass, because value from rcParams may not a tuple
        # self.value = plt.rcParams[self.key]
        # print(f"{self.key}, {self.value}, {plt.rcParams[self.key]}")
        return
