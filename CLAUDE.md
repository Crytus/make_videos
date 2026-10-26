# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

サンプル楽曲のミュージックビデオ制作プロジェクト。**絵コンテ・プロンプト文書と ComfyUI ワークフロー JSON**、および動画生成ツール（`make_videos.py` + `mvgen/`）で構成される。git 管理されていない。

- 尺 176 秒 / 16:9 / 26 カット（Scene 01–25 ＋ 固定エンディング E-1）＋ 参照画像 7 枚（REF-01〜07）
- 画像生成: Qwen Image 2.1（ComfyUI）→ 動画生成: MiniMax H3（I2VA、必要時 Ref2VA）→ 編集で歌と字幕を載せる
- ファイル名プレフィックスは `hope_`。生成済み PNG は `output/` にある

## ファイル間のデータフロー（最重要）

```
plan.md（正・source of truth）
  ├─ _build_plan.py → _gen_assets.py ─→ scenes.md / scenes.csv / hope_refs.csv（画像生成用・生成物）
  └─ movies.md（動画プロンプトの正）── gen_movies_table.py ─→ movies.yaml（動画ツール用一覧・生成物）
```

- **`scenes.md` / `scenes.csv` / `hope_refs.csv` / `movies.yaml` は生成物。直接編集しない。** 画像プロンプトの修正は `plan.md` を直し、`python _build_plan.py` → `python _gen_assets.py` で再生成する。動画プロンプトは `movies.md` を直し `movies.yaml` を再生成する。
- 注意: `_build_plan.py` / `_gen_assets.py` はこのディレクトリに存在しない。`check_mv_assets.py` / `gen_movies_table.py` は外部スキル `music-video-production`（`<skills>/media/music-video-production/scripts/`）のもの。スクリプトが見つからない状態で生成物を更新する必要があるときは、ユーザーに確認したうえで、plan.md / movies.md と一字一句一致するよう生成物側を整合させる。

### よく使うコマンド（スクリプトが利用可能な場合）

```
python _build_plan.py
python _gen_assets.py
python <skills>/media/music-video-production/scripts/gen_movies_table.py .
python <skills>/media/music-video-production/scripts/check_mv_assets.py . --prefix hope_ --song-seconds 176
```

検収スクリプトは参照 CSV を `uk_refs.csv` の名前で探すため、一時ディレクトリに `hope_refs.csv` を `uk_refs.csv` としてコピーして実行する。

## 画像プロンプトの規約（plan.md §2, §8）

- 固定ブロック **CH（主人公）/ ST（スタイル）/ JP（世界観・昼）/ JP-N（夜・夕暮れ）/ CS1（一貫性宣言）** を全プロンプトに**一字一句そのまま**埋め込む。短縮・言い換え禁止。固定ブロックを変える場合は全シーン・全参照画像に同じ変更を反映する。
- CS1 は人物が出るシーンのみ。人物なしのカットは `no people present`。
- `references: reference sheets <file>` を末尾近くに置く（生成・検収スクリプトが参照する）。参照画像は自身の行には付けない。
- 末尾は必ず `16:9, no text`。画面内に文字を一切描かせない（字幕・タイトルは編集で載せる）。
- seed: シーン 01=1000 から +100 刻み（E-1=3500）、参照画像 4000–4600。
- `qwen_image_2_1_t2i.json` は cfg 1 のため**ネガティブプロンプトは実質無効**。不要要素はポジティブ側で抑える。
- 生成順: `hope_ref_*`（特に `hope_ref_02_character-sheet` を先に確定）→ 人物シーン → 人物なしシーン。

## 動画プロンプトの規約（movies.md §0、`h3-prompt-writing` スキル準拠）

- I2VA: 1 行目は定型文 `For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.` を一字一句そのまま。空行の後に `integrated_multimodal_description` / `overall_soundscape` / `non_diegetic_music` の 3 フィールド。
- 全クリップ `non_diegetic_music: N/A`。歌唱・台詞（`<d>`）は書かない。
- 各クリップ 4–15 秒（本作は 6–10 秒、合計 176 秒）。尺表の合計を崩さない。
- `[Shot 2]` 以降は `At 00:03.500, ...` 形式で厳密に増加する時刻を付ける（複数ショットは Scene 10・13・21 のみ）。
- カメラ指示は自然英文（`The camera pushes in with small amplitude at slow speed ...`）。ブラケット命令は使わない。
- Ref2VA（6 節形式）に切り替えたクリップは `movies_ref2va.md` に退避し、`movies.md` は I2VA 方言のみに保つ。
- プロンプト方言の詳細は `h3-prompt-writing` スキル（`base-en.txt` / `ref-en.txt`）。

## 動画生成ツール（make_videos.py / mvgen/）

利用者向けの使い方は `README.md`（オプションや設定を変えたら README と `config.yaml` のコメントも更新する）。依存は PyYAML と ffmpeg/ffprobe（HTTP は標準ライブラリ）。

```
python make_videos.py [generate] --dry-run       # 生成対象の確認（API 形式ワークフローを videos/workflows/ に書き出す）
python make_videos.py status                     # 生成状況（○最新 △設定変更あり ?記録なし -未生成）
python make_videos.py review --serve             # review.html を開き、採用テイクを videos/selected.yaml に保存
python make_videos.py roughcut                   # 採用テイクを尺どおりに切ってつないだ videos/roughcut.mp4
python -m unittest -v                            # 全テスト（ComfyUI 不要。リポジトリ直下で実行）
python -m unittest tests.test_generate.TestGenerate.test_takes   # 1件だけ
```

### 構成とデータの流れ

- `config.yaml` → `mvgen/config.py`（`DEFAULTS` とマージ）。設定の優先順位は **CLI > `clips.<id>` > `generation` > DEFAULTS**。解決は `plan.resolve_clip()` が一手に担う。
- `plan.build_jobs()` がクリップ × テイクのジョブを「テイク番号 → クリップ順」で作る。保存先は take1 = `<開始画像名>.mp4`、take k = `<開始画像名>_t<k>.mp4`、seed は take1 + (k-1)*1000。
- 生成後、動画と同名の `.json` に `metadata.generation_params()`（プロンプト・尺・seed・解像度・ステップ数・画像の sha256・モデル）を記録する。現在の設定と比べて差があれば STALE（`--stale` で再生成）。**見た目に影響する設定を追加したら `generation_params()` にも入れる**こと。記録の無い動画は UNKNOWN で、自動では作り直さない。
- 生成済み（空でない mp4）はスキップ。ダウンロードや記録は `.part` に書いてから置き換える（中断で壊れたファイルを生成済みと誤認しないため）。
- `review.py` は `videos/review.html` と `review_frames/`（ffmpeg で切り出したコマ）を作る。`--serve` は 127.0.0.1 限定の http.server で、`POST …/api/selection` を `selection.save_selection()` に渡す（ファイル名だけを受け付け、実在を確認する）。
- `roughcut.py` は selected.yaml → take1 → 残りのテイクの順に使う動画を選び、ffmpeg の filter_complex で尺どおりに切って concat する。未生成は黒。
- `notify.py` のトーストは Windows PowerShell 5.1（WinRT）経由。pwsh 7 では動かない。

### 生成方式と注意

- i2v（既定）: 公式テンプレート `video_minimax_h3_i2v` と同じ構成（fl2va + `MiniMaxH3ImageToVideo` の first_frame、res_multistep、turbo LoRA 8 steps / 通常 20 steps）を `workflow.build_i2v_workflow()` で組む。I2VA 形式の movies.yaml と一致するのはこちら。
- r2v: `minimaxh3_r2v.json`（API 形式）のノード ID（`workflow.R2V_NODE`）を直接書き換える。テンプレートを作り直してノード ID が変わったら `R2V_NODE` も更新する。r2v のクリップは Ref2VA 6節形式のプロンプトを `clips.<id>.prompt_file` で渡すのが基本。
- 解像度の既定は 0.2MP（608×352）。確認用の低解像度で生成し、採用分を後から手動でアップスケールする運用が前提。既定値を勝手に上げない。
- 尺は `movies.frame_length()` で 24fps・17k+5 フレームに切り上げる（roughcut で尺どおりに切る）。
- テストは `tests/helpers.make_project()` で一時プロジェクトを作り、ComfyClient を `FakeClient` に差し替えて動かす。実際の `videos/` には触れない。

## ComfyUI ワークフロー

- `qwen_image_2_1_t2i.json` — 本作の画像生成（16:9 / 1MP / 25 steps / euler-simple）。`_tate` は縦長版。
- `minimaxh3_r2v.json` — MiniMax H3 の Reference-to-Video（API 形式、LoadImage ×3）。`make_videos.py --mode r2v` のテンプレート。`with upscale (1)` 版は seed 以外同一。
- `flux3_klein_distilled_t2i.json` — 別系統の t2i（本作の計画書では未使用）。
