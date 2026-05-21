#!/usr/bin/env python3
"""Show off the NICD matplotlib style + named colours + gradient colormaps.

Run from the repo root:

    uv run --with matplotlib python demo.py

or, with matplotlib already installed:

    python demo.py

Writes ``demo.png`` next to this script.
"""
from __future__ import annotations

import pathlib

import nicd_palette  # noqa: F401  -- side-effect: registers names + cmaps

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.gridspec import GridSpec  # noqa: E402


PALETTE = [
    "nicd:light-green",
    "nicd:dark-green",
    "nicd:blue",
    "nicd:pink",
    "nicd:purple",
    "nicd:light-grey",
]
PALETTE_LABELS = [name.split(":", 1)[1].replace("-", " ") for name in PALETTE]
GRADIENTS = ["nicd-green", "nicd-blue", "nicd-pink"]


def main() -> None:
    plt.style.use("nicd")

    fig = plt.figure(figsize=(13, 8), constrained_layout=True)
    fig.suptitle("NICD matplotlib style", fontsize=22, fontweight="bold")

    gs = GridSpec(5, 3, figure=fig, height_ratios=[2.6, 2.6, 0.5, 0.5, 0.5])

    # --- Top-left: sinusoids using axes.prop_cycle ----------------------
    ax_lines = fig.add_subplot(gs[0:2, :2])
    x = np.linspace(0, 4 * np.pi, 400)
    for i, label in enumerate(PALETTE_LABELS):
        ax_lines.plot(x, np.sin(x + i * 0.5) + i * 0.25, linewidth=2.2, label=label)
    ax_lines.set_title("Series palette  (axes.prop_cycle)")
    ax_lines.set_xlabel("x")
    ax_lines.set_ylabel("y")
    ax_lines.legend(loc="upper right", ncols=3, fontsize=9)

    # --- Top-right: bars use the same cycle by default ------------------
    ax_bars = fig.add_subplot(gs[0:2, 2])
    heights = [4.2, 3.0, 5.1, 2.4, 4.7, 3.6]
    ax_bars.bar(
        range(len(PALETTE)), heights, color=PALETTE, edgecolor="#002d30", linewidth=0.5
    )
    ax_bars.set_xticks(range(len(PALETTE)))
    ax_bars.set_xticklabels(PALETTE_LABELS, rotation=35, ha="right", fontsize=9)
    ax_bars.set_title("Bars share the cycle")
    ax_bars.set_ylim(0, max(heights) * 1.15)

    # --- Bottom three rows: gradient colormap strips --------------------
    grad = np.linspace(0, 1, 512).reshape(1, -1)
    for row, name in enumerate(GRADIENTS, start=2):
        ax = fig.add_subplot(gs[row, :])
        ax.imshow(grad, aspect="auto", cmap=name)
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_ylabel(name, rotation=0, ha="right", va="center", labelpad=12, fontsize=11)
        for spine in ax.spines.values():
            spine.set_visible(False)

    out = pathlib.Path(__file__).resolve().parent / "demo.png"
    fig.savefig(out)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
