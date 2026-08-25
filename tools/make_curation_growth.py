"""Regenerate the curation growth curve for curation.html.

The "Where it stands" section states what the pipeline has produced as three
numbers. This writes the shape behind them: how the catalogue actually grew,
reconstructed from the data repository's git history, so the page can show that
the curve changes slope when the agents arrive rather than merely asserting it.

The history lives in the *data* repository, not here -- this site only ever sees
`_datasets/` unpacked from an archive, with no commits attached. So the script
reads a local clone of shedding-hub/shedding-hub and writes normalized SVG
coordinates to `_data/curation_growth.yaml`, which curation.html renders in
Liquid.

Committed like `hero_trace.yaml`, and for the same reason: the site build is
pure Ruby and CI has no Python. Rerun it after a data drop, or to change the
geometry:

    python tools/make_curation_growth.py [--repo PATH]

Everything the chart draws is derived here, including the axis ticks and the
label positions, so regenerating is the only step needed to bring the figure
back in line with the catalogue. The page states the figure's `as_of` date, so
a chart that has not been regenerated reads as history rather than as a wrong
current total -- the live totals beside it come from `site.datasets`.
"""

import argparse
import bisect
import datetime as dt
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "_data" / "curation_growth.yaml"
DEFAULT_REPO = ROOT.parent / "shedding-hub"

# viewBox the figure is drawn in. Wider than it is tall: the story is a slope
# change over two years, which a squat frame reads better than a square one.
W, H = 1200.0, 380.0
PAD_L, PAD_R, PAD_T, PAD_B = 48.0, 118.0, 26.0, 34.0

# The first agent-extracted batch: the hinge the whole figure exists to show.
# Pinned by date rather than detected, because "the first batch the agents
# produced" is an editorial fact about how the work was done, not something
# recoverable from the shape of the curve.
AI_START = dt.date(2026, 2, 5)


def dataset_counts(repo: Path) -> list[tuple[dt.date, int]]:
    """Cumulative dataset count at every commit that touched `data/`."""
    log = subprocess.run(
        ["git", "-C", str(repo), "log", "--format=%H %ad", "--date=short",
         "--reverse", "main", "--", "data"],
        capture_output=True, text=True, check=True,
    ).stdout.split("\n")

    per_day: dict[dt.date, int] = {}
    for line in log:
        if not line.strip():
            continue
        sha, date = line.split()
        listing = subprocess.run(
            ["git", "-C", str(repo), "ls-tree", "-d", "--name-only", f"{sha}:data"],
            capture_output=True, text=True,
        ).stdout
        n = len([x for x in listing.split("\n") if x.strip()])
        day = dt.date.fromisoformat(date)
        # A day can carry several merges; the last state that day is the one.
        per_day[day] = max(per_day.get(day, 0), n)

    return sorted(per_day.items())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=DEFAULT_REPO,
                    help="path to a clone of shedding-hub/shedding-hub")
    args = ap.parse_args()

    if not (args.repo / ".git").is_dir():
        raise SystemExit(f"not a git clone: {args.repo}\nPass --repo PATH.")

    pts = dataset_counts(args.repo)
    if not pts:
        raise SystemExit("no data/ history found; is this the data repository?")

    days = [d for d, _ in pts]
    counts = [n for _, n in pts]
    t0, t1 = days[0], days[-1]
    span = (t1 - t0).days or 1

    # Head-room above the last value, rounded to the gridline step.
    step = 25
    y_max = max(step * 2, ((counts[-1] // step) + 1) * step)

    def x_of(d: dt.date) -> float:
        return PAD_L + (d - t0).days / span * (W - PAD_L - PAD_R)

    def y_of(n: float) -> float:
        return H - PAD_B - (n / y_max) * (H - PAD_T - PAD_B)

    def count_on(d: dt.date) -> int:
        """Cumulative count as of a date, carrying the last value forward."""
        i = bisect.bisect_right(days, d) - 1
        return counts[i] if i >= 0 else 0

    # A step path: the catalogue holds its value until a batch lands, so a
    # straight interpolation between merges would draw studies that did not
    # exist yet.
    path: list[str] = []
    prev_y = None
    for d, n in pts:
        x, y = x_of(d), y_of(n)
        if prev_y is not None:
            path.append(f"{x:.1f},{prev_y:.1f}")
        path.append(f"{x:.1f},{y:.1f}")
        prev_y = y
    path.append(f"{x_of(t1):.1f},{prev_y:.1f}")

    gridlines = [{"y": round(y_of(v), 1), "label": str(v)}
                 for v in range(0, y_max + 1, step)]

    xticks = []
    for year in range(t0.year, t1.year + 1):
        for month in (1, 7):
            d = dt.date(year, month, 1)
            if t0 <= d <= t1:
                xticks.append({"x": round(x_of(d), 1),
                               "label": d.strftime("%b %Y")})

    doc = {
        "as_of": t1.isoformat(),
        "width": W,
        "height": H,
        "baseline_y": round(y_of(0), 1),
        "plot_top": round(y_of(y_max), 1),
        "plot_left": round(PAD_L, 1),
        "plot_right": round(W - PAD_R, 1),
        "path": " ".join(path),
        "gridlines": gridlines,
        "xticks": xticks,
        # The AI era, drawn as a wash so the slope change has a named region
        # rather than relying on the reader to spot where it starts.
        "ai_band": {"x": round(x_of(AI_START), 1),
                    "width": round(x_of(t1) - x_of(AI_START), 1)},
        "ai_start": {
            "x": round(x_of(AI_START), 1),
            "y": round(y_of(count_on(AI_START)), 1),
            "date_label": AI_START.strftime("%b %Y"),
            "count": count_on(AI_START),
        },
        "start": {
            "x": round(x_of(t0), 1),
            "y": round(y_of(0), 1),
            "date_label": t0.strftime("%b %Y"),
        },
        "end": {
            "x": round(x_of(t1), 1),
            "y": round(y_of(counts[-1]), 1),
            "count": counts[-1],
            "date_label": t1.strftime("%b %Y"),
        },
        # What the catalogue held the day before the agents landed: the number
        # the page contrasts the current total against.
        "manual_era_end": count_on(AI_START - dt.timedelta(days=1)),
    }

    header = (
        "# Generated by tools/make_curation_growth.py from the data repository's\n"
        "# git history. Do not edit by hand -- rerun the script instead.\n"
    )
    DEST.write_text(header + yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    print(f"wrote {DEST}")
    print(f"  {len(pts)} change-days, {counts[-1]} studies as of {t1}")
    print(f"  manual era ended at {doc['manual_era_end']}, "
          f"AI era starts {AI_START} at {doc['ai_start']['count']}")


if __name__ == "__main__":
    main()
