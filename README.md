# make_videos — MiniMax H3 で MV のクリップを一括生成

クリップの一覧表（`movies.yaml`）をもとに、ローカルの ComfyUI 上の MiniMax H3 で各クリップの動画を生成するツールです。

**作業の流れ:**
1. 低解像度（0.2MP）でまとめて生成する
2. `review.html` で見比べて採用テイクを選ぶ
3. `roughcut` で通しで確認する
4. 採用したクリップを手動でアップスケールする

## インストール

Python 3.10 以上が必要です。

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

### ほかに必要なもの

- **ComfyUI**（既定 `http://127.0.0.1:8188`）と MiniMax H3 のノード・モデル
  - i2v: `minimax_h3_fl2va_pruned_int8_convrot` / `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16`（LoRA）/ `minimax_h3_video_vae_int8_convrot`
  - r2v: `minimax_h3_ref2va_pruned_int8_convrot` / `minimax_h3_ref2v_turbo_4step_v0.1_comfyui_bf16`（LoRA）/ `minimax_h3_video_vae_fp16`
  - 共通: `qwen3vl_32b_minimax_h3_nvfp4_awq` / `minimax_h3_audio_vae_fp32`
- **ffmpeg / ffprobe**（PATH に通す。レビューページのコマ画像とラフ版で使用）

## はじめかた

作業用のディレクトリを作り、設定ファイルの雛形を作ります。

```
mkdir my_mv
cd my_mv
make_videos init
```

次のように用意します（名前は `config.yaml` で変えられます）。

```
my_mv/
├─ config.yaml     # make_videos init で作成
├─ movies.yaml     # クリップの一覧表（下記）
├─ images/         # 各クリップの開始画像
└─ videos/         # 生成結果（自動で作成）
```

準備ができたら生成します。

```
make_videos --dry-run    # まず何が生成されるかを確認（ComfyUI には投入しない）
make_videos              # 生成
```

`make_videos` はカレントディレクトリの `config.yaml` を読みます。別の場所の設定を使うときは `--config path/to/config.yaml` を付けます。

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
make_videos init             # config.yaml の雛形を作る
make_videos                  # 動画を生成（generate は省略可）
make_videos status           # 生成状況の一覧
make_videos review --serve   # 確認ページを開き、採用テイクを選ぶ
make_videos roughcut         # 採用テイクをつないだラフ版を作る
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
- 終了後に `review.html` を自動で更新し、Windows のトースト通知（設定すれば Webhook も）でお知らせします。

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
| `--no-review` / `--no-notify` | 終了後のレビュー更新・通知をしない |
| `--server` | ComfyUI の URL |
| `--config` | 設定ファイル（既定はカレントディレクトリの `config.yaml`） |

コマンドラインで指定した値は、`config.yaml` の値より優先されます。

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

ブラウザで `review.html` が開きます。クリップごとに、開始画像・各テイクの動画・最初/中間/最後のコマ・歌詞・seed・状態が並びます。採用するテイクのラジオボタンを選び、**「選択を保存」** を押すと `videos/selected.yaml` に保存されます。「未選択のみ表示」で、まだ選んでいないクリップだけに絞り込めます。終了は Ctrl+C です。

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
- 音声は既定では生成された音声をつなぎます。`--audio`（または `config.yaml` の `roughcut.audio`）で楽曲の音源に差し替えられます

## 設定ファイル（config.yaml）

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
- **r2v**: 参照画像（最大3枚）を渡して生成します。ワークフローは同梱のテンプレート（`mvgen/templates/minimaxh3_r2v.json`）を使います。自分のワークフローを使う場合は `config.yaml` の `r2v.template` に API 形式で書き出した JSON を指定します（ノード ID は同梱テンプレートと同じである必要があります）。1フレーム目が開始画像と一致するとは限りません。

## 動画の長さ

`duration`（秒）を 24fps のフレーム数に変換し、H3 の制約（17k+5 フレーム）に合わせて切り上げます。8秒 = 192フレーム、10秒 = 243フレーム（約10.1秒）です。端数は `roughcut` や編集で切ってください。

## サンプル

リポジトリ直下の `movies.yaml` / `config.yaml` / `plan.md` / `movies.md` / `scenes.*` などは、サンプル楽曲1曲分の制作データです。開始画像（`output/`）はリポジトリに含めていないため、そのままでは生成できません。自分の作品では `make_videos init` から始めてください。

## テスト

リポジトリ直下で実行します。ComfyUI を起動していなくても動きます（ffmpeg が無い環境では一部をスキップします）。

```
python -m unittest -v
```
