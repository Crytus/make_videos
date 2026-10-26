# make_videos — MiniMax H3 動画生成

`movies.yaml` に書かれた全クリップ（26本・計176秒）を、ローカルの ComfyUI 上の MiniMax H3 で動画にするツールです。

**流れ:** 低解像度（0.2MP）で生成 → `review.html` で見比べて採用テイクを選ぶ → `roughcut` で通しで確認 → 採用分を手動でアップスケール

## 必要なもの

- ComfyUI が起動していること（既定 `http://127.0.0.1:8188`）。MiniMax H3 のノードとモデルが入っていること
  - i2v: `minimax_h3_fl2va_pruned_int8_convrot` / `minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16`（LoRA）
  - r2v: `minimaxh3_r2v.json` で使っているモデル一式
  - 共通: `qwen3vl_32b_minimax_h3_nvfp4_awq` / `minimax_h3_video_vae_int8_convrot` / `minimax_h3_audio_vae_fp32`
- Python 3.10 以上と PyYAML（`pip install pyyaml`）
- ffmpeg / ffprobe（PATH に通す。レビューページのコマ画像とラフ版で使用）
- 開始画像（`movies.yaml` の `ref-image1`）が `output/` にあること

## コマンド一覧

```
python make_videos.py                  # 動画を生成（generate は省略可）
python make_videos.py status           # 生成状況の一覧
python make_videos.py review --serve   # 確認ページを開き、採用テイクを選ぶ
python make_videos.py roughcut         # 採用テイクをつないだラフ版を作る
```

## 1. 生成（generate）

```
python make_videos.py
```

- `movies.yaml` の全クリップを生成し、`videos/` に保存します。
  - take1 は `videos/hope_01_path_before_dawn.mp4`、2本目以降は `..._t2.mp4`、`..._t3.mp4`
  - 同じ名前の `.json` に、生成時の設定（seed・プロンプト・画像のハッシュ・解像度など）と所要時間を記録します。
- **生成済みの動画がある場合はスキップします。** 途中で止めても、もう一度実行すれば残りから続きを生成します。
- 複数テイクのときは、まず全クリップの take1 を作り、次に take2 … の順で進みます。途中で止めても、全体を一通り確認できます。
- 1本ごとに残り時間の見積もりを表示します（過去の記録と今回の実績から計算）。
- 1本が失敗しても止まらず次へ進みます。最後に失敗したファイルが表示されるので、同じコマンドを再実行してください。
- 終了後に `review.html` を自動で更新し、Windows のトースト通知（設定すれば Webhook も）でお知らせします。

### よく使う例

```
python make_videos.py --ids 05 E-1           # 指定したクリップだけ
python make_videos.py --ids 04 --takes 5     # テイクを5本に増やす（既存の分はスキップ）
python make_videos.py --ids 10 --force       # 生成済みでも作り直す
python make_videos.py --stale                # プロンプトや画像を変えたテイクだけ作り直す
python make_videos.py --dry-run              # 何が生成されるか確認（ワークフロー JSON を書き出すだけ）
```

### 設定の変更の検出（--stale）

`movies.yaml` のプロンプトや尺、開始画像の中身、解像度・モデルなどを変えると、その設定で作った動画は「設定変更あり」になります。通常の実行ではスキップされ、次のように表示されます。

```
設定が変わったテイクが 1本あります（--stale で再生成）:
  hope_07_holding_the_dream.mp4: プロンプトが変更
```

`--stale` を付けると、これらだけを作り直します。記録（.json）が無い動画（このツール以前に作ったもの）は対象外です。

### オプション

| オプション | 説明 |
|---|---|
| `--ids ID ...` | 対象クリップ（`01`〜`25`, `E-1`）。省略時は全件 |
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
| `--config` | 設定ファイル（既定 `config.yaml`） |

コマンドラインで指定した値は、`config.yaml` の値より優先されます。

## 2. 生成状況の確認（status）

```
python make_videos.py status
```

```
 04 胸に秘めた光  t1○★ t2○ t3△  [i2v, 上書き: takes]  変更: t3: プロンプト
```

`○` 最新 / `△` 設定変更あり / `?` 記録なし / `-` 未生成 / `★` 採用テイク

## 3. 見比べて採用テイクを選ぶ（review）

```
python make_videos.py review --serve
```

ブラウザで `review.html` が開きます。クリップごとに、開始画像・各テイクの動画・最初/中間/最後のコマ・歌詞・seed・状態が並びます。採用するテイクのラジオボタンを選び、**「選択を保存」** を押すと `videos/selected.yaml` に保存されます。「未選択のみ表示」で、まだ選んでいないクリップだけに絞り込めます。終了は Ctrl+C です。

`review.html` を直接開いた場合（`--serve` なし）は直接保存できないため、`selected.yaml` がダウンロードされます。それを `videos/` に置いてください。

`selected.yaml` の形式（手で編集しても構いません）:

```yaml
"01": hope_01_path_before_dawn.mp4
"04": hope_04_light_in_hands_t2.mp4
```

## 4. ラフ版（roughcut）

```
python make_videos.py roughcut
python make_videos.py roughcut --audio song.wav   # 歌を重ねる
```

全クリップを `movies.yaml` の尺どおりに切りそろえ（H3 の都合で少し長く生成される分を切る）、順番につないで `videos/roughcut.mp4`（176秒）を作ります。

- 各クリップに使うテイク: `selected.yaml` の採用テイク → take1 → 残っているテイク
- 未生成のクリップは黒画面で埋めます
- 音声は既定では生成された音声をつなぎます。`--audio`（または `config.yaml` の `roughcut.audio`）で歌の音源に差し替えられます

## 設定ファイル（config.yaml）

共通の設定と、クリップごとの上書きを書きます。省略した項目は既定値になります。優先順位は **コマンドライン > `clips.<id>` > `generation` > 既定値** です。

```yaml
generation:
  mode: i2v
  megapixels: 0.2
  takes: 1

notify:
  toast: true
  webhook: null      # Discord / Slack 互換の Webhook URL

clips:
  "04": {takes: 3}   # 手のカットは多めに引く
  "10":              # 顔が崩れたカットを Ref2VA で撮り直す
    mode: r2v
    ref-images: [hope_10_a_tear.png, hope_ref_02_character-sheet.png, hope_ref_01_location-path-dawn.png]
    prompt_file: prompts/10_ref2va.txt
```

`clips.<id>` に書けるキー: `mode` / `ref-images` / `prompt` / `prompt_file` / `seed` / `steps` / `megapixels` / `turbo` / `takes`

- **id は必ずクォートしてください**（`"04"`）。クォートし忘れても `4` → `"04"` に補正しますが、`E-1` などとの混在を避けるためです。
- r2v に切り替えるクリップは、`movies.yaml` の I2VA 形式のプロンプトではなく、Ref2VA の6節形式のプロンプトを `prompt_file` で渡すのが基本です（`movies.md` §0）。
- 全項目と説明は `config.yaml` のコメントを参照してください。

## 生成方式

- **i2v（既定）**: `ref-image1` を動画の1フレーム目にします。ComfyUI 公式テンプレート `video_minimax_h3_i2v` と同じ構成です。`movies.yaml` のプロンプト（I2VA 形式）と合っているのはこちらです。
- **r2v**: `minimaxh3_r2v.json` を土台にして、参照画像（最大3枚）を渡します。1フレーム目が静止画と一致するとは限りません。

## 動画の長さ

`duration`（秒）を 24fps のフレーム数に変換し、H3 の制約（17k+5 フレーム）に合わせて切り上げます。8秒 = 192フレーム、10秒 = 243フレーム（約10.1秒）です。端数は `roughcut` や編集で切ってください。

## テスト

```
python -m unittest -v
```

ComfyUI を起動していなくても実行できます（ffmpeg が無い環境では一部をスキップします）。
