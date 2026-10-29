# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

MiniMax H3（ローカル ComfyUI）で MV のクリップを一括生成するツール `make_videos`（`mvgen/` パッケージ。`pip install` で `make_videos` コマンドになる）、歌詞から `movies.yaml` までを作るエージェント用スキル `skills/music-video-production/`、その動作確認に使っているサンプル楽曲1曲分の制作データで構成される。ライセンスは MIT。GitHub: https://github.com/Crytus/make_videos （公開リポジトリ）。

- **サンプル楽曲の曲名を README・コメント・設定の説明・コミットメッセージなどに書かない。** ツールは汎用。例には `clip_01_opening.png` のような汎用名を使う。
- `videos/`（生成物）と `output/`（サンプルの画像 52MB）は .gitignore で管理外。
- 公開リポジトリなので、個人環境の絶対パス（ユーザーのホームや作業ドライブ）や特定エージェント専用のツール名をスキル・README・CLAUDE.md に書かない。`h3-prompt-writing` スキルはライセンス不明のため同梱しない（スキル内では探索順で参照する）。

## スキル（skills/music-video-production/）

- `SKILL.md`（手順）、`references/file-templates.md`（成果物の雛形）、`scripts/gen_movies_table.py`（movies.md → movies.yaml）、`scripts/check_mv_assets.py`（成果物の検査。参照 CSV は `--refs-csv` / `<prefix>refs.csv` / 唯一の `*refs.csv` の順に探す）。
- スクリプトは依存なし（標準ライブラリのみ）。`tests/test_skill_scripts.py` がサンプルデータで「検査が通る」「movies.yaml がバイト単位で再現される」ことを確認する。movies.yaml の書式を変えるときは `gen_movies_table.py` と make_videos（`mvgen/movies.py`）の両方を合わせる。

## ツール（make_videos / mvgen/）

利用者向けの使い方は `README.md`。オプションや設定を変えたら README と `mvgen/templates/config_video.yaml`（`make_videos init` の雛形）のコメントも更新する。依存は PyYAML と ffmpeg/ffprobe（HTTP は標準ライブラリ）。

```
pip install -e .                                 # make_videos コマンドを入れる（インストールせず python make_videos.py でも同じ）
make_videos init                                 # カレントディレクトリに config_video.yaml の雛形
make_videos [generate] --dry-run                 # 生成対象の確認（API 形式ワークフローを videos/workflows/ に書き出す）
make_videos status                               # 生成状況（○最新 △設定変更あり ?記録なし -未生成）
make_videos review --serve                       # review.html を開き、採用テイクを videos/selected.yaml に保存
make_videos roughcut                             # 採用テイクを尺どおりに切ってつないだ videos/roughcut.mp4
make_videos videomaker                           # 採用テイクをつなぐ videomaker のシナリオ videos/videomaker.yaml
python -m unittest -v                            # 全テスト（ComfyUI 不要。リポジトリ直下で実行）
python -m unittest tests.test_generate.TestGenerate.test_takes   # 1件だけ
```

### 構成とデータの流れ

- 設定ファイルは既定で**カレントディレクトリ**の `config_video.yaml`（`--config` で変更）。相対パスは config_video.yaml のディレクトリ基準。`mvgen/config.py` の `DEFAULTS` とマージし、優先順位は **CLI > `clips.<id>` > `generation` > DEFAULTS**。クリップ単位の解決は `plan.resolve_clip()` が一手に担う。
- リポジトリ直下の `config_video.yaml` はサンプル用（`image_dir: output`、`upload_subfolder: hope` など）。汎用の既定値は `DEFAULTS` と `mvgen/templates/config_video.yaml` 側。
- `plan.build_jobs()` がクリップ × テイクのジョブを「テイク番号 → クリップ順」で作る。保存先は take1 = `<開始画像名>.mp4`、take k = `<開始画像名>_t<k>.mp4`、seed は take1 + (k-1)*1000。
- 生成後、動画と同名の `.json` に `metadata.generation_params()`（プロンプト・尺・seed・解像度・ステップ数・画像の sha256・モデル）を記録する。現在の設定と比べて差があれば STALE（`--stale` で再生成）。**見た目に影響する設定を追加したら `generation_params()` にも入れる**こと。記録の無い動画は UNKNOWN で、自動では作り直さない。
- 生成済み（空でない mp4）はスキップ。ダウンロードや記録は `.part` に書いてから置き換える（中断で壊れたファイルを生成済みと誤認しないため）。
- `review.py` は `videos/review.html` と `review_frames/`（ffmpeg で切り出したコマ）を作る。generate 中は `review.auto`（each / end / off、既定 each）に従い1本ごとに作り直す。ページ側は `--serve` 時に HEAD の Last-Modified を15秒ごとに見て更新バナーを出す（自動リロードはしない）。`--serve` は 127.0.0.1 限定の http.server で、`POST …/api/selection` を `selection.save_selection()` に渡す（ファイル名だけを受け付け、実在を確認する）。
- `roughcut.py` は selected.yaml → take1 → 残りのテイクの順に使う動画を選び、ffmpeg の filter_complex で尺どおりに切って concat する。未生成は黒。
- `videomaker.py` は roughcut と同じ `plan_cues()` で動画を選び、videomaker（https://github.com/Crytus/videomaker）のシナリオを書き出す。各シーンに movies.yaml の尺を `duration` で入れて videomaker 側で切らせる。未生成は開始画像。`review --serve` の保存時にも `videomaker.auto` に従って作り直す（`make_handler` の `on_save`）。
- `notify.py` のトーストは Windows PowerShell 5.1（WinRT）経由。pwsh 7 では動かない。
- パッケージデータ（`mvgen/templates/*`）は `pyproject.toml` の `package-data` で同梱する。テンプレートを増やしたらインストール後のパスで読めるか確認する。

### 生成方式と注意

- i2v（既定）: 公式テンプレート `video_minimax_h3_i2v` と同じ構成（fl2va + `MiniMaxH3ImageToVideo` の first_frame、res_multistep、turbo LoRA 8 steps / 通常 20 steps）を `workflow.build_i2v_workflow()` で組む。I2VA 形式のプロンプトと一致するのはこちら。
- r2v: 同梱の `mvgen/templates/minimaxh3_r2v.json`（`r2v.template` で差し替え可、API 形式）のノード ID（`workflow.R2V_NODE`）を直接書き換える。テンプレートを作り直してノード ID が変わったら `R2V_NODE` も更新する。r2v のクリップは Ref2VA 6節形式のプロンプトを `clips.<id>.prompt_file` で渡すのが基本。
- 解像度の既定は 0.2MP（608×352）。確認用の低解像度で生成し、採用分を後から手動でアップスケールする運用が前提。既定値を勝手に上げない。
- 尺は `movies.frame_length()` で 24fps・17k+5 フレームに切り上げる（roughcut で尺どおりに切る）。
- テストは `tests/helpers.make_project()` で一時プロジェクトを作り、ComfyClient を `FakeClient` に差し替えて動かす。実際の `videos/` には触れない。

## サンプル制作データ

リポジトリ直下の文書類はサンプル楽曲1曲分（尺 176 秒 / 16:9 / 26 カット＝Scene 01–25 ＋ 固定エンディング E-1 ＋ 参照画像 7 枚）。画像生成は Qwen Image 2.1（ComfyUI）、動画生成は MiniMax H3（I2VA、必要時 Ref2VA）、歌と字幕は編集で載せる。ファイル名プレフィックスは `hope_`、開始画像は `output/`。

### ファイル間のデータフロー

```
plan.md（正・source of truth）
  ├─ _build_plan.py → _gen_assets.py ─→ scenes.md / scenes.csv / hope_refs.csv（画像生成用・生成物）
  └─ movies.md（動画プロンプトの正）── gen_movies_table.py ─→ movies.yaml（make_videos の入力・生成物）
```

- **`scenes.md` / `scenes.csv` / `hope_refs.csv` / `movies.yaml` は生成物。直接編集しない。** 画像プロンプトは `plan.md`、動画プロンプトは `movies.md` を直して再生成する。
- `_build_plan.py` / `_gen_assets.py` はリポジトリに存在しない（スキルでは任意のパターンとして紹介）。scenes.* を更新する必要があるときは、ユーザーに確認したうえで plan.md と一字一句一致するよう整合させる。
- movies.yaml の再生成: `python skills/music-video-production/scripts/gen_movies_table.py .`
- 検収: `python skills/music-video-production/scripts/check_mv_assets.py . --prefix hope_ --song-seconds 176`

### 画像プロンプトの規約（plan.md §2, §8）

- 固定ブロック **CH（主人公）/ ST（スタイル）/ JP（世界観・昼）/ JP-N（夜・夕暮れ）/ CS1（一貫性宣言）** を全プロンプトに**一字一句そのまま**埋め込む。固定ブロックを変える場合は全シーン・全参照画像に同じ変更を反映する。
- CS1 は人物が出るシーンのみ。人物なしのカットは `no people present`。
- `references: reference sheets <file>` を末尾近くに置く。末尾は必ず `16:9, no text`（画面内に文字を描かせない）。
- seed: シーン 01=1000 から +100 刻み（E-1=3500）、参照画像 4000–4600。
- `qwen_image_2_1_t2i.json` は cfg 1 のため**ネガティブプロンプトは実質無効**。不要要素はポジティブ側で抑える。

### 動画プロンプトの規約（movies.md §0、`h3-prompt-writing` スキル準拠）

- I2VA: 1 行目は定型文 `For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.` を一字一句そのまま。空行の後に `integrated_multimodal_description` / `overall_soundscape` / `non_diegetic_music` の 3 フィールド。
- 全クリップ `non_diegetic_music: N/A`。歌唱・台詞（`<d>`）は書かない。各クリップ 4–15 秒、合計 176 秒を崩さない。
- `[Shot 2]` 以降は `At 00:03.500, ...` 形式で厳密に増加する時刻を付ける。カメラ指示は自然英文。ブラケット命令は使わない。
- Ref2VA（6 節形式）に切り替えたクリップは `movies_ref2va.md` に退避し、`movies.md` は I2VA 方言のみに保つ。
- プロンプト方言の詳細は `h3-prompt-writing` スキル（`references/base-en.txt` / `ref-en.txt`）。探索順は skills の SKILL.md を参照。

### ComfyUI ワークフロー

- `qwen_image_2_1_t2i.json` — サンプルの画像生成（16:9 / 1MP / 25 steps / euler-simple）。`_tate` は縦長版。
- `minimaxh3_r2v.json` — MiniMax H3 の Reference-to-Video（API 形式）。`mvgen/templates/` に同じものを同梱。`with upscale (1)` 版は seed 以外同一。
- `flux3_klein_distilled_t2i.json` — 別系統の t2i（サンプルの計画書では未使用）。
