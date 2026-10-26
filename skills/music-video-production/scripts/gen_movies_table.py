#!/usr/bin/env python3
"""Build the flat batch-clip table for a video tool from a project's movies.md.

Primary format is YAML (one mapping per clip):

    - id: "01"
      name: <scene name>
      duration: 8
      ref-image1: <file>
      ref-image2: ""
      ref-image3: ""
      prompt: |-
        <prompt, verbatim multi-line>
      lyrics: <matching lyric>

`--format csv` still emits scene-no,scene-name,duration,ref-file1..3,prompt
with the prompt flattened to one physical line.

Source of truth is movies.md: no prompt is ever re-typed. duration comes from
`秒数**: N 秒`, ref-image1..3 from the numbered upload list (empty when the
clip has fewer), lyrics from `対応歌詞`.

Usage: python gen_movies_table.py <project_dir> [-f yaml|csv] [-o <file>]
Exit 0 on success; prints rows and total seconds, NG lines for broken clips.
"""

import argparse
import csv
import io
import os
import re

MAX_REFS = 3
QUOTE_TRIGGERS = set(':#,[]{}&*!|>\'"%@`?-')


def flatten(text):
    return re.sub(r"\s{2,}", " ", " ".join(p.strip() for p in text.split("\n") if p.strip())).strip()


def scalar(value, force_quote=False):
    """Minimal, dependency-free YAML scalar quoting."""
    s = str(value)
    need = (force_quote or s == "" or s != s.strip()
            or s[0] in QUOTE_TRIGGERS or s[-1] == ":"
            or ": " in s or " #" in s or "\n" in s
            or s.lower() in {"true", "false", "null", "yes", "no", "on", "off", "~"}
            or re.fullmatch(r"[-+]?[0-9.]+([eE][-+]?[0-9]+)?", s) is not None)
    if not need:
        return s
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def to_yaml(rows):
    out = []
    for r in rows:
        out.append(f'- id: {scalar(r["id"], force_quote=True)}')
        out.append(f'  name: {scalar(r["name"])}')
        out.append(f'  duration: {r["duration"]}')
        for i in range(MAX_REFS):
            out.append(f'  ref-image{i + 1}: {scalar(r["refs"][i] if i < len(r["refs"]) else "")}')
        out.append("  prompt: |-")
        for line in r["prompt_raw"].split("\n"):
            out.append("    " + line if line.strip() else "")
        out.append(f'  lyrics: {scalar(r["lyrics"])}')
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("-f", "--format", choices=["yaml", "csv"], default="yaml")
    ap.add_argument("-o", "--out", default=None)
    ap.add_argument("--encoding", default="utf-8-sig")
    ap.add_argument("--max-refs", type=int, default=MAX_REFS)
    args = ap.parse_args()

    md = io.open(os.path.join(args.project_dir, "movies.md"), encoding="utf-8").read()
    blocks = md.split("\n### Scene ")[1:]
    if not blocks:
        raise SystemExit("movies.md: no '### Scene' blocks")

    rows, problems = [], []
    for block in blocks:
        head, body = block.split("\n", 1)
        m = re.match(r"(\S+) — (.+)$", head)
        if not m:
            raise SystemExit("unparsable scene header: " + head)
        num, name = m.group(1), m.group(2).strip()

        secs = re.search(r"秒数\*\*:\s*(\d+)\s*秒", body)
        if not secs:
            problems.append(f"{num}: no `秒数**: N 秒` field")
            continue

        files = re.findall(r"^\s+\d+\.\s+`([^`]+)`", body, flags=re.M)
        if len(files) > args.max_refs:
            raise SystemExit(f"{num}: {len(files)} refs > {args.max_refs} slots")
        if not files:
            problems.append(f"{num}: no numbered upload list")

        pm = re.search(r"```text\n(.*?)\n```", body, flags=re.S)
        if not pm:
            problems.append(f"{num}: no ```text block")
            continue
        raw = pm.group(1).strip("\n")

        ly = re.search(r"- \*\*対応歌詞\*\*:\s*(.+)", body)
        lyrics = ly.group(1).strip() if ly else ""
        if not lyrics:
            problems.append(f"{num}: no 対応歌詞")

        if "non_diegetic_music" not in raw:
            problems.append(f"{num}: no non_diegetic_music in prompt")

        rows.append(dict(id=num, name=name, duration=secs.group(1), refs=files,
                         prompt_raw=raw, prompt=flatten(raw), lyrics=lyrics))

    if args.format == "yaml":
        out_path = os.path.join(args.project_dir, args.out or "movies.yaml")
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(to_yaml(rows))
    else:
        out_path = os.path.join(args.project_dir, args.out or "movies.csv")
        with open(out_path, "w", encoding=args.encoding, newline="") as f:
            w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            w.writerow(["scene-no", "scene-name", "duration",
                        "ref-file1", "ref-file2", "ref-file3", "prompt"])
            for r in rows:
                w.writerow([r["id"], r["name"], r["duration"], *r["refs"],
                            *[""] * (args.max_refs - len(r["refs"])), r["prompt"]])

    total = sum(int(r["duration"]) for r in rows)
    for p in problems:
        print("NG:", p)
    print(f"rows={len(rows)} total={total}s -> {out_path}")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
