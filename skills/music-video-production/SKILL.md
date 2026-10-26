---
name: music-video-production
description: "Use when making an AI music video from lyrics. Runs the lyric→scene→still→clip pipeline with fixed consistency blocks and derived CSV/MD/YAML artifacts, ending in a movies.yaml that the make_videos tool turns into MiniMax H3 clips."
version: 2
author: Crytus
license: MIT
---

# Music video production (lyrics → scenes → stills → clips)

End-to-end pipeline for an AI music video built from a song's lyrics. One project directory, seven artifacts, seven stages.
The last artifact, `movies.yaml`, is the input of the `make_videos` command in this repository (ComfyUI + MiniMax H3).

## Companion skill: `h3-prompt-writing` (optional, recommended)

Stage 6 writes MiniMax H3 prompts. The authority on field names, labels and timing notation is the separate
**`h3-prompt-writing`** skill (`SKILL.md`, `references/base-en.txt` for T2VA / I2VA / FL2VA / L2VA,
`references/ref-en.txt` for Ref2VA). It is not bundled here. Look for it in this order and read the files before
writing clip prompts:

1. `../h3-prompt-writing/` — next to this skill
2. `~/.claude/skills/h3-prompt-writing/`
3. `~/.agents/skills/h3-prompt-writing/`
4. any other skills directory your agent uses

It may not appear in your agent's skill list even when it is installed — resolve it by path before concluding it is
absent. When it is missing, follow the rules summarised in Stage 6 below; they cover the I2VA and Ref2VA formats this
pipeline needs.

## Project layout

```
<project_dir>/
  plan.md           # 正 (source of truth): concept, fixed blocks, scene↔lyric map, scenes, ref prompts
  scenes.md         # production sheet: name / lyrics / description / refs / prompt per scene
  scenes.csv        # batch-image list: scene_num,scene_name,seed,file_name,positive_prompt  (utf-8-sig)
  <prefix>refs.csv  # same columns, one row per reference image  (e.g. ab_refs.csv)
  movies.md         # clip sheet for the video model: name / seconds / ref files / prompt
  movies.yaml       # batch-clip input for make_videos: id / name / duration / ref-image1..3 / prompt / lyrics
  config.yaml       # make_videos settings (`make_videos init`)
  <image_dir>/      # stills <prefix>01_*.png and references <prefix>ref_01_*.png (image_dir in config.yaml)
```

Use a short project prefix, including its trailing underscore, on every filename (`ab_` → `ab_01_opening.png`, `ab_ref_02_character-sheet.png`, `ab_refs.csv`). Never reuse a prefix from another song.

## Stage 1 — Scene planning from lyrics

1. Map every block: `[Intro] [Verse] [Chorus] [Inter] [Bridge] … [Outro] [Ending]`. Instrumental blocks still get scenes (establishing shot / metaphor / montage).
2. Give **multiple scenes to every Verse and Chorus** (~1 scene per lyric line; 4 lines → 4 scenes). Merge only where two lines form one image.
3. Inventory **24–26 scenes** for a 2:30–3:00 song plus a fixed closing scene `E-1`. Rough 6–8 s per scene.
4. Write a scene↔lyric table with: `# | scene name | section | matching lyric | 尺目安`. Mirroring the image/genre arc matters more than exact timing — mark times as 目安.
5. Choose one **visual device per emotional axis** and repeat it: e.g. "difference" = left/right diptych, "same heart" = one shared glowing light. Repetition of a device reads as intentional; variety reads as drift.

## Stage 2 — Fixed blocks (the consistency engine)

Define once, copy **verbatim** into every prompt. Four block types:

- **`CH1` / `CH2` …** — one block per character: species/age, exact hair or fur, eye colour, costume with colours, one distinguishing detail. Two characters → two blocks, plus a **lineup reference** that fixes their height relationship.
- **`ST`** — style, e.g. `cinematic live-action photography, soft 35mm film grain, …` or `soft watercolour and coloured-pencil illustration, …`
- **`JP`** (or any world block) — setting/nationality: biome, plants, architecture, materials. If the cast is not human, carry the setting through **plants, textures and palette**, never by adding extra people (ban them in the negative).
- **`CS2` / `CS1`** — consistency declaratives: `the same two characters as in every scene, identical faces, identical outfits, identical colors` for two-character shots, singular form for solo shots.

Prompt order is fixed and identical everywhere: `shot type → setting → character block → action → light → JP → ST → CS → references: → 16:9, no text`.

## Stage 3 — `plan.md`

Concept, palette, arc, camera rules, fixed blocks with the negative base, scene↔lyric table, per-scene detail (lyrics / 内容 / カメラ・光 / positive / negative / seed / file_name), editorial flow notes, generation notes, reference-image prompts, and the ref→scene mapping. Seeds: `1000` step `+100` for scenes, `4000` upward for references, `E-1` at the end of the scene range.

## Stage 4 — Reference images first

Generate before any scene still, in this order:

1. **Location parent plate** — the set that most scenes share (path/room/shore). Fix element positions in words ("path from lower left to the crest, tree at the upper centre").
2. **Character sheets** — 3 views + 3 expressions on a plain cream background, **no text, no labels, no swatches, no measurement lines**.
3. **Lineup** — the characters side by side, stating the height relation (multi-character songs only).
4. **Secondary locations** — one plate per lighting/weather state (night, rain, dusk, interior).

Rules: character refs keep character blocks verbatim + `CS1`; location refs say `no people present` / `no characters` and add `people, characters` to the negative; never let a day plate define light for a night or autumn scene (`lock the layout only, not the light`).

## Stage 5 — Stills: `scenes.md` + `scenes.csv`

- **Generate both files from `plan.md` by parsing it** (regex on `### Scene …` sections). Never retype prompts — drift between three files is the number-one failure of this pipeline.
- Every still prompt ends with a **reference line** naming the plates it must follow: `references: reference sheets ab_ref_02_character-sheet, ab_ref_01_location-path`.
- `scenes.md`: per scene → シーン名 / 曲構成 / 対応歌詞 / シーン説明 / カメラ・光 / 参照画像（ID+file）/ seed / file_name / positive / negative.
- `scenes.csv`: exactly `scene_num,scene_name,seed,file_name,positive_prompt`, UTF-8 **with BOM**, one row per scene, prompt in a single line.
- Negative prompts are resolved to full text in the MD (base + scene extras), and stay out of the CSV.

## Stage 6 — Clips: `movies.md`

Write the clip prompts in the **`h3-prompt-writing`** format (read `base-en.txt`, and `ref-en.txt` when reference plates are attached). Pick the mode by what is actually uploaded:

- **I2VA** — only the scene still is attached (make_videos `mode: i2v`, the default). The first line of the prompt is mandatory and verbatim:
  `For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.`
  Then a blank line, then `integrated_multimodal_description:`, `overall_soundscape:`, `non_diegetic_music:`.
- **Ref2VA** — the still **plus** character/location sheets are attached (make_videos `mode: r2v`). Use the six sections in order: `subject_definitions`, `summary` (with a `[reference generation + keyframe completion]`-style prefix), `retention_analysis` (`fully_preserved` / `partially_preserved` / `attribute_transfer` / `weak_reference`), `detailed_description`, `overall_soundscape`, `non_diegetic_music`. Give every sheet its own `<Subject N>` line and cite the still as `<Picture N>` only when it anchors a frame.
- **FL2VA / L2VA** only when the project deliberately supplies both ends of a shot.

Format rules that are easy to get wrong:

- Labels are `<Picture N>`, `<Subject N>`, `<Video N>`, `<Audio N>` — never `@image1`. Numbering follows upload order and stays stable across all sections.
- Shots: `[Shot 1]` carries no timestamp; later shots use `[Shot 2] At 00:03.500, ...` with strictly increasing times inside the clip duration.
- Camera moves are **natural English inside the shot**, with type + amplitude + speed: `The camera pushes in with small amplitude at slow speed toward her hands.` No bracket commands in this dialect.
- `overall_soundscape` = ambience and physical sound only; put singing/dialogue/lyrics in `detailed_description` as `<d>[Japanese] …</d>` with `(S1)`-style speaker IDs. For this pipeline the song is added in the edit, so write **`non_diegetic_music: N/A`** and keep the frame free of text.
- `detailed_description` for a generation task lands around 350–500 English words; match the described timeline length to the requested clip length (4–15 s).
- Upload order in the MD stays the same as the label order: 1. the scene still (frame anchor), 2.–3. at most two supporting plates (identity, set layout). More plates get blended.
- Keep one dialect per file. When a few clips switch to Ref2VA, keep their prompts in a separate file (e.g. `movies_ref2va.md`, or `prompt_file` entries under `clips:` in `config.yaml`) so `movies.md` stays pure I2VA.

## Stage 7 — `movies.yaml` (batch input for make_videos)

Generation tools want a flat table, not a markdown sheet. **YAML is the default**: a CSV makes editors and parsers
fight over the long prompt (commas, quotes, embedded newlines). One mapping per clip:

```yaml
- id: "01"                 # scene number, quoted so 01 is not parsed as 1
  name: <scene name>
  duration: 8              # integer seconds
  ref-image1: <file>       # upload order; empty string when the clip has fewer than three
  ref-image2: ""
  ref-image3: ""
  prompt: |-               # verbatim multi-line prompt, block scalar
    For the target video, ...
  lyrics: <matching lyric> # from the clip's 対応歌詞
```

Build it with `scripts/gen_movies_table.py <project_dir>` — it parses `movies.md` and never retypes a prompt.
`--format csv` still emits `scene-no,scene-name,duration,ref-file1..3,prompt` for a tool that demands CSV;
that variant flattens the prompt to one physical line.

- Exactly three ref slots. Error above three instead of dropping one: over-reference is the failure this table prevents.
- `prompt: |-` keeps the mandatory first line and the blank line before `integrated_multimodal_description:`.
- `id` is always quoted (`"01"`, `"E-1"`); YAML and every downstream parser must see a string.
- Write UTF-8 **without BOM** (a BOM breaks strict YAML parsers); only the CSV variant uses `utf-8-sig`.

Verify after generating: loads with `yaml.safe_load`, record count == clip count, durations sum to the song length,
every `prompt` equals its `movies.md` block verbatim, ids load as strings, unused ref slots are `""`.

### Handing off to make_videos

```
make_videos init          # once: creates config.yaml (set movies / image_dir / out_dir)
make_videos --dry-run     # check what will be generated
make_videos               # generate every clip
make_videos review --serve
```

`ref-image1` must exist in `image_dir`; the clip is saved under the same stem (`ab_01_x.png` → `videos/ab_01_x.mp4`).

## Verification (run before reporting done)

`python scripts/check_mv_assets.py <project_dir> --prefix <prefix> --song-seconds <n>` checks, without any project knowledge:

- CSV columns, unique seeds and filenames, UTF-8-sig readable
- every prompt carries `16:9`, `no text`, and (if `--ref-marker` given) the reference line
- the reference CSV is `--refs-csv <file>`, or found automatically as `<prefix>refs.csv` / the only `*refs.csv` in the project
- `movies.md`: every clip has name / seconds / reference list / prompt; reference-label mentions match the number of listed files (`--label-style auto|at|picture` handles both `<Picture N>` and `@imageN` dialects); start frame exists in `scenes.csv` (or as a ref in the refs CSV); `non_diegetic_music` present; duration total printed and compared against the song length
- `AVOID` lines are an older-dialect habit; the `h3-prompt-writing` format has no negative field, so the check is opt-in via `--require-avoid`

Also read the generated MD back and confirm one scene block by eye: block text verbatim, `CS2`/`CS1` correct for the character count, references plausible for the scene's light/season.

## Pitfalls

- **Seeds/file names must be unique across scenes and references**, otherwise batch jobs overwrite each other. Validate, don't assume.
- **Diptych scenes drift** — the seam slides and the two panels merge into one set. State "panel borders fixed" and add `panels merging` to the negative.
- **Character sheets with labels** come back as garbled text. Ask for empty margins instead of dividers.
- **Over-reference** is a real failure: 4+ plates per clip make H3 blend palettes. Two supporting plates maximum.
- **Section naming** in the MD (`Verse` / `二分割・Chorus`) must stay consistent, because the CSV and QA scripts key off it.
- **Two H3 dialects exist and must not be mixed**: `h3-prompt-writing` uses `<Picture N>` labels, `[Shot N] At MM:SS.mmm`, and camera motion written as English inside the shot; the older Hailuo 2.x style uses `@imageN` and bracket tokens. Pick one per project and say which in `movies.md` section 0.
- Simplified-Chinese characters slip into Japanese copy (歌词 → 歌詞, 画面 vs 画靣). Grep the final MD for a few known offenders.
- **`movies.yaml` ids must stay quoted** (`- id: "01"`), otherwise `01` loads as the integer 1 and the zero padding
  is lost. Keep `prompt: |-` a block scalar so the mandatory first line and the blank line before
  `integrated_multimodal_description:` survive. The `--format csv` variant must instead flatten the prompt to one
  physical line — a quoted multi-line CSV field breaks readers that split on newlines.
- **Generate the table from `movies.md` and compare verbatim** (`prompt` == block text). Hand-copying clip prompts
  into a second file is the fastest way to ship a stale prompt.
- **The asset checker scans the whole tail of `movies.md`**, so a later numbered list written as `1. `file`` counts as a
  clip's reference file. Write post-clip sections as `- **手順1**: …` bullets and the phantom refs disappear.
- **20+ scene projects: hold the blocks as variables.** An optional pattern: a small `_build_plan.py` in the project
  that owns `CH/ST/JP/CS1` and emits `plan.md`, plus a `_gen_assets.py` that parses `plan.md` into
  `scenes.md`/`scenes.csv`/`<prefix>refs.csv`. It makes verbatim drift structurally impossible. Typing a 70-word
  character block 26 times by hand is where it actually breaks. (These scripts are project-specific and not shipped.)

## Templates

Skeletons for all artifacts: [references/file-templates.md](references/file-templates.md).
