"""Register NICD gradient colormaps with matplotlib.

Companion to ``~/.matplotlib/stylelib/nicd.mplstyle``. The mplstyle file
sets the discrete series palette and font, but matplotlib stylesheets
can't register colormaps — that has to happen in code. Import this module
once per process to add the three gradients (``nicd-green``, ``nicd-blue``,
``nicd-pink``):

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path.home() / ".matplotlib"))
    import nicd_palette  # noqa: F401  -- registers cmaps as a side-effect

    plt.imshow(arr, cmap="nicd-green")

Each colormap is also registered in its ``_r`` reversed form.
"""
from __future__ import annotations

import matplotlib as mpl
from matplotlib import colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

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
