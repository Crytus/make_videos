#!/usr/bin/env python3
"""Validate a music-video project's derived artifacts.

Checks scenes.csv, optional refs CSV, and movies.md for the invariants that
break batch generation: unique seeds/filenames, missing suffixes, @imageN
counts that do not match the listed reference files, clips whose start frame
does not exist, and clips that forgot to suppress generated music.

Usage:
    python check_mv_assets.py <project_dir> [--prefix ab_] [--refs-csv ab_refs.csv]
                             [--ref-marker "reference sheets"] [--song-seconds 165]

The reference CSV is --refs-csv, otherwise <prefix>refs.csv, otherwise the only
*refs.csv in the project directory (none is fine: references are then skipped).

Exit code 0 = clean, 1 = problems found. Prints every problem with its scene id.
"""

import argparse
import csv
import glob
import os
import re
import sys

SCENE_COLS = ["scene_num", "scene_name", "seed", "file_name", "positive_prompt"]
CLIP_LABELS = ["秒数", "参照画像ファイル名", "プロンプト"]


def read_csv(path, problems, label):
    if not os.path.exists(path):
        problems.append(f"{label}: missing file {path}")
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        header = reader.fieldnames or []
    if [c.strip() for c in header] != SCENE_COLS:
        problems.append(f"{label}: header {header} != {SCENE_COLS}")
    for i, row in enumerate(rows, 1):
        for col in SCENE_COLS:
            if col not in row or row[col] in (None, ""):
                problems.append(f"{label}: row {i} ({row.get('scene_num','?')}) empty {col}")
    return rows


def check_unique(rows, problems, label):
    for col in ("seed", "file_name"):
        seen = {}
        for row in rows:
            v = (row.get(col) or "").strip()
            if v in seen:
                problems.append(f"{label}: duplicate {col} {v} in {seen[v]} and {row.get('scene_num')}")
            seen[v] = row.get("scene_num")


def find_refs_csv(base, prefix, explicit):
    """Locate the reference-image CSV. Returns a path or None."""
    if explicit:
        return explicit if os.path.isabs(explicit) else os.path.join(base, explicit)
    if prefix:
        candidate = os.path.join(base, f"{prefix}refs.csv")
        if os.path.exists(candidate):
            return candidate
    found = sorted(glob.glob(os.path.join(base, "*refs.csv")))
    if len(found) > 1:
        raise SystemExit(f"several refs CSVs found ({', '.join(os.path.basename(f) for f in found)}); "
                         "pass --refs-csv or --prefix")
    return found[0] if found else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--prefix", default=None, help="expected filename prefix, e.g. ab_")
    ap.add_argument("--refs-csv", default=None,
                    help="reference-image CSV (default: <prefix>refs.csv or the only *refs.csv)")
    ap.add_argument("--ref-marker", default="reference sheets",
                    help="substring every still prompt must contain ('' to skip)")
    ap.add_argument("--require-avoid", action="store_true",
                    help="require an AVOID line per clip (Hailuo-2.x dialect); off for h3-prompt-writing format")
    ap.add_argument("--label-style", choices=["auto", "at", "picture"], default="auto",
                    help="reference label dialect used in movies.md: @imageN (Hailuo 2.x bracket style) "
                         "or <Picture N> (h3-prompt-writing style)")
    ap.add_argument("--song-seconds", type=float, default=None,
                    help="song length; clip durations are compared against it")
    args = ap.parse_args()

    problems = []
    base = args.project_dir
    scenes_csv = os.path.join(base, "scenes.csv")
    movies_md = os.path.join(base, "movies.md")

    scenes = read_csv(scenes_csv, problems, "scenes.csv")
    check_unique(scenes, problems, "scenes.csv")

    refs_csv = find_refs_csv(base, args.prefix, args.refs_csv)
    refs_label = os.path.basename(refs_csv) if refs_csv else "refs CSV"
    ref_files = set()
    if refs_csv:
        refs = read_csv(refs_csv, problems, refs_label)
        check_unique(refs, problems, refs_label)
        ref_files = {(r.get("file_name") or "").strip() for r in refs}
        check_unique(scenes + refs, problems, "scenes+refs")

    known = {(r.get("file_name") or "").strip() for r in scenes} | ref_files

    for row in scenes:
        num = row.get("scene_num", "?")
        prompt = row.get("positive_prompt") or ""
        if "16:9" not in prompt:
            problems.append(f"scenes.csv {num}: prompt lacks 16:9")
        if "no text" not in prompt.lower():
            problems.append(f"scenes.csv {num}: prompt lacks 'no text'")
        if args.ref_marker and args.ref_marker not in prompt:
            problems.append(f"scenes.csv {num}: prompt lacks '{args.ref_marker}' line")
        if args.prefix and not (row.get("file_name") or "").startswith(args.prefix):
            problems.append(f"scenes.csv {num}: file_name missing prefix {args.prefix}")

    total = 0
    if not os.path.exists(movies_md):
        problems.append(f"movies.md: missing file {movies_md}")
    else:
        text = open(movies_md, encoding="utf-8").read()
        blocks = text.split("\n### Scene ")[1:]
        if not blocks:
            problems.append("movies.md: no '### Scene' blocks found")
        for block in blocks:
            num = block.split(" — ")[0].strip()
            for label in CLIP_LABELS:
                if label not in block:
                    problems.append(f"movies.md {num}: missing '{label}'")
            m = re.search(r"秒数\*\*:\s*(\d+)\s*秒", block)
            if m:
                secs = int(m.group(1))
                total += secs
                if not 4 <= secs <= 15:
                    problems.append(f"movies.md {num}: {secs}s outside 4-15s")
            else:
                problems.append(f"movies.md {num}: unparsable seconds")

            listed = re.findall(r"^\s+\d+\.\s+`([^`]+)`", block, flags=re.M)
            style = args.label_style
            if style == "auto":
                style = "picture" if re.search(r"<Picture\s+\d+>", block) else "at"
            mentioned = set(re.findall(r"@image(\d+)", block)) if style == "at" \
                else set(re.findall(r"<Picture\s+(\d+)>", block))
            if len(listed) != len(mentioned):
                tag = "@imageN" if style == "at" else "<Picture N>"
                problems.append(f"movies.md {num}: {len(listed)} files listed but {len(mentioned)} {tag} used")
            if listed and not listed[0].endswith(".png"):
                problems.append(f"movies.md {num}: first listed file is not a png")
            start = listed[0] if listed else None
            if start and start not in known:
                problems.append(f"movies.md {num}: start frame {start} not in scenes.csv/{refs_label}")
            for f in listed[1:]:
                if f not in ref_files and ref_files:
                    problems.append(f"movies.md {num}: support ref {f} not in {refs_label}")
            if "non_diegetic_music" not in block:
                problems.append(f"movies.md {num}: no non_diegetic_music line")
            if args.require_avoid and "AVOID" not in block:
                problems.append(f"movies.md {num}: no AVOID line")

        if args.song_seconds:
            drift = total - args.song_seconds
            print(f"clip total {total}s vs song {args.song_seconds:g}s  (drift {drift:+g}s)")
            if abs(drift) > args.song_seconds * 0.05:
                problems.append(f"movies.md: clip total {total}s drifts >5% from song length")

    for p in problems:
        print("NG:", p)
    print(f"\nscenes={len(scenes)} refs={len(ref_files)} clips={total}s problems={len(problems)}")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
