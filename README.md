# make_videos — MiniMax H3 で MV のクリップを一括生成

楽曲の歌詞から MV のクリップを作るためのツール一式です。

| 構成 | 役割 |
|---|---|
| `make_videos`（Python ツール） | クリップの一覧表 `movies.yaml` をもとに、ローカルの ComfyUI 上の MiniMax H3 で各クリップの動画を一括生成する |
| `skills/music-video-production`（エージェント用スキル） | 歌詞から絵コンテ・画像プロンプト・動画プロンプトを作り、`movies.yaml` まで仕上げる手順とスクリプト |

**全体の流れ:**

1. **スキル**で、歌詞から `plan.md` → `scenes.csv`（画像プロンプト）→ `movies.md` → `movies.yaml` を作る
2. `scenes.csv` をもとに、generate_image（別リポジトリにあり）で各シーンの開始画像を作る、hope_refs.csv（参照画像用）も同様につくる
3. **make_videos** で、低解像度（0.2MP）でまとめて動画を生成する
4. `review.html` で見比べて採用テイクを選び、`roughcut` で通しで確認する
5. 採用したクリップを手動でアップスケールし、動画編集ソフトで楽曲と字幕（必要なら）を載せる（[videomaker](https://github.com/Crytus/videomaker) を使う場合は、`make_videos videomaker` でシナリオ YAML を書き出せる）

## セットアップ

### 1. ComfyUI と MiniMax H3 のモデル

1. ComfyUI を MiniMax H3 対応版に更新します（ノード一覧に `MiniMaxH3ImageToVideo` / `MiniMaxH3ReferenceToVideo` があれば対応しています）。
2. モデルを Hugging Face の [Comfy-Org/MiniMax-H3](https://huggingface.co/Comfy-Org/MiniMax-H3) から入手し、ComfyUI の `models/` 以下に置きます。

| 種類 | 置き場所 | i2v（既定） | r2v |
|---|---|---|---|
| 拡散モデル | `models/diffusion_models/` | `minimax_h3_fl2va_pruned_int8_convrot` | `minimax_h3_ref2va_pruned_int8_convrot` |
| turbo LoRA | `models/loras/` | `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16` | `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16` |
| テキストエンコーダー | `models/text_encoders/` | `qwen3vl_32b_minimax_h3_nvfp4_awq` | 同左 |
| 動画 VAE | `models/vae/` | `minimax_h3_video_vae_int8_convrot` | `minimax_h3_video_vae_fp16` |
| 音声 VAE | `models/vae/` | `minimax_h3_audio_vae_fp32` | 同左 |

（拡張子はいずれも `.safetensors`）

3. ComfyUI を起動します（既定 `http://127.0.0.1:8188`）。ブラウザでテンプレート「MiniMax H3: Image to Video」が動けば準備完了です。

別の量子化版など、ファイル名が違うモデルを使う場合は `config_video.yaml` の `i2v:` で指定します。r2v は `r2v.template` に自分のワークフローを指定します。

### 2. ffmpeg

レビューページのコマ画像とラフ版で使います。`ffmpeg` と `ffprobe` に PATH を通してください。

```
winget install ffmpeg          # Windows
brew install ffmpeg            # macOS
sudo apt install ffmpeg        # Ubuntu など
```

### 3. make_videos（Python 3.10 以上）

```
pip install git+https://github.com/Crytus/make_videos.git
```

リポジトリを clone して手元で変更しながら使う場合:

```
git clone https://github.com/Crytus/make_videos.git
cd make_videos
pip install -e .
```

インストールすると `make_videos` コマンドが使えるようになります。インストールせずに、リポジトリ直下で `python make_videos.py …` としても同じように動きます。

### 4. スキル（歌詞から movies.yaml を作る場合）

`skills/music-video-production` フォルダを、使っている AI エージェントのスキル置き場にコピーします。

**Claude Code** の場合:

| 使う範囲 | 置き場所 |
|---|---|
| すべてのプロジェクト | `~/.claude/skills/music-video-production/` |
| 特定のプロジェクトだけ | `<プロジェクト>/.claude/skills/music-video-production/` |

```
# Windows（PowerShell）
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse skills\music-video-production "$HOME\.claude\skills\"

# macOS / Linux
mkdir -p ~/.claude/skills && cp -r skills/music-video-production ~/.claude/skills/
```

**その他のエージェント**（`SKILL.md` 形式のスキルに対応しているもの）は、そのエージェントのスキル置き場（例: `~/.agents/skills/`）にコピーします。

**推奨:** MiniMax H3 のプロンプト形式を定義した別スキル `h3-prompt-writing` も、同じスキル置き場に入れてください。無い場合は、`SKILL.md` に書かれた形式の要約で代用します。

入れたら、エージェントに次のように頼みます。

```
music-video-production スキルで、lyrics.txt の歌詞から MV の計画と movies.yaml を作って
```

スキルに同梱のスクリプトは単体でも使えます。

```
python skills/music-video-production/scripts/gen_movies_table.py <プロジェクト>              # movies.md → movies.yaml
python skills/music-video-production/scripts/check_mv_assets.py <プロジェクト> --prefix ab_ --song-seconds 176   # 成果物の検査
```

### 5. プロジェクトの作成

作業用のディレクトリを作り、設定ファイルの雛形を作ります。

```
mkdir my_mv
cd my_mv
make_videos init
```

`config_video.yaml` を開き、少なくとも次を確認します。

| 項目 | 内容 |
|---|---|
| `server` | ComfyUI の URL（別の PC や別ポートで動かしている場合に変更） |
| `movies` / `image_dir` / `out_dir` | 一覧表・開始画像・生成結果の場所 |
| `generation.megapixels` | 解像度（既定 0.2 = 608×352。確認用） |
| `notify.webhook` | 完了を Discord / Slack に送る場合の Webhook URL |

ディレクトリは次のようになります。

```
my_mv/
├─ config_video.yaml  # make_videos init で作成
├─ movies.yaml        # クリップの一覧表（スキルで作成、または手で書く）
├─ images/            # 各クリップの開始画像
└─ videos/            # 生成結果（自動で作成）
```

準備ができたら生成します。

```
make_videos --dry-run    # まず何が生成されるかを確認（ComfyUI には投入しない）
make_videos              # 生成
```

`make_videos` はカレントディレクトリの `config_video.yaml` を読みます。別の場所の設定を使うときは `--config path/to/config_video.yaml` を付けます。

## movies.yaml の書き方

クリップを編集順に並べたリストです。

```yaml
- id: "01"                      # クリップ id（文字列。"E-1" なども可）
  name: オープニング             # 表示名
  duration: 8                   # 秒数（4〜15秒）
  ref-image1: clip_01_opening.png   # 開始画像（images/ 内のファイル名）。出力ファイル名にもなる
  ref-image2: ""                # r2v 用の追加の参照画像（任意）
  ref-image3: ""
  prompt: |-                    # MiniMax H3 のプロンプト
    For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

    integrated_multimodal_description: [Shot 1] ...

    overall_soundscape: ...

    non_diegetic_music: N/A
  lyrics: 歌詞の一節            # レビューページに表示（任意）
```

- 必須キーは `id` / `duration` / `ref-image1` / `prompt` です。
- 動画は `ref-image1` の名前で保存されます（`clip_01_opening.png` → `videos/clip_01_opening.mp4`）。

## コマンド一覧

```
make_videos init             # config_video.yaml の雛形を作る
make_videos                  # 動画を生成（generate は省略可）
make_videos status           # 生成状況の一覧
make_videos review --serve   # 確認ページを開き、採用テイクを選ぶ
make_videos roughcut         # 採用テイクをつないだラフ版を作る
make_videos videomaker       # 採用テイクをつなぐ videomaker のシナリオ YAML を書き出す
```

各コマンドのオプションは `make_videos <コマンド> --help` で確認できます。

## 1. 生成（generate）

```
make_videos
```

- `movies.yaml` の全クリップを生成し、`videos/` に保存します。
  - take1 は `clip_01_opening.mp4`、2本目以降は `clip_01_opening_t2.mp4`、`_t3.mp4` …
  - 同じ名前の `.json` に、生成時の設定（seed・プロンプト・画像のハッシュ・解像度など）と所要時間を記録します。
- **生成済みの動画がある場合はスキップします。** 途中で止めても、もう一度実行すれば残りから続きを生成します。
- 複数テイクのときは、まず全クリップの take1 を作り、次に take2 … の順で進みます。途中で止めても、全体を一通り確認できます。
- 1本ごとに残り時間の見積もりを表示します（過去の記録と今回の実績から計算）。
- 1本が失敗しても止まらず次へ進みます。最後に失敗したファイルが表示されるので、同じコマンドを再実行してください。
- 動画が1本できるごとに `review.html` を自動で更新します（`config_video.yaml` の `review.auto` で `end`＝最後に1回 / `off`＝しない に変更可）。
- 終了すると Windows のトースト通知（設定すれば Webhook も）でお知らせします。

### よく使う例

```
make_videos --ids 05 E-1           # 指定したクリップだけ
make_videos --ids 04 --takes 5     # テイクを5本に増やす（既存の分はスキップ）
make_videos --ids 10 --force       # 生成済みでも作り直す
make_videos --stale                # プロンプトや画像を変えたテイクだけ作り直す
make_videos --dry-run              # 何が生成されるか確認（ワークフロー JSON を書き出すだけ）
```

### 設定の変更の検出（--stale）

`movies.yaml` のプロンプトや尺、開始画像の中身、解像度・モデルなどを変えると、その設定で作った動画は「設定変更あり」になります。通常の実行ではスキップされ、次のように表示されます。

```
設定が変わったテイクが 1本あります（--stale で再生成）:
  clip_07_bud.mp4: プロンプトが変更
```

`--stale` を付けると、これらだけを作り直します。記録（.json）が無い動画（このツール以外で作ったもの）は対象外です。

### オプション

| オプション | 説明 |
|---|---|
| `--ids ID ...` | 対象クリップの id。省略時は全件 |
| `--takes N` | 1クリップあたりのテイク数 |
| `--force` | 生成済みでも作り直す |
| `--stale` | 設定が変わったテイクを作り直す |
| `--mode {i2v,r2v}` | 生成方式 |
| `--megapixels` | 解像度（16:9 で 0.2 = 608×352） |
| `--steps` | サンプリングステップ数 |
| `--turbo` / `--no-turbo` | i2v で turbo LoRA を使う / 使わない（8 / 20 steps） |
| `--seed` | take1 の seed（全クリップ共通） |
| `--seed-base` | 自動 seed の基準値 |
| `--dry-run` | キュー投入せず、ワークフロー JSON を `videos/workflows/` に書き出す |
| `--no-review` / `--no-notify` | レビューページの自動更新・終了時の通知をしない |
| `--server` | ComfyUI の URL |
| `--config` | 設定ファイル（既定はカレントディレクトリの `config_video.yaml`） |

コマンドラインで指定した値は、`config_video.yaml` の値より優先されます。

## 2. 生成状況の確認（status）

```
make_videos status
```

```
 04 手のひら  t1○★ t2○ t3△  [i2v, 上書き: takes]  変更: t3: プロンプト
```

`○` 最新 / `△` 設定変更あり / `?` 記録なし / `-` 未生成 / `★` 採用テイク

## 3. 見比べて採用テイクを選ぶ（review）

```
make_videos review --serve
```

ブラウザで `review.html` が開きます。クリップごとに、開始画像・各テイクの動画・最初/中間/最後のコマ・歌詞・seed・状態が並びます。採用するテイクのラジオボタンを選び、**「選択を保存」** を押すと `videos/selected.yaml` に保存されます。同時に videomaker のシナリオ `videos/videomaker.yaml` も作り直します（[5. videomaker](#5-videomaker-用のシナリオvideomaker) 参照。`videomaker.auto: false` で止められます）。「未選択のみ表示」で、まだ選んでいないクリップだけに絞り込めます。終了は Ctrl+C です。

`--serve` で開いている間に生成が進んで `review.html` が更新されると、画面上部に「新しいクリップがあります」と表示されます。未保存の選択が消えないよう自動では再読み込みしないので、必要なら「選択を保存」してから「再読み込み」を押してください。

`review.html` を直接開いた場合（`--serve` なし）は直接保存できないため、`selected.yaml` がダウンロードされます。それを `videos/` に置いてください。

`selected.yaml` の形式（手で編集しても構いません）:

```yaml
"01": clip_01_opening.mp4
"04": clip_04_hands_t2.mp4
```

## 4. ラフ版（roughcut）

```
make_videos roughcut
make_videos roughcut --audio song.wav   # 楽曲を重ねる
```

全クリップを `movies.yaml` の尺どおりに切りそろえ（H3 の都合で少し長く生成される分を切る）、順番につないで `videos/roughcut.mp4` を作ります。

- 各クリップに使うテイク: `selected.yaml` の採用テイク → take1 → 残っているテイク
- 未生成のクリップは黒画面で埋めます
- 音声は既定では生成された音声をつなぎます。`--audio`（または `config_video.yaml` の `roughcut.audio`）で楽曲の音源に差し替えられます

## 5. videomaker 用のシナリオ（videomaker）

```
make_videos videomaker
make_videos videomaker --output mv.yaml   # 出力先を変える
```

[videomaker](https://github.com/Crytus/videomaker) で採用テイクをつなぎ、楽曲・歌詞の字幕を載せるためのシナリオ `videos/videomaker.yaml` を書き出します。`videomaker render videos/videomaker.yaml` でそのまま書き出せます。

```yaml
video:
  width: 1920
  height: 1080
  fps: 24
  bgm_volume: 1.0
  bgm_loop: false
  bgm: ../song.wav
scenes:
  - id: '01'
    video: clip_01_opening.mp4
    duration: 8
    subtitle: ''
  - id: '04'
    video: clip_04_hands_t2.mp4
    duration: 6
    subtitle: 胸に秘めた光
```

- 各シーンに使うテイクは `roughcut` と同じです（`selected.yaml` の採用テイク → take1 → 残っているテイク）。未生成のクリップは開始画像（静止画）で埋めます
- 各シーンに `movies.yaml` の `duration` を書きます。H3 で少し長く生成された分は videomaker が尺どおりに切ります
- 字幕は `movies.yaml` の `lyrics` です。「（イントロ／歌唱なし）」のように全体が括弧書きのものは空にします（`videomaker.subtitle: none` で字幕なし）
- パスは書き出した YAML からの相対パスです（ドライブが違う場合は絶対パス）
- `video:` / `options:` は `config_video.yaml` の `videomaker.video` / `videomaker.options` をそのまま写します。`bgm` を省略すると `roughcut.audio` を使います。`bgm` と `subtitle.font` は、`config_video.yaml` 基準で実在すれば YAML 基準の相対パスに直し、実在しなければそのまま書きます（videomaker 側の `assets/` 検索に任せる）
- 書き出すたびに上書きするので、共通の設定は YAML ではなく `config_video.yaml` に書いてください

```yaml
# config_video.yaml
videomaker:
  subtitle: lyrics
  video:
    fps: 30
    subtitle:
      font: assets/fonts/msgothic.ttc
      position: bottom
      style: {fill: "#FFFFFF", stroke: "#000000", padding: 32}
  options:
    no_voice: true
```

## 設定ファイル（config_video.yaml）

共通の設定と、クリップごとの上書きを書きます。省略した項目は既定値になります。優先順位は **コマンドライン > `clips.<id>` > `generation` > 既定値** です。全項目と説明は `make_videos init` で作られる雛形のコメントを参照してください。

```yaml
movies: movies.yaml
image_dir: images
out_dir: videos

generation:
  mode: i2v
  megapixels: 0.2
  takes: 1

notify:
  toast: true
  webhook: null      # Discord / Slack 互換の Webhook URL

clips:
  "04": {takes: 3}   # 崩れやすいカットは多めに引く
  "10":              # 1クリップだけ r2v（参照画像）で生成する
    mode: r2v
    ref-images: [clip_10_start.png, character_sheet.png, location.png]
    prompt_file: prompts/10_r2v.txt
```

`clips.<id>` に書けるキー: `mode` / `ref-images` / `prompt` / `prompt_file` / `seed` / `steps` / `megapixels` / `turbo` / `takes`

- **id は必ずクォートしてください**（`"04"`）。クォートし忘れても `4` → `"04"` に補正します。
- r2v に切り替えるクリップは、I2VA 形式のプロンプトではなく Ref2VA 形式（`subject_definitions` / `summary` / `retention_analysis` / `detailed_description` / `overall_soundscape` / `non_diegetic_music`）のプロンプトを `prompt_file` で渡すのが基本です。

## 生成方式

- **i2v（既定）**: `ref-image1` を動画の1フレーム目にします。ComfyUI 公式テンプレート `video_minimax_h3_i2v` と同じ構成です。I2VA 形式のプロンプト（1行目が `For the target video, at 0.00 seconds …`）を使います。
- **r2v**: 参照画像（最大3枚）を渡して生成します。ワークフローは同梱のテンプレート（`mvgen/templates/minimaxh3_r2v.json`）を使います。自分のワークフローを使う場合は `config_video.yaml` の `r2v.template` に API 形式で書き出した JSON を指定します（ノード ID は同梱テンプレートと同じである必要があります）。1フレーム目が開始画像と一致するとは限りません。

## 動画の長さ

`duration`（秒）を 24fps のフレーム数に変換し、H3 の制約（17k+5 フレーム）に合わせて切り上げます。8秒 = 192フレーム、10秒 = 243フレーム（約10.1秒）です。端数は `roughcut`・`videomaker` や編集で切ってください。

## サンプル

リポジトリ直下の `movies.yaml` / `config_video.yaml` / `plan.md` / `movies.md` / `scenes.*` などは、サンプル楽曲1曲分の制作データです。開始画像（`output/`）はリポジトリに含めていないため、そのままでは生成できません。自分の作品では `make_videos init` から始めてください。

## テスト

リポジトリ直下で実行します。ComfyUI を起動していなくても動きます（ffmpeg が無い環境では一部をスキップします）。

```
python -m unittest -v
```

## ライセンス

MIT（[LICENSE](LICENSE)）
なお`h3-prompt-writing`スキルは同梱していません
