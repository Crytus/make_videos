# Artifact templates

Copy the skeletons, replace `<…>`. Keep the headings — the CSV/QA scripts and the next session both key off them.

## plan.md

```markdown
# ミュージックビデオ絵コンテ計画「<title>」

楽曲: <title>（自作詞）/ シーン数: <N>（Scene 01–NN ＋ 固定 E-1）/ アスペクト比: 16:9 / 生成モデル: Qwen Image 2.1 / スタイル: <style>

## 1. 全体のビジュアル・コンセプト
- 舞台 / 色 / 物語の弧 / 描き分けの軸 / カメラ / 文字ゼロ方針

## 2. キャラクター設定（一貫性ブロック・英語固定文）
### <ID> — <name>（固定ブロック。CH1 / CH2 …）
> <verbatim English character block>
### ST — スタイル固定ブロック
> <style block>
### JP — 世界観固定ブロック（国・土地）
> <world block>            ※ 例外（季節違いなど）は JP-A として明記
### 一貫性宣言文
- 二匹/二人: `the same two characters as in every scene, identical faces, identical outfits, identical colors`
- 単独: `the same character as in every scene, identical face, identical outfit, identical colors`
### ネガティブプロンプト共有ベース
> <base negative>

## 3. シーン ↔ 歌詞 対応表
| # | シーン名 | 曲構成 | 対応歌詞 | 尺目安 |

## 4. シーン詳細
### Scene 01 — <name>（<section>）
- **歌詞**: …
- **内容**: …
- **カメラ/光**: …
- **positive_prompt**:
  `…, <JP>, <ST>, <CS>, 16:9, no text`
- **negative_prompt**: 共有ベース ＋ `…`
- **seed**: 1000 / **file_name**: `<prefix>01_<desc>.png`（例: `ab_01_opening.png`）

## 5. シーンの流れ（編集メモ）
| 区間 | シーン | 編集の意図 |

## 6. <image model> 実行メモ
（ワークフロー、解像度、ステップ/CFG、seed 運用、生成順、CSV の単一ソース原則）

## 7. 参照画像（リファレンス）プロンプト
### REF-01 — <character> キャラクターシート
- **用途** / **作画の要点** / **positive_prompt** / **negative_prompt** / **seed** / **file_name**

## 8. 参照画像の運用（シーン別マッピング）
| シーン | 参照する基準画像 | 一致させる要素 |
追記ルール（5点）: CH verbatim ・ JP ・ CS2/CS1 ・ references: 行 ・ 16:9, no text
```

## scenes.md

```markdown
# <title> — シーン表（画像生成用）

## 0. 使い方           ← 基準画像→参照入力→シーン生成 の順序、生成順、CSV の扱い
## 1. 固定ブロック       ← plan.md と同一文（変更禁止）
## 2. 参照画像一覧       ← | ID | file_name | 用途 |
## 3. シーン一覧         ← | # | シーン名 | 曲構成 | 対応歌詞 | seed | file_name |
## 4. シーン詳細
### Scene 01 — <name>
- **シーン名** / **曲構成** / **対応歌詞** / **シーン説明** / **カメラ・光** /
  **参照画像**: REF-01（`file`）, REF-04（`file`） / **seed** / **file_name** /
  **positive_prompt** / **negative_prompt**
## 5. 検収チェックリスト
```

## scenes.csv / <prefix>refs.csv

```csv
scene_num,scene_name,seed,file_name,positive_prompt
01,<name>,1000,<prefix>01_<desc>.png,"<single-line prompt>, references: reference sheets <ref>, 16:9, no text"
```

The reference list uses the same columns (`REF-01,…,4000,<prefix>ref_01_<desc>.png,…`) and is named `<prefix>refs.csv`.

- UTF-8 **with BOM** (`encoding="utf-8-sig"`), `csv.QUOTE_MINIMAL`, prompt whitespace collapsed to one line.
- Generate by parsing `plan.md`; never hand-edit.

## movies.md

Written in the `h3-prompt-writing` dialect. Stills only → **I2VA**; stills + reference plates → **Ref2VA**.

```markdown
# <title> — 動画生成シナリオ（MiniMax H3 / <mode>）

## 0. モデル仕様とプロンプト規約   ← 採用モード(I2VA/Ref2VA)・尺の範囲・解像度・参照上限／固定ルール
## 1. 尺表
| # | シーン名 | 秒数 | 累積 | 開始画像（Picture 1） | 補助参照 |
## 2. シーン別プロンプト
### Scene 01 — <name>
- **シーン名** / **秒数** / **対応歌詞**（＋曲構成）
- **参照画像ファイル名（アップロード順）**:
  1. `<still>.png` — Picture 1 / 開始フレーム
  2. `<ref>.png` — Picture 2 / 場所参照
- **プロンプト**:
```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] <style>, matching <Picture 1>: a medium-wide shot of <setting> in the same layout as <Picture 2>. <…first-frame anchor → action onset → development → reaction, about 350–500 words for a generation task…>. The camera pushes in with small amplitude at slow speed toward <subject>, then holds a static shot.

overall_soundscape: <ambience and physical sounds only>.

non_diegetic_music: N/A
```
- **編集メモ**
## 3. 生成と検収の手順
## 4. 出典
```

Ref2VA variant: replace the instruction line and body with the six sections
`subject_definitions` / `summary` / `retention_analysis` / `detailed_description` / `overall_soundscape` / `non_diegetic_music`,
giving each reference plate its own `<Subject N>` line and using `<Picture N>` only for frame anchors.

## movies.yaml

```yaml
- id: "01"
  name: <scene name>
  duration: 8
  ref-image1: <prefix>01_<desc>.png
  ref-image2: ""
  ref-image3: ""
  prompt: |-
    For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

    integrated_multimodal_description: [Shot 1] …

    overall_soundscape: …

    non_diegetic_music: N/A
  lyrics: <matching lyric>
```

- Generate with `scripts/gen_movies_table.py <project_dir>` from `movies.md`; never hand-copy prompts.
- This is the input of `make_videos` (see the repository README).
- `id` quoted (keeps `01` a string), `duration` an integer, unused ref slots `""`, max 3 refs.
- `prompt: |-` is the verbatim multi-line form; UTF-8 without BOM.
- `--format csv` produces the flat `scene-no,scene-name,duration,ref-file1..3,prompt` table (prompt flattened, UTF-8-sig).

Do not mix in the older Hailuo 2.x dialect (`@image1` keyframe wording + bracket camera commands such as `[Push in]`). When `h3-prompt-writing` is not installed, follow the format summary in SKILL.md Stage 6.
