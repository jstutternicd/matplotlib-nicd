"""Register NICD gradient colormaps with matplotlib.

Companion to ``~/.matplotlib/stylelib/nicd.mplstyle``. The mplstyle file
sets the discrete series palette and font, but matplotlib stylesheets
can't register colormaps or carry ``Path``-based markers — those have to
happen in code. Import this module once per process to add the three
gradients (``nicd-green``, ``nicd-blue``, ``nicd-pink``) and the named
colours; call :func:`use` to apply the full style including the marker
cycle:

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path.home() / ".matplotlib"))
    import nicd_palette
    nicd_palette.use()             # style + colours + markers

    plt.imshow(arr, cmap="nicd-green")

Each colormap is also registered in its ``_r`` reversed form.
"""
from __future__ import annotations

from cycler import cycler
import matplotlib as mpl
from matplotlib import colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.path import Path

# Named series colours, namespaced ``nicd:`` to mirror matplotlib's own
# ``tab:`` palette and avoid clashing with CSS names ("pink" / "purple"
# already mean other shades in matplotlib).
_NAMED_COLOURS = {
    "nicd:light-green": "#4fe18f",
    "nicd:dark-green":  "#002d30",
    "nicd:blue":        "#00c3d6",
    "nicd:pink":        "#ff709d",
    "nicd:purple":      "#a361ff",
    "nicd:light-grey":  "#f2f2f2",
}

_GRADIENTS = {
    "nicd-green": ("#4fe18f", "#00b0a2"),
    "nicd-blue":  ("#00c3d6", "#00b0a2"),
    "nicd-pink":  ("#ff709d", "#aa1878"),
}

# Right triangle with the right angle at the top-right corner. Vertices
# span [-1, 1] to match matplotlib's built-in triangle markers, so it
# scales identically under ``markersize``.
RIGHT_TRIANGLE = Path(
    [(1.0, 1.0), (-1.0, 1.0), (1.0, -1.0), (1.0, 1.0)],
    [Path.MOVETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY],
)

# Default marker cycle: the right triangle, then a circle, repeating.
_MARKER_CYCLE = [RIGHT_TRIANGLE, "o"]


def _register() -> None:
    # Named colours: stuff straight into the global map. There is no public
    # registration API for individual named colours, but updating the dict
    # is how matplotlib's own ``tab:`` colours get there.
    mcolors._colors_full_map.update(_NAMED_COLOURS)

    # Colormaps: re-registration must be tolerated when this module is
    # reloaded in-process (e.g. Jupyter ``%run``).
    for name, stops in _GRADIENTS.items():
        cmap = LinearSegmentedColormap.from_list(name, list(stops))
        try:
            mpl.colormaps.register(cmap)
        except ValueError:
            mpl.colormaps.register(cmap, force=True)
        try:
            mpl.colormaps.register(cmap.reversed())
        except ValueError:
            mpl.colormaps.register(cmap.reversed(), force=True)


_register()


def use() -> None:
    """Apply the NICD style with the marker cycle wired up.

    Equivalent to ``plt.style.use("nicd")`` plus an ``axes.prop_cycle``
    override that pairs each series colour with a marker. The mplstyle
    file can carry the colour cycle but not ``Path``-based markers, so
    the marker half is set here.
    """
    import matplotlib.pyplot as plt

    plt.style.use("nicd")
    colours = list(_NAMED_COLOURS.keys())
    markers = [_MARKER_CYCLE[i % len(_MARKER_CYCLE)] for i in range(len(colours))]
    combined = cycler(color=colours) + cycler(marker=markers)
    # RcParams.__setitem__ validates ``axes.prop_cycle`` markers as string|int
    # only, rejecting Path objects. Downstream consumers (Axes._get_lines /
    # Line2D.set_marker) handle Path markers fine, so bypass validation via
    # the underlying dict to wire the cycle through.
    dict.__setitem__(plt.rcParams, "axes.prop_cycle", combined)
