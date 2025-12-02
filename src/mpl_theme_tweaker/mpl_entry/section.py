from abc import ABC, abstractmethod

from mpl_theme_tweaker.mpl_entry.mpl_entry import (
    BoolEntry,
    ColorEntry,
    Entry,
    FloatEntry,
    Float2Entry,
    IntEntry,
    MarkerStyleEntry,
    SeparatorEntry,
    StrEntry,
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

    def to_str(self) -> str:
        header = f"## {'*' * 71}\n## * {self.get_name():<68}*\n## {'*' * 71}\n"
        body: list[str] = []
        for entry in self.entries:
            body.append(entry.to_str())

        return header + "\n".join(body)


class FigureSection(Section):
    __SECTION_NAME__ = "Figure"

    def __init__(self):
        super().__init__()

    def _setup_entries(self) -> list[Entry]:
        frameon = BoolEntry("frame on", "figure.frameon", True)
        use_constrained = BoolEntry(
            "constrained layout", "figure.constrained_layout.use"
        )

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
        figsize = Float2Entry(
            "figsize",
            "figure.figsize",
            {
                "value": [6.4, 4.8],
                "vmin": 0.0,
                "vmax": 100.0,
                "format": "%.3f",
            },
        )

        facecolor = ColorEntry("face color", "figure.facecolor")
        edgecolor = ColorEntry("edge color", "figure.edgecolor", sameline=True)

        titlesize = StrEntry(
            "title size",
            "figure.titlesize",
            {
                "value": 3,
                "items": [
                    "xx-small",
                    "x-small",
                    "small",
                    "medium",
                    "large",
                    "x-large",
                    "xx-large",
                ],
            },
        )
        titleweight = StrEntry(
            "title weight",
            "figure.titleweight",
            {
                "value": 0,
                "items": ["normal", "bold"],
            },
        )

        labelsize = StrEntry(
            "label size",
            "figure.labelsize",
            {
                "value": 3,
                "items": [
                    "xx-small",
                    "x-small",
                    "small",
                    "medium",
                    "large",
                    "x-large",
                    "xx-large",
                ],
            },
        )
        labelweight = StrEntry(
            "label weight",
            "figure.labelweight",
            {
                "value": 0,
                "items": [
                    "normal",
                    "bold",
                ],
            },
        )

        _info = {
            "value": 0.125,
            "vmin": 0.0,
            "vmax": 1.0,
            "step": 0.005,
            "stepfast": 0.05,
            "format": "%.4f",
        }
        subplot_left = FloatEntry("left", "figure.subplot.left", _info)
        _info["value"] = 0.9
        subplot_right = FloatEntry("right", "figure.subplot.right", _info)
        _info["value"] = 0.11
        subplot_bottom = FloatEntry("bottom", "figure.subplot.bottom", _info)
        _info["value"] = 0.88
        subplot_top = FloatEntry("top", "figure.subplot.top", _info)
        wspace = FloatEntry(
            "wspace",
            "figure.subplot.wspace",
            {
                "value": 0.2,
                "vmin": -1.0,
                "vmax": 2.0,
                "step": 0.01,
                "stepfast": 0.1,
                "format": "%.4f",
            },
        )
        hspace = FloatEntry(
            "hspace",
            "figure.subplot.hspace",
            {
                "value": 0.2,
                "vmin": -1.0,
                "vmax": 2.0,
                "step": 0.01,
                "stepfast": 0.1,
                "format": "%.4f",
            },
        )

        # ==== savefig ==== #
        savefig_transparent = BoolEntry(
            "savefig transparent", "savefig.transparent", False
        )
        savefig_format = StrEntry(
            "savefig format",
            "savefig.format",
            {
                "value": 0,
                "items": ["png", "jpg", "jpeg", "pdf", "svg"],
            },
        )
        savefig_bbox = StrEntry(
            "savefig bbox",
            "savefig.bbox",
            {
                "value": 1,
                "items": ["tight", "standard"],
            },
        )
        animation_writer = StrEntry(
            "animation writer",
            "animation.writer",
            {
                "value": 0,
                "items": [
                    "ffmpeg",
                    "ffmpeg_file",
                    "imagemagick",
                    "imagemagick_file",
                    "html",
                    "pillow",
                ],
            },
        )

        return [
            frameon,
            use_constrained,
            dpi,
            figsize,
            facecolor,
            edgecolor,
            titlesize,
            titleweight,
            labelsize,
            labelweight,
            SeparatorEntry("Subplot"),
            subplot_left,
            subplot_right,
            subplot_bottom,
            subplot_top,
            wspace,
            hspace,
            SeparatorEntry("Misc"),
            savefig_transparent,
            savefig_format,
            savefig_bbox,
            animation_writer,
        ]


class AxesSection(Section):
    __SECTION_NAME__ = "Axes"

    def __init__(self):
        super().__init__()

    def _setup_entries(self) -> list[Entry]:
        facecolor = ColorEntry("face", "axes.facecolor")
        edgecolor = ColorEntry("edge", "axes.edgecolor", sameline=True)

        spinewidth = FloatEntry(
            "spines width",
            "axes.linewidth",
            {
                "value": 1.5,
                "vmin": 0.0,
                "vmax": 10.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )
        spines_left = BoolEntry("left", "axes.spines.left", True)
        spines_right = BoolEntry("right", "axes.spines.right", True, sameline=True)
        spines_bottom = BoolEntry("bottom", "axes.spines.bottom", True, sameline=True)
        spines_top = BoolEntry("top", "axes.spines.top", True, sameline=True)

        grid_color = ColorEntry("color", "grid.color")
        grid = BoolEntry("grid", "axes.grid")
        polar_grid = BoolEntry("polar axes grid", "polaraxes.grid", True, sameline=True)
        axes3d_grid = BoolEntry("3D axes grid", "axes3d.grid", True, sameline=True)
        grid_axis = StrEntry(
            "axis",
            "axes.grid.axis",
            {
                "value": 2,
                "items": ["x", "y", "both"],
            },
        )
        grid_which = StrEntry(
            "which",
            "axes.grid.which",
            {
                "value": 2,
                "items": ["major", "minor", "both"],
            },
        )
        grid_linestyle = StrEntry(
            "linestyle",
            "grid.linestyle",
            {
                "value": 0,
                "items": ["-", "--", "-.", ":"],
            },
        )
        grid_linewidth = FloatEntry(
            "linewidth",
            "grid.linewidth",
            {
                "value": 0.8,
                "vmin": 0.0,
                "vmax": 10.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )
        grid_alpha = FloatEntry(
            "alpha",
            "grid.alpha",
            {
                "value": 0.5,
                "vmin": 0.0,
                "vmax": 1.0,
                "step": 0.05,
                "stepfast": 0.1,
                "format": "%.2f",
            },
        )

        titlecolor = ColorEntry("color ", "axes.titlecolor")
        title_location = StrEntry(
            "location",
            "axes.titlelocation",
            {
                "value": 0,
                "items": ["left", "center", "right"],
            },
        )
        titlesize = StrEntry(
            "size",
            "axes.titlesize",
            {
                "value": 0,
                "items": ["small", "medium", "large"],
            },
        )
        titleweight = StrEntry(
            "weight",
            "axes.titleweight",
            {
                "value": 0,
                "items": ["normal", "bold"],
            },
        )
        titley = FloatEntry(
            "title y",
            "axes.titley",
            {
                "value": 1.1,
                "vmin": -1.0,
                "vmax": 2.0,
                "step": 0.01,
                "stepfast": 0.1,
                "format": "%.3f",
            },
        )
        titlepad = FloatEntry(
            "title pad",
            "axes.titlepad",
            {
                "value": 6.0,
                "vmin": -10.0,
                "vmax": 20.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )

        labelcolor = ColorEntry("color  ", "axes.labelcolor")
        labelsize = StrEntry(
            "label size",
            "axes.labelsize",
            {
                "value": 0,
                "items": ["small", "medium", "large"],
            },
        )
        labelweight = StrEntry(
            "label weight",
            "axes.labelweight",
            {
                "value": 0,
                "items": ["normal", "bold"],
            },
        )
        labelpad = FloatEntry(
            "label pad",
            "axes.labelpad",
            {
                "value": 6.0,
                "vmin": -10.0,
                "vmax": 20.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )
        xlabelloc = StrEntry(
            "x label location",
            "xaxis.labellocation",
            {
                "value": 1,
                "items": ["left", "center", "right"],
            },
        )
        ylabelloc = StrEntry(
            "y label location",
            "yaxis.labellocation",
            {
                "value": 1,
                "items": ["top", "center", "bottom"],
            },
        )

        unicode_minus = BoolEntry("unicode minus", "axes.unicode_minus", True)
        xmargin = FloatEntry(
            "x margin",
            "axes.xmargin",
            {
                "value": 0.05,
                "vmin": 0.0,
                "vmax": 0.5,
                "step": 0.01,
                "stepfast": 0.1,
                "format": "%.3f",
            },
        )
        ymargin = FloatEntry(
            "y margin",
            "axes.ymargin",
            {
                "value": 0.05,
                "vmin": 0.0,
                "vmax": 0.5,
                "step": 0.01,
                "stepfast": 0.1,
                "format": "%.3f",
            },
        )
        zmargin = FloatEntry(
            "z margin",
            "axes.zmargin",
            {
                "value": 0.05,
                "vmin": 0.0,
                "vmax": 0.5,
                "step": 0.01,
                "stepfast": 0.1,
                "format": "%.3f",
            },
        )

        autolimit_mode = StrEntry(
            "autolimit mode",
            "axes.autolimit_mode",
            {
                "value": 0,
                "items": ["data", "round_numbers"],
            },
        )

        axes3d_automargin = BoolEntry("automargin", "axes3d.automargin", False)

        axes3d_xaxis_panecolor = ColorEntry("xaxis pane", "axes3d.xaxis.panecolor")
        axes3d_yaxis_panecolor = ColorEntry(
            "yaxis pane", "axes3d.yaxis.panecolor", sameline=True
        )
        axes3d_zaxis_panecolor = ColorEntry(
            "zaxis pane", "axes3d.zaxis.panecolor", sameline=True
        )

        return [
            facecolor,
            edgecolor,
            SeparatorEntry("Spines"),
            spinewidth,
            spines_left,
            spines_right,
            spines_bottom,
            spines_top,
            SeparatorEntry("Grid"),
            grid_color,
            grid,
            polar_grid,
            axes3d_grid,
            grid_axis,
            grid_which,
            grid_linestyle,
            grid_linewidth,
            grid_alpha,
            SeparatorEntry("Title"),
            titlecolor,
            title_location,
            titlesize,
            titleweight,
            titley,
            titlepad,
            SeparatorEntry("Label"),
            labelcolor,
            labelsize,
            labelweight,
            labelpad,
            xlabelloc,
            ylabelloc,
            SeparatorEntry("Axes 3d"),
            axes3d_automargin,
            axes3d_xaxis_panecolor,
            axes3d_yaxis_panecolor,
            axes3d_zaxis_panecolor,
            SeparatorEntry("Misc"),
            unicode_minus,
            xmargin,
            ymargin,
            zmargin,
            autolimit_mode,
        ]


class TicksSection(Section):
    __SECTION_NAME__ = "Ticks"

    def __init__(self):
        super().__init__()

    def _setup_entries(self) -> list[Entry]:
        xtop = BoolEntry("x top", "xtick.top", False)
        xbottom = BoolEntry("x bottom", "xtick.bottom", True, sameline=True)
        yleft = BoolEntry("y left", "ytick.left", True, sameline=True)
        yright = BoolEntry("y right", "ytick.right", False, sameline=True)

        xcolor = ColorEntry("x color", "xtick.color")
        ycolor = ColorEntry("y color", "ytick.color", sameline=True)
        xlabeltop = BoolEntry("x label top", "xtick.labeltop", False)
        xlabelbottom = BoolEntry(
            "x label bottom", "xtick.labelbottom", True, sameline=True
        )
        ylabelleft = BoolEntry("y label left", "ytick.labelleft", True, sameline=True)
        ylabelright = BoolEntry(
            "y label right", "ytick.labelright", False, sameline=True
        )
        xlabelcolor = ColorEntry("x label color", "xtick.labelcolor")
        ylabelcolor = ColorEntry("y label color", "ytick.labelcolor", sameline=True)

        major_size = FloatEntry(
            "major size",
            "xtick.major.size",
            {
                "value": 3.5,
                "vmin": 0.0,
                "vmax": 10.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )
        major_width = FloatEntry(
            "major width",
            "xtick.major.width",
            {
                "value": 0.8,
                "vmin": 0.0,
                "vmax": 10.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )
        major_pad = FloatEntry(
            "major pad",
            "xtick.major.pad",
            {
                "value": 3.5,
                "vmin": 0.0,
                "vmax": 10.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )

        minor_size = FloatEntry(
            "minor size",
            "xtick.minor.size",
            {
                "value": 2.0,
                "vmin": 0.0,
                "vmax": 10.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )
        minor_width = FloatEntry(
            "minor width",
            "xtick.minor.width",
            {
                "value": 0.6,
                "vmin": 0.0,
                "vmax": 10.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )
        minor_pad = FloatEntry(
            "minor pad",
            "xtick.minor.pad",
            {
                "value": 3.5,
                "vmin": 0.0,
                "vmax": 10.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )
        xvisible = BoolEntry("x visible", "xtick.minor.visible", True)
        yvisible = BoolEntry("y visible", "ytick.minor.visible", True, sameline=True)

        return [
            SeparatorEntry("Tick line"),
            xtop,
            xbottom,
            yleft,
            yright,
            xcolor,
            ycolor,
            SeparatorEntry("Tick Label"),
            xlabeltop,
            xlabelbottom,
            ylabelleft,
            ylabelright,
            xlabelcolor,
            ylabelcolor,
            SeparatorEntry("Major tick"),
            major_size,
            major_width,
            major_pad,
            SeparatorEntry("Minor tick"),
            minor_size,
            minor_width,
            minor_pad,
            xvisible,
            yvisible,
        ]


class LinesSection(Section):
    __SECTION_NAME__ = "Lines"

    def __init__(self):
        super().__init__()

    def _setup_entries(self) -> list[Entry]:
        color = ColorEntry("color", "lines.color")
        linewidth = FloatEntry(
            "line width",
            "lines.linewidth",
            {
                "value": 1.5,
                "vmin": 0.0,
                "vmax": 10.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )
        linestyle = StrEntry(
            "line style",
            "lines.linestyle",
            {
                "value": 0,
                "items": ["-", "--", "-.", ":"],
            },
        )
        antialiased = BoolEntry("antialiased", "lines.antialiased", True)

        markerfacecolor = ColorEntry("facecolor", "lines.markerfacecolor")
        markeredgecolor = ColorEntry(
            "edge color", "lines.markeredgecolor", sameline=True
        )
        marker = MarkerStyleEntry("marker", "lines.marker")

        markeredgewidth = FloatEntry(
            "marker edge width",
            "lines.markeredgewidth",
            {
                "value": 1.0,
                "vmin": 0.0,
                "vmax": 10.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )

        markersize = FloatEntry(
            "marker size",
            "lines.markersize",
            {
                "value": 6.0,
                "vmin": 0.0,
                "vmax": 50.0,
                "step": 0.5,
                "stepfast": 5.0,
                "format": "%.3f",
            },
        )

        fillstyle = StrEntry(
            "markers fillstyle",
            "markers.fillstyle",
            {
                "value": 0,
                "items": ["full", "left", "right", "bottom", "top", "none"],
            },
        )

        patch_facecolor = ColorEntry("facecolor ", "patch.facecolor")
        patch_edgecolor = ColorEntry("edge color ", "patch.edgecolor", sameline=True)
        patch_force_edgecolor = BoolEntry(
            "patch force edgecolor", "patch.force_edgecolor", sameline=True
        )
        patch_linewidth = FloatEntry(
            "patch line width",
            "patch.linewidth",
            {
                "value": 1.0,
                "vmin": 0.0,
                "vmax": 10.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )
        patch_antialiased = BoolEntry("patch antialiased", "patch.antialiased", True)

        hatch_color = ColorEntry("hatch color", "hatch.color")
        hatch_linewidth = FloatEntry(
            "hatch line width",
            "hatch.linewidth",
            {
                "value": 1.0,
                "vmin": 0.0,
                "vmax": 10.0,
                "step": 0.1,
                "stepfast": 1.0,
                "format": "%.3f",
            },
        )

        return [
            SeparatorEntry("Line"),
            color,
            linewidth,
            linestyle,
            antialiased,
            SeparatorEntry("Marker"),
            markerfacecolor,
            markeredgecolor,
            marker,
            markeredgewidth,
            markersize,
            fillstyle,
            SeparatorEntry("Patch"),
            patch_facecolor,
            patch_edgecolor,
            patch_force_edgecolor,
            patch_linewidth,
            patch_antialiased,
            SeparatorEntry("Hatch"),
            hatch_color,
            hatch_linewidth,
        ]


class LegendSection(Section):
    __SECTION_NAME__ = "Legend"

    def __init__(self):
        super().__init__()

    def _setup_entries(self) -> list[Entry]:
        facecolor = ColorEntry("face color", "legend.facecolor")
        edgecolor = ColorEntry("edge color", "legend.edgecolor", sameline=True)
        labelcolor = ColorEntry("label color", "legend.labelcolor", sameline=True)
        loc = StrEntry(
            "legend location",
            "legend.loc",
            {
                "value": 0,
                "items": [
                    "best",
                    "upper right",
                    "upper left",
                    "lower left",
                    "lower right",
                    "right",
                    "center left",
                    "center right",
                    "lower center",
                    "upper center",
                    "center",
                ],
            },
        )
        fontsize = StrEntry(
            "font size",
            "legend.fontsize",
            {
                "value": 0,
                "items": [
                    "xx-small",
                    "x-small",
                    "small",
                    "medium",
                    "large",
                    "x-large",
                    "xx-large",
                ],
            },
        )

        frameon = BoolEntry("frame on", "legend.frameon", True)
        fancybox = BoolEntry("fancy box", "legend.fancybox", True, sameline=True)
        shadow = BoolEntry("shadow", "legend.shadow", False, sameline=True)
        framealpha = FloatEntry(
            "frame alpha",
            "legend.framealpha",
            {
                "value": 1.0,
                "vmin": 0.0,
                "vmax": 1.0,
                "step": 0.1,
                "stepfast": 0.5,
                "format": "%.3f",
            },
        )

        num_points = IntEntry(
            "number of points",
            "legend.numpoints",
            {
                "value": 1,
                "vmin": 1,
                "vmax": 5,
                "step": 1,
                "stepfast": 1,
            },
        )
        scatter_points = IntEntry(
            "scatter points",
            "legend.scatterpoints",
            {
                "value": 1,
                "vmin": 1,
                "vmax": 5,
                "step": 1,
                "stepfast": 1,
            },
        )
        markerscale = FloatEntry(
            "marker scale",
            "legend.markerscale",
            {
                "value": 1.0,
                "vmin": 0.0,
                "vmax": 5.0,
                "step": 0.1,
                "stepfast": 0.5,
                "format": "%.3f",
            },
        )

        borderpad = FloatEntry(
            "border pad",
            "legend.borderpad",
            {
                "value": 0.4,
                "vmin": 0.0,
                "vmax": 2.0,
                "step": 0.1,
                "stepfast": 0.1,
                "format": "%.3f",
            },
        )
        borderaxespad = FloatEntry(
            "border axes pad",
            "legend.borderaxespad",
            {
                "value": 0.5,
                "vmin": 0.0,
                "vmax": 2.0,
                "step": 0.1,
                "stepfast": 0.1,
                "format": "%.3f",
            },
        )
        labelspacing = FloatEntry(
            "label spacing",
            "legend.labelspacing",
            {
                "value": 0.5,
                "vmin": 0.0,
                "vmax": 3.0,
                "step": 0.1,
                "stepfast": 0.1,
                "format": "%.3f",
            },
        )
        handlelength = FloatEntry(
            "handle length",
            "legend.handlelength",
            {
                "value": 2.0,
                "vmin": 0.0,
                "vmax": 5.0,
                "step": 0.1,
                "stepfast": 0.5,
                "format": "%.3f",
            },
        )
        handleheight = FloatEntry(
            "handle height",
            "legend.handleheight",
            {
                "value": 0.7,
                "vmin": 0.0,
                "vmax": 3.0,
                "step": 0.1,
                "stepfast": 0.1,
                "format": "%.3f",
            },
        )
        handletextpad = FloatEntry(
            "handle text pad",
            "legend.handletextpad",
            {
                "value": 0.8,
                "vmin": 0.0,
                "vmax": 2.0,
                "step": 0.1,
                "stepfast": 0.1,
                "format": "%.3f",
            },
        )
        columnspacing = FloatEntry(
            "column spacing",
            "legend.columnspacing",
            {
                "value": 2.0,
                "vmin": 0.0,
                "vmax": 5.0,
                "step": 0.1,
                "stepfast": 0.5,
                "format": "%.3f",
            },
        )

        return [
            facecolor,
            edgecolor,
            labelcolor,
            loc,
            fontsize,
            SeparatorEntry("Frame"),
            frameon,
            shadow,
            fancybox,
            framealpha,
            SeparatorEntry("Marker"),
            num_points,
            scatter_points,
            markerscale,
            SeparatorEntry("Layout"),
            borderpad,
            borderaxespad,
            labelspacing,
            handlelength,
            handleheight,
            handletextpad,
            columnspacing,
        ]


class ImageSection(Section):
    __SECTION_NAME__ = "Image"

    def __init__(self):
        super().__init__()

    def _setup_entries(self) -> list[Entry]:
        aspect = StrEntry(
            "aspect",
            "image.aspect",
            {
                "value": 1,
                "items": ["auto", "equal"],
            },
        )
        interpolation = StrEntry(
            "interpolation",
            "image.interpolation",
            {
                "value": 0,
                "items": [
                    "none",
                    "nearest",
                    "bilinear",
                    "bicubic",
                    "spline16",
                    "spline36",
                    "hanning",
                    "hamming",
                    "hermite",
                    "kaiser",
                    "quadric",
                    "catrom",
                    "gaussian",
                    "bessel",
                    "mitchell",
                    "sinc",
                ],
            },
        )
        cmap = StrEntry(
            "colormap",
            "image.cmap",
            {
                "value": 0,
                "items": [
                    "viridis",
                    "hot",
                    "cool",
                    "coolwarm",
                    "binary",
                    "plasma",
                    "inferno",
                    "magma",
                    "cividis",
                    "jet",
                    "rainbow",
                ],
            },
        )
        lut = IntEntry(
            "lut",
            "image.lut",
            {
                "value": 256,
                "vmin": 0,
                "vmax": 256,
                "step": 1,
                "stepfast": 10,
            },
        )
        origin = StrEntry(
            "origin",
            "image.origin",
            {
                "value": 0,
                "items": ["upper", "lower"],
            },
        )

        resample = BoolEntry("resample", "image.resample", True)
        composite = BoolEntry("composite", "image.composite_image", True, sameline=True)

        return [aspect, interpolation, cmap, lut, origin, resample, composite]


class BoxplotSection(Section):
    __SECTION_NAME__ = "Boxplot"

    def __init__(self):
        super().__init__()

    def _setup_entries(self) -> list[Entry]:
        notch = BoolEntry("notch", "boxplot.notch", False)
        vertical = BoolEntry("vertical", "boxplot.vertical", True, sameline=True)
        patchartist = BoolEntry(
            "patch artist", "boxplot.patchartist", True, sameline=True
        )

        showmeans = BoolEntry("show means", "boxplot.showmeans", False)
        showcaps = BoolEntry("show caps", "boxplot.showcaps", True, sameline=True)
        showbox = BoolEntry("show box", "boxplot.showbox", True, sameline=True)
        showfliers = BoolEntry("show fliers", "boxplot.showfliers", True, sameline=True)
        meanline = BoolEntry("mean line", "boxplot.meanline", False, sameline=True)

        whiskers = FloatEntry(
            "whiskers",
            "boxplot.whiskers",
            {
                "value": 1.5,
                "vmin": 0.0,
                "vmax": 5.0,
                "step": 0.1,
                "stepfast": 0.5,
                "format": "%.3f",
            },
        )

        flier_marker = StrEntry(
            "flier marker",
            "boxplot.flierprops.marker",
            {
                "value": 0,
                "items": [
                    "o",
                    ".",
                    "^",
                    "v",
                    "<",
                    ">",
                    "8",
                    "s",
                    "p",
                    "P",
                    "*",
                    "h",
                    "H",
                    "X",
                    "D",
                    "d",
                ],
            },
        )

        flier_color = ColorEntry("flier color", "boxplot.flierprops.color")
        flier_markerfacecolor = ColorEntry(
            "flier marker facecolor",
            "boxplot.flierprops.markerfacecolor",
            sameline=True,
        )
        flier_markeredgecolor = ColorEntry(
            "flier marker edgecolor",
            "boxplot.flierprops.markeredgecolor",
            sameline=True,
        )

        flier_markeredgewidth = FloatEntry(
            "flier marker edgewidth",
            "boxplot.flierprops.markeredgewidth",
            {
                "value": 1.0,
                "vmin": 0.0,
                "vmax": 5.0,
                "step": 0.1,
                "stepfast": 0.5,
                "format": "%.3f",
            },
        )
        flier_markersize = FloatEntry(
            "flier marker size",
            "boxplot.flierprops.markersize",
            {
                "value": 6,
                "vmin": 0,
                "vmax": 20,
                "step": 1,
                "stepfast": 1,
                "format": "%.3f",
            },
        )
        flier_linestyle = StrEntry(
            "flier linestyle",
            "boxplot.flierprops.linestyle",
            {
                "value": 0,
                "items": ["none", "-", "--", "-.", ":"],
            },
        )
        flier_linewidth = FloatEntry(
            "flier line width",
            "boxplot.flierprops.linewidth",
            {
                "value": 1.0,
                "vmin": 0.0,
                "vmax": 5.0,
                "step": 0.1,
                "stepfast": 0.5,
                "format": "%.3f",
            },
        )

        box_color = ColorEntry("box color", "boxplot.boxprops.color")
        box_linewidth = FloatEntry(
            "box line width",
            "boxplot.boxprops.linewidth",
            {
                "value": 1.0,
                "vmin": 0.0,
                "vmax": 5.0,
                "step": 0.1,
                "stepfast": 0.5,
                "format": "%.3f",
            },
        )
        box_linestyle = StrEntry(
            "box linestyle",
            "boxplot.boxprops.linestyle",
            {
                "value": 0,
                "items": ["none", "-", "--", "-.", ":"],
            },
        )

        whisker_color = ColorEntry("whisker color", "boxplot.whiskerprops.color")
        whisker_linewidth = FloatEntry(
            "whisker line width",
            "boxplot.whiskerprops.linewidth",
            {
                "value": 1.0,
                "vmin": 0.0,
                "vmax": 5.0,
                "step": 0.1,
                "stepfast": 0.5,
                "format": "%.3f",
            },
        )
        whisker_linestyle = StrEntry(
            "whisker linestyle",
            "boxplot.whiskerprops.linestyle",
            {
                "value": 0,
                "items": ["none", "-", "--", "-.", ":"],
            },
        )

        cap_color = ColorEntry("cap color", "boxplot.capprops.color")
        cap_linewidth = FloatEntry(
            "cap line width",
            "boxplot.capprops.linewidth",
            {
                "value": 1.0,
                "vmin": 0.0,
                "vmax": 5.0,
                "step": 0.1,
                "stepfast": 0.5,
                "format": "%.3f",
            },
        )
        cap_linestyle = StrEntry(
            "cap linestyle",
            "boxplot.capprops.linestyle",
            {
                "value": 0,
                "items": ["none", "-", "--", "-.", ":"],
            },
        )

        median_color = ColorEntry("median color", "boxplot.medianprops.color")
        median_linewidth = FloatEntry(
            "median line width",
            "boxplot.medianprops.linewidth",
            {
                "value": 1.0,
                "vmin": 0.0,
                "vmax": 5.0,
                "step": 0.1,
                "stepfast": 0.5,
                "format": "%.3f",
            },
        )
        median_linestyle = StrEntry(
            "median linestyle",
            "boxplot.medianprops.linestyle",
            {
                "value": 0,
                "items": ["none", "-", "--", "-.", ":"],
            },
        )

        mean_color = ColorEntry("mean color", "boxplot.meanprops.color")
        mean_linewidth = FloatEntry(
            "mean line width",
            "boxplot.meanprops.linewidth",
            {
                "value": 1.0,
                "vmin": 0.0,
                "vmax": 5.0,
                "step": 0.1,
                "stepfast": 0.5,
                "format": "%.3f",
            },
        )
        mean_linestyle = StrEntry(
            "mean linestyle",
            "boxplot.meanprops.linestyle",
            {
                "value": 0,
                "items": ["none", "-", "--", "-.", ":"],
            },
        )
        mean_marker = StrEntry(
            "mean marker",
            "boxplot.meanprops.marker",
            {
                "value": 0,
                "items": [
                    "o",
                    ".",
                    "^",
                    "v",
                    "<",
                    ">",
                    "8",
                    "s",
                    "p",
                    "P",
                    "*",
                    "h",
                    "H",
                    "X",
                    "D",
                    "d",
                ],
            },
        )
        mean_markerfacecolor = ColorEntry(
            "mean markerfacecolor", "boxplot.meanprops.markerfacecolor"
        )
        mean_markeredgecolor = ColorEntry(
            "mean markeredgecolor", "boxplot.meanprops.markeredgecolor"
        )
        mean_markersize = FloatEntry(
            "mean markersize",
            "boxplot.meanprops.markersize",
            {
                "value": 6.0,
                "vmin": 0.0,
                "vmax": 20.0,
                "step": 0.1,
                "stepfast": 0.5,
                "format": "%.3f",
            },
        )

        return [
            notch,
            vertical,
            patchartist,
            showmeans,
            showcaps,
            showbox,
            showfliers,
            meanline,
            whiskers,
            SeparatorEntry("Flier Properties"),
            flier_marker,
            flier_color,
            flier_markerfacecolor,
            flier_markeredgecolor,
            flier_markeredgewidth,
            flier_markersize,
            flier_linestyle,
            flier_linewidth,
            SeparatorEntry("Box Properties"),
            box_color,
            box_linewidth,
            box_linestyle,
            SeparatorEntry("Whisker Properties"),
            whisker_color,
            whisker_linewidth,
            whisker_linestyle,
            SeparatorEntry("Cap Properties"),
            cap_color,
            cap_linewidth,
            cap_linestyle,
            SeparatorEntry("Median Properties"),
            median_color,
            median_linewidth,
            median_linestyle,
            SeparatorEntry("Mean Properties"),
            mean_color,
            mean_linewidth,
            mean_linestyle,
            mean_marker,
            mean_markerfacecolor,
            mean_markeredgecolor,
            mean_markersize,
        ]


class TextSection(Section):
    __SECTION_NAME__ = "Text"

    def __init__(self):
        super().__init__()

    def _setup_entries(self) -> list[Entry]:
        family = StrEntry(
            "font family",
            "font.family",
            {
                "value": 0,
                "items": ["serif", "sans-serif", "cursive", "fantasy", "monospace"],
            },
        )
        style = StrEntry(
            "font style",
            "font.style",
            {
                "value": 0,
                "items": ["normal", "italic", "oblique"],
            },
        )
        variant = StrEntry(
            "font variant",
            "font.variant",
            {
                "value": 0,
                "items": ["normal", "small-caps"],
            },
        )
        weight = StrEntry(
            "font weight",
            "font.weight",
            {
                "value": 0,
                "items": ["normal", "bold", "heavy", "light", "medium", "semibold"],
            },
        )
        size = FloatEntry(
            "font size",
            "font.size",
            {
                "value": 12.0,
                "vmin": 0.0,
                "vmax": 50.0,
                "step": 0.5,
                "stepfast": 5.0,
                "format": "%.3f",
            },
        )

        mathtext_fontset = StrEntry(
            "mathtext fontset",
            "mathtext.fontset",
            {
                "value": 0,
                "items": [
                    "dejavusans",
                    "dejavuserif",
                    "cm",
                    "stix",
                    "stixsans",
                    "custom",
                ],
            },
        )

        color = ColorEntry("text color", "text.color")
        antialiased = BoolEntry("antialiased", "text.antialiased", True, sameline=True)
        parse_math = BoolEntry("parse math", "text.parse_math", True, sameline=True)
        hinting = StrEntry(
            "text hinting",
            "text.hinting",
            {
                "value": 0,
                "items": ["default", "no_autohint", "force_autohint", "no_hinting"],
            },
        )

        return [
            SeparatorEntry("Font"),
            family,
            style,
            variant,
            weight,
            size,
            SeparatorEntry("LaTeX"),
            mathtext_fontset,
            SeparatorEntry("Text"),
            color,
            antialiased,
            parse_math,
            hinting,
        ]
