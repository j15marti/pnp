#!/usr/bin/env python3
"""Plot the exact proved accounting envelope from the finite-audit JSON."""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output-base", type=Path, required=True)
    args = parser.parse_args()
    record = json.loads(args.results.read_text())["illustration"]
    h, ell, delta = record["H"], record["ell"], record["delta"]
    time_floor = delta * ((h + ell - 1) // ell)

    def phi(z):
        q = max(0, z // ell)
        return q * z - ell * q * (q + 1) // 2

    def envelope(paid):
        q, rem = divmod(paid, delta)
        return (delta - rem) * phi(h - ell * q) + rem * phi(h - ell * (q + 1))

    initial = envelope(0)
    xs = [i / 400 for i in range(401)]
    ys = [envelope(round(x * time_floor)) / initial for x in xs]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(9.2, 5.6), dpi=180)
    ax.fill_between(xs, ys, color="#dceaf6", alpha=0.9)
    ax.plot(xs, ys, color="#175e91", linewidth=2.8)
    for x in (0, .25, .5, .75, 1):
        y = envelope(round(x * time_floor)) / initial
        ax.scatter([x], [y], color="#175e91", s=34, zorder=3)
        if x not in (0, 1):
            ax.annotate(f"{y:.1%}", (x, y), xytext=(10, 8),
                        textcoords="offset points", color="#174767", fontsize=10)
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 1.05)
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.set_xlabel("Preprocessing time as a fraction of the guaranteed time floor", labelpad=12)
    ax.set_ylabel("Lower bound on remaining cumulative cost\nrelative to its initial lower bound", labelpad=10)
    ax.grid(color="#e6e9ec", linewidth=.8)
    ax.set_axisbelow(True)
    ax.set_title("Paid preprocessing and the cost that remains", loc="left",
                 fontweight="bold", fontsize=16, pad=18)
    fig.text(.13, .035,
             f"Theorem arithmetic, not a runtime measurement.  r = {record['r']:,}; "
             f"Q = {record['Q']}; d = {record['d']}.",
             fontsize=9, color="#5b6269")
    fig.subplots_adjust(left=.13, right=.96, bottom=.20, top=.86)
    args.output_base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output_base.with_suffix(".png"), dpi=180, transparent=True)
    fig.savefig(args.output_base.with_suffix(".svg"), transparent=True)
    plt.close(fig)


if __name__ == "__main__":
    main()
