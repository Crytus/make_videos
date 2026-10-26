# 希望の道 — 動画生成シナリオ（MiniMax H3 / I2VA）

## 0. モデル仕様とプロンプト規約

- **採用モード**: **I2VA**（Image-to-Video-with-Audio）。各クリップには `scenes.md` の**シーン静止画1枚だけ**をアップロードする。静止画は `hope_ref_*` から作られているので、参照プレートを同時に渡す必要はない（渡すほど H3 はパレットを混ぜる）。
- **尺の範囲**: 4–15秒。本作は 6–10秒（平均6.8秒、合計176秒）。
- **解像度**: 1920×1080 / 16:9 / 24fps。静止画は 1152×648 から 2倍アップスケールして渡す。
- **歌**: 本編の歌は**編集で載せる**（生成音声には歌わせない）。したがって全クリップで `non_diegetic_music: N/A`、画面内に字幕・歌詞・タイトルは描かせない。`integrated_multimodal_description` に `<d>`（歌唱・台詞）は一切書かない。
- **プロンプト規約（`h3-prompt-writing` 準拠）**:
  - 1行目は I2VA の定型文を**一字一句そのまま**。空行を挟んでから3フィールド。
  - ラベルは `<Picture N>`。本作は各クリップ1枚なので `<Picture 1>` のみ。番号は全クリップで固定。
  - `[Shot 2]` 以降は `At 00:03.500, ...` 形式で**厳密に増加**する時刻を付ける。本作は基本1ショット（静止画から連続して伸ばす＝I2VAの得意形）で、カットを割るのは Scene 10・13・21 の3本だけ。
  - カメラは `The camera pushes in with small amplitude at slow speed toward ...` の自然英文。ブラケット命令（`[Push in]`）は使わない。
  - 人物は主人公のみ。台詞がないので話者ID（`S1`）は付けない。
- **演技の統一**: 泣きは「目を開いたまま一滴」。笑いは「口角だけ」。走らない、跳ねない、振り向きすぎない。感情は**光の量**と**歩く速さ**で語る。
- **Ref2VA への切り替え**: 顔が崩れたカットだけ、静止画＋`hope_ref_02_character-sheet`＋`hope_ref_01_location-path-dawn` の3枚を上げて Ref2VA（`subject_definitions` / `summary` / `retention_analysis` / `detailed_description` / `overall_soundscape` / `non_diegetic_music` の6節）で撮り直す。この場合 `<Picture 1>` が開始フレーム、`<Subject 1>` が人物、`<Subject 2>` が道の形状になる。切り替えたクリップだけ `movies_ref2va.md` に退避し、本ファイルは I2VA のまま保つ（方言の混在禁止）。

## 1. 尺表

| # | シーン名 | 秒数 | 累積 | 開始画像（Picture 1） | 補助参照 |
|---|---|---|---|---|---|
| 01 | 夜明け前の一本道 | 8 | 0:08 | `hope_01_path_before_dawn.png` | なし |
| 02 | 新しい朝が | 6 | 0:14 | `hope_02_new_morning_sky.png` | なし |
| 03 | 窓を照らすよ | 6 | 0:20 | `hope_03_window_light.png` | なし |
| 04 | 胸に秘めた光 | 6 | 0:26 | `hope_04_light_in_hands.png` | なし |
| 05 | 解き放つ時 | 6 | 0:32 | `hope_05_release_the_light.png` | なし |
| 06 | 小さなつぼみ | 6 | 0:38 | `hope_06_small_bud.png` | なし |
| 07 | 夢を抱きしめ | 6 | 0:44 | `hope_07_holding_the_dream.png` | なし |
| 08 | 風に揺れても | 6 | 0:50 | `hope_08_bending_in_wind.png` | なし |
| 09 | 顔上げて進む | 6 | 0:56 | `hope_09_chin_up_walk_on.png` | なし |
| 10 | 時には涙 | 7 | 1:03 | `hope_10_a_tear.png` | なし |
| 11 | こぼれる日も | 7 | 1:10 | `hope_11_walking_in_rain.png` | なし |
| 12 | それでも強く | 7 | 1:17 | `hope_12_still_strong.png` | なし |
| 13 | 立ち上がるから | 7 | 1:24 | `hope_13_standing_up.png` | なし |
| 14 | 誰も知らない | 7 | 1:31 | `hope_14_nobody_knows.png` | なし |
| 15 | 未来の扉 | 7 | 1:38 | `hope_15_door_of_the_future.png` | なし |
| 16 | 自分の手で | 7 | 1:45 | `hope_16_with_my_own_hands.png` | なし |
| 17 | 開いていこう | 8 | 1:53 | `hope_17_open_it_up.png` | なし |
| 18 | 輝く星は | 6 | 1:59 | `hope_18_the_stars.png` | なし |
| 19 | いつも見守る | 6 | 2:05 | `hope_19_always_watching.png` | なし |
| 20 | 信じる心 | 6 | 2:11 | `hope_20_believing_heart.png` | なし |
| 21 | 道しるべだよ | 6 | 2:17 | `hope_21_a_signpost.png` | なし |
| 22 | 優しい笑顔 | 7 | 2:24 | `hope_22_gentle_smile.png` | なし |
| 23 | 希望を咲かせ | 7 | 2:31 | `hope_23_hope_blooms.png` | なし |
| 24 | 自分らしく | 7 | 2:38 | `hope_24_as_i_am.png` | なし |
| 25 | 生きていこう | 8 | 2:46 | `hope_25_live_on.png` | なし |
| E-1 | 希望の道（固定エンディング） | 10 | 2:56 | `hope_E1_ending.png` | なし |

**合計 176秒（2分56秒）** = 想定楽曲尺と一致。

## 2. シーン別プロンプト

### Scene 01 — 夜明け前の一本道

- **シーン名**: 夜明け前の一本道（Intro）
- **秒数**: 8 秒
- **対応歌詞**: （イントロ／歌唱なし）
- **参照画像ファイル名（アップロード順）**:
  1. `hope_01_path_before_dawn.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage with soft 35mm film grain and gentle halation, matching the composition, colour and exposure of <Picture 1>: a low-angle wide shot of an empty stone-paved path curving between terraced rice fields toward a lone cherry tree on the hill crest before dawn. The frame holds the same geometry throughout — path entering at the lower left, wooden fence and grass in the near foreground, crest and tree at the upper centre — while the light changes around it. Mist drifts slowly from right to left at knee height and thins as the seconds pass, uncovering two more rows of terrace stones and the wet black outline of the fence. The indigo sky above the crest shifts from deep blue to a pale silver band along the horizon; the single small window light far down the path brightens, flickers once and steadies. The tree at the crest stays motionless and only its outer twigs move a little. Grass heads in the foreground sway in a slow shallow breeze. The camera pushes in with small amplitude at slow speed, bringing the crest slightly nearer and lowering the horizon by a few percent, then settles into a static shot for the final second so the frame can cut cleanly into the next sunrise image. No figure enters the path at any point; the emptiness is the subject.

overall_soundscape: A thin high dawn wind moves through the grass and the distant cedar grove. Water drips somewhere below the path, and a single small bird calls twice from the valley.

non_diegetic_music: N/A
```

- **編集メモ**: 尺は8秒。冒頭は完全静止に近く、3秒目から気づく程度のプッシュイン。次の Scene 02 へは空の明度が揃うタイミングでカット。

### Scene 02 — 新しい朝が

- **シーン名**: 新しい朝が（Verse 1）
- **秒数**: 6 秒
- **対応歌詞**: 新しい朝が
- **参照画像ファイル名（アップロード順）**:
  1. `hope_02_new_morning_sky.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a wide shot of the dawn sky over a Japanese valley, thin layered clouds catching gold along their edges while the sun is still below the horizon. The cloud layers keep exactly the positions and shapes they have in <Picture 1> at the start; they then drift slowly toward the upper right while the gold along their lower edges widens and turns warmer, moving from pale peach to a saturated amber. A band of deep blue still holds at the very top of the frame. Light spills upward as the sun clears the ridge, and the underside of the highest thin cloud lights up last. Three small birds cross the lower third from left to right in a loose line, flapping twice each, and exit the frame. The pink mist far below in the valley brightens gradually and begins to dissolve. The camera tilts up with small amplitude at slow speed, giving the sky more of the frame, and then holds. No horizon detail, buildings or power lines appear. The final frame is noticeably brighter than the first, so the cut into the interior room reads as a continuation of the same sunrise.

overall_soundscape: A wide, quiet valley ambience with a light wind at height. Three small birds pass with soft wingbeats, and a distant dog barks once far below.

non_diegetic_music: N/A
```

- **編集メモ**: 6秒。空の明度が上がるだけのカット。ここで観客の目を「光」に慣らす。

### Scene 03 — 窓を照らすよ

- **シーン名**: 窓を照らすよ（Verse 1）
- **秒数**: 6 秒
- **対応歌詞**: 窓を照らすよ
- **参照画像ファイル名（アップロード順）**:
  1. `hope_03_window_light.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a medium shot inside a small Japanese room where a rectangle of morning sunlight lies across the wooden floorboards and the end of a low bed. The young woman in <Picture 1> keeps her exact position, clothing, hairstyle and the brass key on its dark cord: she sits on the edge of the bed in a loose side view, bare feet set down inside the rectangle of light. At the start her shoulders are soft and her gaze is down; she then lifts her head slowly toward the window light, and her hand slides along the mattress. The rectangle of light creeps left across the boards as the sun rises, its edge crossing her toes, then the top of her foot, then the boards beside her. Dust motes turn visibly inside the beam, drifting up and to the right, caught by the light. A thin curtain edge lifts a little where air moves past the window. Her bob shifts with the small movement of her head and one strand falls forward. The camera pushes in with small amplitude at slow speed, tightening from the full room to her upper body and the light on the floor, and holds. She never looks at the camera. The last frame leaves her face just off-centre, lit from the window side.

overall_soundscape: A quiet wooden house interior with a faint creak of floorboards and the soft shift of a quilt. Birds outside the window, muffled through glass, and the brush of fabric as her hand moves.

non_diegetic_music: N/A
```

- **編集メモ**: 6秒。光の長方形が足を越える一瞬を、歌詞「窓を照らすよ」の頭に合わせる。

### Scene 04 — 胸に秘めた光

- **シーン名**: 胸に秘めた光（Verse 1）
- **秒数**: 6 秒
- **対応歌詞**: 胸に秘めた光
- **参照画像ファイル名（アップロード順）**:
  1. `hope_04_light_in_hands.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic macro footage, soft 35mm film grain and strong halation around the light source, matching <Picture 1>: two cupped hands held together at her chest, the small tarnished brass key on its thin dark cord resting inside the palms, everything behind them falling into soft brown shadow. At the start the glow between the palms is faint — a warm orange point just visible through the gap. Her fingers close a fraction tighter, one thumb shifting to press against the other, and the point of light brightens in a slow pulse, dimming, then rising again a little stronger, so that the inner edges of her fingers turn translucent amber and a thin light spills out along the seam between her hands. The key catches a single specular highlight that slides along its bow as her palms tilt slightly upward. Fine skin texture, thin veins on the wrists and a few loose strands of her bob at the top edge of frame stay visible in the shadow. The camera pushes in with very small amplitude at slow speed toward the seam between her fingers and settles into a static shot as the glow reaches its brightest point. The pool of warm light on her knuckles grows slightly while the background remains almost black. The final frame is the brightest of the clip, so the cut to the open hands can release it.

overall_soundscape: Near silence with a soft indoor room tone. A tiny metallic tick from the key as it settles against her palm, and slow quiet breathing.

non_diegetic_music: N/A
```

- **編集メモ**: 6秒。この「掌の光」は Scene 05 → 13 → 20 → 25 と反復する。毎回少しずつ大きく、最後は画面の外まで。

### Scene 05 — 解き放つ時

- **シーン名**: 解き放つ時（Verse 1）
- **秒数**: 6 秒
- **対応歌詞**: 解き放つ時
- **参照画像ファイル名（アップロード順）**:
  1. `hope_05_release_the_light.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: the young woman standing in the doorway of an old Japanese house with the sliding wooden door open behind her, strong backlight from outside rimming her hair and shoulders. She keeps the identity, clothing and brass key of <Picture 1>. At the start her hands are closed at her chest as in the previous image; she opens them outward and upward, and scattered points of golden light lift from her palms, drifting apart and rising past her shoulders into the doorway light, where they thin out and vanish after a metre or so. Her denim jacket sleeve falls back as her arms open. She does not throw her arms wide: the gesture stops at shoulder height, palms up, and her face stays calm with her chin slightly raised. Outside the door, the morning light on the stone threshold brightens as the door finishes sliding, and the long shadow of the door frame slides away from her feet. She then steps forward once onto the stone threshold, her white canvas sneaker landing on the lit stone. The camera pushes in with small amplitude at slow speed as her hands open, then holds a static shot while she steps. The last frame is dominated by the bright doorway, with her body partly silhouetted.

overall_soundscape: Old wood sliding in its groove, the soft scuff of a canvas shoe on stone, and a breeze moving through the doorway carrying distant birdsong.

non_diegetic_music: N/A
```

- **編集メモ**: 6秒。Verse 1 の締め。ここで一度、光を「外」へ渡す。

### Scene 06 — 小さなつぼみ

- **シーン名**: 小さなつぼみ（Verse 2）
- **秒数**: 6 秒
- **対応歌詞**: 小さなつぼみ
- **参照画像ファイル名（アップロード順）**:
  1. `hope_06_small_bud.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic macro footage, soft 35mm film grain, matching <Picture 1>: a low-angle macro of a single closed pale bud on a slender green stem among wild mustard flowers on a grassy riverbank, backlit so the bud's edges glow translucent and the background dissolves into deep green bokeh. The bud keeps exactly the shape, size and angle it has in <Picture 1> — it must not open at any point in this clip. The stem sways in a light breeze, moving the bud three or four centimetres through the frame and back; the movement is slow and elastic, and the bud always returns to its original position. Dew beads on the petals slide a millimetre or two, merge, and one bead falls out of frame, catching a bright specular point as it drops. Mustard flowers in the near foreground blur and sharpen as they move closer to the lens, and a second out-of-focus stem crosses the lower left. The sun behind the plant brightens slightly as a thin cloud passes, so the halo around the bud swells and then settles. The camera holds a static shot and lets the plant move; a very small push in at slow speed brings the bud a little closer in the final two seconds. Warm gold light, no insects, no hands, no change of species.

overall_soundscape: A light breeze moving through grass and the fine dry rustle of mustard stems. The soft ticking of a water drop falling from a leaf onto the soil, and a river running quietly behind.

non_diegetic_music: N/A
```

- **編集メモ**: 6秒。**開花させないこと**。開花は Scene 23 だけ。構図を Scene 23 と完全一致させる基準カットでもある。

### Scene 07 — 夢を抱きしめ

- **シーン名**: 夢を抱きしめ（Verse 2）
- **秒数**: 6 秒
- **対応歌詞**: 夢を抱きしめ
- **参照画像ファイル名（アップロード順）**:
  1. `hope_07_holding_the_dream.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a medium close-up at eye level on a grassy riverbank, where the young woman crouches and gently cups a single pale bud in both hands, her bob falling forward over her cheek and the brass key swinging free beneath her collar. She keeps the identity, hair, denim jacket and cream dress of <Picture 1>. At the start her eyes are open and lowered toward the bud; she then closes them slowly and her expression relaxes into a faint smile, the corners of her mouth lifting only slightly. Her hands stay cupped and still — she never picks or bends the flower. Her breathing shows in the small rise and fall of her shoulders. Wind moves the loose hair at her temple and lifts the collar of her jacket, and the mustard flowers behind her nod but stay out of focus. The morning light on her cheek warms by a few degrees as a cloud clears the sun, and a soft flare appears in the top corner and then thins. The camera pushes in with small amplitude at slow speed, moving from her hands and face to mostly her closed eyes and the edge of the bud, and then holds. No second person, no animals, no picking action at any point.

overall_soundscape: Grass and mustard stems rustling in a light breeze. Quiet, steady breathing close to the microphone, and the river running behind her.

non_diegetic_music: N/A
```

- **編集メモ**: 6秒。目を閉じる瞬間を歌詞の「夢を」に重ねる。

### Scene 08 — 風に揺れても

- **シーン名**: 風に揺れても（Verse 2）
- **秒数**: 6 秒
- **対応歌詞**: 風に揺れても
- **参照画像ファイル名（アップロード順）**:
  1. `hope_08_bending_in_wind.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a low-angle medium shot of the young woman standing braced on the riverbank as a strong gust flattens the grass and whips the hem of her denim jacket sideways, one forearm raised against the wind, hair blown across her face, eyes narrowed but open. She keeps the identity, clothing and brass key of <Picture 1>. The gust arrives at the start of the clip and builds for three seconds, then eases. Her jacket hem lifts and snaps to the left, the collar stands away from her neck, and her bob streams sideways across her cheek and mouth so part of her face is hidden and then revealed again. She plants her back foot and leans slightly into the wind without losing balance; her raised forearm takes the pressure and her hand opens flat. Behind and beside her the grass goes down in waves from right to left, and the pale bud on its stem bends hard almost horizontal but does not snap — its stem stays continuous and springs back when the gust eases. The overcast silver light thins near the end as a break of gold appears in the clouds behind her, brightening the rim of her hair. The camera holds a static shot through the gust, then pushes in with very small amplitude at slow speed as the wind drops. She is not blown over and no plants break.

overall_soundscape: A strong gust rushing through grass and fabric, the snap of a jacket hem, and a low sustained wind under it. The rustle of a dense field bending all at once.

non_diegetic_music: N/A
```

- **編集メモ**: 6秒。風向きは全カット左→右で統一。ここだけ音を荒く、彩度は落とさない。

### Scene 09 — 顔上げて進む

- **シーン名**: 顔上げて進む（Verse 2）
- **秒数**: 6 秒
- **対応歌詞**: 顔上げて進む
- **参照画像ファイル名（アップロード順）**:
  1. `hope_09_chin_up_walk_on.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic tracking footage, soft 35mm film grain, matching <Picture 1>: a medium shot from behind and slightly to the side as the young woman lifts her chin to the sky and then walks forward along the stone path between the rice terraces, her jacket swinging, long early shadows raking across the stones. She keeps the identity, hair, jacket, dress and brass key of <Picture 1>. At the start she is standing still, seen from behind at hip height; she raises her chin, holds for a beat, then steps off with her left foot. Her stride is unhurried and even — no running, no bouncing — and her arms move loosely. The white canvas sneakers meet the stones one after another, settling on the flat faces and skipping the cracks. Her shadow shortens slightly and slides to her right as the sun climbs. The path stones pass beneath her at a steady rate, and the terrace wall on the left and the fence on the right slide out of the back of the frame. Dust lifts a little at each footfall and hangs in the low light. The camera tracks forward with the same speed as her walk, keeping her at the same size in frame, with small amplitude and at slow speed. In the last second she lifts her head a touch higher and her shoulders square. The clip ends mid-stride so it can cut on movement into the rain section.

overall_soundscape: Even footsteps on stone with a light scuff of rubber, the swing of denim, and a morning breeze with distant birds.

non_diegetic_music: N/A
```

- **編集メモ**: 6秒。歩き出しでサビ前を抜ける。カット尻は「動きの中で切る」。


### Scene 10 — 時には涙

- **シーン名**: 時には涙（Chorus）
- **秒数**: 7 秒
- **対応歌詞**: 時には涙
- **参照画像ファイル名（アップロード順）**:
  1. `hope_10_a_tear.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: an extreme close-up in profile of the young woman standing in falling rain on a suburban street, wet strands of her bob stuck to her cheek, eyes glassy but held open, freckles visible under the water. She keeps the identity, hair and clothing of <Picture 1>. Her eyes do not close and she does not sob: her jaw tightens once, and a single tear leaves her lower lash, runs down over her freckles, and hangs at the line of her jaw before falling out of frame. Rain runs down her temple and off her chin in thin continuous streams. Each blink clears the water from her lashes and it gathers again immediately. Her lips part slightly and then close. The flat grey light stays even, with a narrow specular highlight running down her wet cheek.
[Shot 2] At 00:04.500, the shot cuts to a wider view from behind at shoulder height: she stands motionless on the wet sidewalk with her back to camera, shoulders slightly bowed, rain streaking diagonally past her and the red mailbox and wet asphalt reflections of the street lamps in the lower third. She does not move except for the smallest shift of weight from one foot to the other, and her hand closes slowly around the cord of her brass key. The camera holds a static shot in both parts; there is no push in. Rain is visible in both shots at the same angle, and her clothing and hair are equally wet across the cut.

overall_soundscape: Steady rain on fabric, asphalt and the metal lid of a mailbox, with water running in gutters nearby. Faint traffic noise far off and one car passing on wet road.

non_diegetic_music: N/A
```

- **編集メモ**: 7秒。涙は一滴だけ。4.5秒でカット。ここから Scene 13 まで彩度を10%落とす。

### Scene 11 — こぼれる日も

- **シーン名**: こぼれる日も（Chorus）
- **秒数**: 7 秒
- **対応歌詞**: こぼれる日も
- **参照画像ファイル名（アップロード順）**:
  1. `hope_11_walking_in_rain.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a wide shot of a rain-soaked suburban Japanese sidewalk with a red-painted mailbox and low street lamps, mirror-like puddles reflecting the grey sky, rain streaking diagonally. The young woman of <Picture 1> walks alone along the sidewalk without an umbrella, shoulders slightly bowed, one hand closed around the cord of her brass key. She enters the action already walking at the left side of frame and continues left to right at an even, tired pace, neither hurrying nor stopping. Her hair is flat with water, her denim jacket darkens across the shoulders, and the hem of her cream dress is wet to mid-calf. Each footfall breaks a puddle and the reflection of the streetlamp shatters, then reassembles a metre behind her. She passes the mailbox: its red paint and the wet metal lid hold a hard line of light, and the water dripping from its edge is visible. Her reflection crosses the puddles upside down under her. She does not look up, does not wipe her face, and does not shelter under anything. In the final second her stride shortens slightly and her head begins to turn a few degrees toward the sky, setting up the next shot. The camera tracks left to right with her at walking speed, medium amplitude, keeping the sidewalk lines converging ahead of her.

overall_soundscape: Heavy steady rain on asphalt, metal and fabric, with water running fast along the gutter. Wet footsteps and the soft drag of soaked clothing.

non_diegetic_music: N/A
```

- **編集メモ**: 7秒。横移動のみ。傘は絶対に持たせない（雨を「受ける」ことが主題）。

### Scene 12 — それでも強く

- **シーン名**: それでも強く（Chorus）
- **秒数**: 7 秒
- **対応歌詞**: それでも強く
- **参照画像ファイル名（アップロード順）**:
  1. `hope_12_still_strong.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a medium close-up from slightly below as the young woman stands in steady rain and raises her face into it while one narrow column of sunlight breaks through the clouds and lands on her face, water beading on her skin, her jaw set and her eyes steady and open. She keeps the identity, hair, jacket and brass key of <Picture 1>. At the start her chin is low; she lifts it slowly through the first two seconds until her face is fully turned to the sky, then holds. The column of light widens slightly and drifts left across her cheek, so that half her face is lit warm and half stays in cold grey rain. Droplets inside the beam glow silver and those outside it stay dull. Her eyes stay open and she blinks twice against the water without lowering her head. Her wet hair is pushed back from her forehead by the rain itself rather than by her hand. Her shoulders drop and settle, and the small tension at her jaw releases at the very end while her expression stays determined. The camera pushes in with small amplitude at slow speed toward her eyes and then holds a static shot. The rain never stops and no rainbow or clear sky appears.

overall_soundscape: Rain continuing at the same density throughout, with droplets striking her jacket close to the microphone. A faint low wind and distant water running in a gutter.

non_diegetic_music: N/A
```

- **編集メモ**: 7秒。光の柱は画面の対角に。ここで雨の彩度をわずかに戻し始める。

### Scene 13 — 立ち上がるから

- **シーン名**: 立ち上がるから（Chorus）
- **秒数**: 7 秒
- **対応歌詞**: 立ち上がるから
- **参照画像ファイル名（アップロード順）**:
  1. `hope_13_standing_up.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a low-angle medium shot on wet stone paving just after the rain, where the young woman crouches and then pushes herself up with one hand on her knee, water dripping from her jacket hem, the pale sky reflected in the puddle under her sneakers. She keeps the identity, hair, clothing and brass key of <Picture 1>. She starts low in frame, folded down, her hand on her knee and her head down; she then rises in one continuous movement over three seconds — hand pressing on the knee, back straightening, hips coming up, and finally her face entering the top of the frame. Her wet hair swings back as her head comes up and stays behind her shoulders. Water runs off her jacket hem and the ends of her sleeves in thin streams and joins the puddle, which ripples and briefly blurs the sky reflected in it. The angle stays low so she grows upward through the frame rather than the camera moving.
[Shot 2] At 00:05.000, the shot cuts to a close-up of her face from the front, three-quarter lit: the rain has almost stopped, single drops still falling past the lens, her lashes stuck together and her cheeks wet, and the first warm after-rain light on the side of her nose and mouth. She looks straight ahead, not at the camera, and her lips close into a firm line as she exhales. The camera holds a static shot to the end. Rain density is clearly lighter in the second shot than in the first, and her wet clothing is continuous across the cut.

overall_soundscape: Water dripping steadily from clothing onto stone, a wet hand sliding on wet fabric, and footsteps settling as she stands. Rain easing to scattered drops.

non_diegetic_music: N/A
```

- **編集メモ**: 7秒。5秒でカット。立ち上がりに合わせて彩度と明度が戻る＝サビの解答。

### Scene 14 — 誰も知らない

- **シーン名**: 誰も知らない（Bridge）
- **秒数**: 7 秒
- **対応歌詞**: 誰も知らない
- **参照画像ファイル名（アップロード順）**:
  1. `hope_14_nobody_knows.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a wide shot from below of an old moss-covered stone staircase climbing into a cedar grove at dusk, the young woman seen from behind halfway up the steps with one hand flat on the mossy stone wall, climbing steadily without looking back. She keeps the identity, hair, jacket, dress and brass key of <Picture 1>. She climbs at a slow, deliberate pace, lifting each foot onto the next stone and bringing the trailing foot level before the next step, so her whole body rises in small regular increments. Her hand slides along the wall, fingers catching in the moss, then lifting and setting down again further up. Her jacket hem and the ends of her hair swing a little with each step. Wet moss holds the low sky light as a thin green sheen, and a few loose leaves fall past the camera from the trees above. The light dims by degrees as she climbs into the shadow of the cedars, and two more stars become visible between the trunks. The camera tilts up with small amplitude at slow speed, following her upward but never overtaking her, so she stays in the lower third and the door at the top of the steps is barely visible in shadow. She never turns her head. The final frame leaves her a little higher and further away than the first.

overall_soundscape: Footsteps on damp stone with moss giving slightly underfoot, her hand brushing the wall, and a light wind moving high in the cedars. Crickets beginning below in the valley.

non_diegetic_music: N/A
```

- **編集メモ**: 7秒。上昇のみ。扉はまだ見せない（シルエットで予告だけ）。

### Scene 15 — 未来の扉

- **シーン名**: 未来の扉（Bridge）
- **秒数**: 7 秒
- **対応歌詞**: 未来の扉
- **参照画像ファイル名（アップロード順）**:
  1. `hope_15_door_of_the_future.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a close-up of an old weathered wooden door at the top of the mossy stone steps, ivy creeping across its frame, a rusted iron hinge, a thin seam of warm light escaping through the gap between door and frame, deep blue dusk behind. The door stays shut for the whole clip. Ivy leaves tremble in the evening wind and one leaf lets go and falls past the lens. The thin seam of light widens almost imperceptibly — a millimetre at most — as the wood settles, then steady again, breathing with the warm glow inside. Where the light passes the ivy, the leaf edges glow green-gold. Dust drifts in the light seam. The iron hinge shows rust texture that catches a small highlight as the light shifts. There is no person and no sound of a person. The camera pushes in with very small amplitude at slow speed toward the seam of light, the door filling more of the frame, and then holds a static shot so the last frame is nearly the light itself — the door's wood reduced to a dark border. The warm light grows slightly brighter across the clip while the blue dusk around it deepens.

overall_soundscape: A very quiet evening on a hillside: a low wind in the cedars, ivy moving against wood, and the faint dry creak of old timber settling. No footsteps.

non_diegetic_music: N/A
```

- **編集メモ**: 7秒。人物なし。ここだけ「光だけの画」にして、次で手を入れる。

### Scene 16 — 自分の手で

- **シーン名**: 自分の手で（Bridge）
- **秒数**: 7 秒
- **対応歌詞**: 自分の手で
- **参照画像ファイル名（アップロード順）**:
  1. `hope_16_with_my_own_hands.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic macro footage, soft 35mm film grain and halation around the light from the keyhole, matching <Picture 1>: a close view of her hand lifting the small tarnished brass key on its thin dark cord away from her chest and guiding it into the old iron keyhole, warm amber light from inside the keyhole washing over her fingers while cold blue dusk sits on the back of the hand. Her fingertips find the keyhole, feel for the slot once, and press the key home; her thumb and forefinger then turn it a quarter turn, with visible effort at the halfway point, the tendons in the back of her hand tightening. The key stops hard at the end of the turn. As it turns, the seam of light around the keyhole brightens and throws a thin vertical line of amber up across her knuckles. Tiny flakes of rust fall from the plate and catch the light as they drop out of frame. Her fingers stay in frame the whole time, close to the wood grain, which is worn smooth in a circle around the keyhole from years of use. The camera pushes in with very small amplitude at slow speed toward the keyhole and holds; the focus stays on her fingertips and the brass. No second hand, no second key, no modern lock.

overall_soundscape: The small metallic scrape of a brass key entering an iron keyhole, a dry click, then the creak of a stiff mechanism turning. Her breathing, close and controlled.

non_diegetic_music: N/A
```

- **編集メモ**: 7秒。手だけのカット。鍵を回す「抵抗」を見せる（一発で開かない）。

### Scene 17 — 開いていこう

- **シーン名**: 開いていこう（Bridge）
- **秒数**: 8 秒
- **対応歌詞**: 開いていこう
- **参照画像ファイル名（アップロード順）**:
  1. `hope_17_open_it_up.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage with heavy halation and a bloom across the highlights, soft 35mm film grain, matching <Picture 1>: a medium-wide shot looking through an old wooden door as it swings inward at the top of the stone steps, the young woman standing on the threshold in silhouette with the brass key still in her hand, warm dawn light flooding past her into the dark cedar corridor. She keeps the posture and silhouette of <Picture 1>. The door moves slowly at first, then faster as its weight takes over, until it stands open against the light. Light pours through the widening gap in a horizontal band, then spreads until the whole frame beyond her is white-gold and the interior around the camera falls to deep shadow. Her silhouette sharpens against it: the edge of her bob, the shoulder line of her denim jacket, the hem of her dress, and the small key hanging from her fingers as her arm comes down. Her hair and the loose ivy at the door frame move in the draft from outside. Dust and seed fluff lift through the light and drift toward the camera. She does not step through: the clip ends with her still on the threshold, one hand on the door edge, and the frame almost overexposed around her.
The camera pushes in with small amplitude at slow speed through the opening door, ending close to her back-lit outline, and holds. The exposure rises gently across the eight seconds rather than snapping.

overall_soundscape: A heavy wooden door swinging on old hinges with a long groan, then air moving through the opening. Wind stirring ivy and dry leaves outside, and a distant morning bird.

non_diegetic_music: N/A
```

- **編集メモ**: 8秒。Bridgeの白飛び。ここだけ露出を上げる（+1.5段相当）。編集で次の星空へ落とす。

### Scene 18 — 輝く星は

- **シーン名**: 輝く星は（Verse 3）
- **秒数**: 6 秒
- **対応歌詞**: 輝く星は
- **参照画像ファイル名（アップロード順）**:
  1. `hope_18_the_stars.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a wide shot of a hilltop at night with a lone cherry tree in silhouette at the left of frame, the faint band of the Milky Way across the upper right, warm town lights far down the valley. The stars stay in their exact positions — no star moves, twinkles dramatically or trails. The Milky Way holds its shape while becoming marginally more visible as the eye adjusts. Thin cloud drifts very slowly across the lower third of the sky below the star band, and where it passes in front of the town glow it carries a faint warm underside. The tree's branches are almost perfectly still; only the finest twigs move. Dew on the grass catches points of starlight that brighten slightly as the camera settles. One faint shooting star crosses a short distance in the upper left during the third second and is gone. The camera holds a static shot, then tilts up with small amplitude at slow speed so the Milky Way takes more of the frame and the tree's crown reaches the lower left corner. No moon, no aircraft, no artificial light on the hill.

overall_soundscape: A wide night ambience: light wind through grass, crickets in the valley, and one distant dog. Almost silent at the top of the hill.

non_diegetic_music: N/A
```

- **編集メモ**: 6秒。星は動かさない。冒頭は音楽を抜いて環境音だけにすると映える。

### Scene 19 — いつも見守る

- **シーン名**: いつも見守る（Verse 3）
- **秒数**: 6 秒
- **対応歌詞**: いつも見守る
- **参照画像ファイル名（アップロード順）**:
  1. `hope_19_always_watching.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a close-up from above of the young woman lying back in the grass under the lone tree and looking up at the sky, stars reflected as small white points in her open eyes, her breath faintly visible, hair fanned out in the grass, one hand resting on the brass key. She keeps the identity, hair, clothing and key of <Picture 1>. She does not move her head at all: her eyes stay open and travel very slightly, following a point that crosses the sky, and the reflected star points in them shift by a millimetre or two. A single blink, slow and complete, clears and returns the reflections. Her chest rises and falls evenly and her breath shows as a faint white wisp that drifts out of the bottom of frame. A few grass blades in the near foreground move across her cheek and out again with the wind, and one strand of her bob lifts and settles. The moonlight stays cool on her skin while a faint warm rim from the valley lights her jaw and ear. The camera pushes in with very small amplitude at slow speed toward her eyes and holds. No cut, no ground movement, no insects landing.

overall_soundscape: Grass close to the microphone moving in a light night wind, quiet steady breathing, and crickets further down the hill.

non_diegetic_music: N/A
```

- **編集メモ**: 6秒。まばたき1回だけ。瞳の星の反射がこの曲の「守られている」の答え。

### Scene 20 — 信じる心

- **シーン名**: 信じる心（Verse 3）
- **秒数**: 6 秒
- **対応歌詞**: 信じる心
- **参照画像ファイル名（アップロード順）**:
  1. `hope_20_believing_heart.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain and strong halation around the glow, matching <Picture 1>: a medium close-up at night of the young woman sitting upright in the grass beside the lone tree, one palm pressed flat over the brass key at her chest, hair lifting in a light night wind. She keeps the identity, hair, clothing and key of <Picture 1>. The glow under her palm starts faint, as it did in the earlier hand image, and then grows: light leaks between her fingers, runs along the seam of her hand and up the inside of her wrist, and throws a soft warm patch onto her collar and jaw. It pulses rather than flickers — swelling, holding, easing, swelling again — and each pulse lifts the light a little further, until the warm light reaches her chin and the underside of her hair while the starlit background stays cool blue. Her fingers press down a touch harder and her knuckles whiten slightly. Her eyes are closed in the first second, then open and look forward past the camera, not into it. The night wind moves her bob, the grass around her waist, and the edge of her dress. The camera pushes in with very small amplitude at slow speed from her chest toward her face and holds, so the glow ends up at the bottom edge of frame and her lit face fills the rest. No visible light source, no runes, no sparks, no particles in the air.

overall_soundscape: A light wind through grass and fabric with crickets far down the valley. Her breathing, slow and deep, close to the microphone.

non_diegetic_music: N/A
```

- **編集メモ**: 6秒。Scene 04 と同じ光の「拡大版」。掌から出る量を明確に増やす。

### Scene 21 — 道しるべだよ

- **シーン名**: 道しるべだよ（Verse 3）
- **秒数**: 6 秒
- **対応歌詞**: 道しるべだよ
- **参照画像ファイル名（アップロード順）**:
  1. `hope_21_a_signpost.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: an extreme wide shot from high above of the stone-paved path winding down the dark hillside toward the valley, the young woman standing small at the top of the path with her back to camera, looking down its length. She keeps the silhouette, clothing and posture of <Picture 1>. A dotted line of small star-like points of light ignites along the stones, one at a time, travelling from her feet down the path and away into the valley: each point appears as a soft warm dot about the size of a firefly, holds for a moment, and stays lit as the next one appears. The chain reaches the first switchback within two seconds, the second by four seconds, and disappears into the mist at the bottom of the valley at the end. She does not move except to lower her shoulders and let her arms hang. Mist in the valley shifts slowly and the far town glow stays steady.
[Shot 2] At 00:04.000, the shot cuts to a closer view from behind her at shoulder height, slightly low: her dark bob and denim jacket in the near foreground, the lit stones running away from her feet down the slope, and the valley beyond. She takes one step forward onto the first lit stone and the light around her sneaker brightens, then holds. The camera tilts down with small amplitude at slow speed, following the line of light away from her, and holds. The number and spacing of the lit stones is continuous across the cut, and her position matches the first shot.

overall_soundscape: A high, thin night wind over the hill and the low rustle of grass. No footsteps until the single step at the end, when a canvas shoe meets stone.

non_diegetic_music: N/A
```

- **編集メモ**: 6秒。4秒でカット。光の点線は「道しるべ」の直訳。点は増えるが消えない。

### Scene 22 — 優しい笑顔

- **シーン名**: 優しい笑顔（Chorus 2）
- **秒数**: 7 秒
- **対応歌詞**: 優しい笑顔
- **参照画像ファイル名（アップロード順）**:
  1. `hope_22_gentle_smile.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a medium shot from behind on the stone path at sunrise, the young woman pausing mid-step and turning her head back over her shoulder with a soft open smile, the morning light catching the edge of her face and the brass key. She keeps the identity, hair, jacket, dress and key of <Picture 1>. Her body keeps walking away for one more half-step while her head is already turning, so the turn reads as hesitation rather than a full stop; she then settles her weight on the front foot. The turn is small — head and shoulders only, no pivot of the hips. Her bob swings across the back of her neck and comes to rest on her far shoulder, and one strand stays lifted by the breeze. Her smile grows from nothing: first the eyes, then the corners of the mouth, until her cheeks lift and her eyes narrow slightly. The sun on the side of her face is low and warm, and the fine hairs at her temple and the fuzz on her cheek catch the light as a bright edge. The valley behind her is still blue and shadowed, so her lit face is the brightest thing in the frame. The camera pushes in with small amplitude at slow speed as she turns, and holds on her face. She does not look into the lens; her gaze goes just past it.

overall_soundscape: A single scuff of a shoe on stone as she stops, the swing of denim, and a light morning breeze with distant birds. Very quiet overall.

non_diegetic_music: N/A
```

- **編集メモ**: 7秒。振り返りは肩越しのみ。笑顔は「目→口角」の順に立ち上げる。

### Scene 23 — 希望を咲かせ

- **シーン名**: 希望を咲かせ（Chorus 2）
- **秒数**: 7 秒
- **対応歌詞**: 希望を咲かせ
- **参照画像ファイル名（アップロード順）**:
  1. `hope_23_hope_blooms.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic macro footage, soft 35mm film grain and halation around the backlight, matching <Picture 1> in framing, camera position, background bokeh and species: the pale bud on the grassy riverbank now opening. At 0.00 the petals are still partly closed; over the first four seconds they unfold outward one after another, outer petals first and the innermost last, each opening with a slow elastic release rather than a mechanical pop. The stem does not move from its position and the rest of the plant stays exactly as in the earlier bud shot. As the flower opens, glittering golden motes of light lift from its centre and drift upward into the backlit morning air, small and sparse at first, then a slow steady stream that thins as it rises. Dew beads slide off the petal edges as they tilt, each one catching a specular point before it falls out of frame. The backlight swells slightly and turns the open petals translucent so the fine veins are visible. The camera holds a static shot at first, then pushes in with very small amplitude at slow speed toward the opened flower and holds. The final frame is a fully open flower with light rising out of it. No insects, no hands, no second flower, no change of species, no wilting.

overall_soundscape: A soft silence dominated by the breeze in the grass and the faint rustle of petals opening. The tiny tick of a dew drop leaving a petal edge.

non_diegetic_music: N/A
```

- **編集メモ**: 7秒。**Scene 06 と同構図**。編集で06と重ねて比較できるようにしておく（同位置・同倍率）。

### Scene 24 — 自分らしく

- **シーン名**: 自分らしく（Chorus 2）
- **秒数**: 7 秒
- **対応歌詞**: 自分らしく
- **参照画像ファイル名（アップロード順）**:
  1. `hope_24_as_i_am.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a wide shot from behind as the young woman walks away up the stone path straight into the low sunrise, her long shadow stretching toward the camera across the stones, the edges of her denim jacket glowing with rim light. She keeps the identity, hair, clothing and brass key of <Picture 1>. She walks with an easy stride, arms loose, neither slow nor hurried, and her shadow moves with her across the lit stones, shortening slightly as the sun climbs. The sun is directly ahead, so her figure is a partly silhouetted shape with a bright rim along her shoulders, the back of her head and the hem of her jacket; individual strands of hair at the back of her head catch the light as thin bright lines. One large soft lens flare sits low in the frame, sliding slowly to the left as the camera moves. Ahead of her the path rises over the crest and the sky is a flat pale gold with three birds crossing it from left to right. Greenery on both sides stays in cool shadow, and the terrace walls run as dark lines away from the camera. The camera tracks forward behind her with small amplitude at slow speed, keeping her at the same size, never overtaking her. She does not turn around and her face is never visible. The clip ends before she reaches the crest.

overall_soundscape: Steady footsteps on stone receding slightly, a light morning wind, and three birds calling as they cross.

non_diegetic_music: N/A
```

- **編集メモ**: 7秒。影を画面の下半分に大きく。顔は見せない（次の25で「空を仰ぐ」まで引っ張る）。

### Scene 25 — 生きていこう

- **シーン名**: 生きていこう（Chorus 2）
- **秒数**: 8 秒
- **対応歌詞**: 生きていこう
- **参照画像ファイル名（アップロード順）**:
  1. `hope_25_live_on.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a wide shot from slightly below on the hill crest beneath the lone cherry tree, the young woman standing at the very crest with both arms spread wide and her face lifted into the sunrise, dress and jacket moving in the morning wind, the brass key swinging on its cord. She keeps the identity, hair, clothing and key of <Picture 1>. Her arms are already open at the start; she lifts them a few degrees higher and opens her palms to the sky, and her chin comes up until her face is fully toward the light. She holds the pose without moving her feet; only her clothing, hair and the key move. Her bob lifts at the back and one strand crosses her cheek. The key swings on its cord and catches the sun once as a bright small point at her collarbone. Below the crest the valley is full of morning mist, and the mist moves slowly toward the camera in a shallow layer, so the ground she stands on looks like the top of the world. Warm sunrise light floods the frame from the left, long shadows rake across the grass, and the tree's branches frame the upper edge. Thin cloud above her is lit pink-gold. The camera pulls out with small amplitude at slow speed, revealing more of the mist and the sky, then holds for the final second. Her eyes stay closed until the last beat, then open. No jumping, no dancing, no spinning.

overall_soundscape: Wind moving through grass and denim at the crest, the thin whistle of air past her ears, and the mist settling below. A single bird far off.

non_diegetic_music: N/A
```

- **編集メモ**: 8秒。ここが感情の頂点。カメラは引く（＝世界が広がる）。歌詞の「生きていこう」に目を開ける瞬間を合わせる。

### Scene E-1 — 希望の道（固定エンディング）

- **シーン名**: 希望の道（固定エンディング / Ending）
- **秒数**: 10 秒
- **対応歌詞**: （アウトロ／歌唱なし）
- **参照画像ファイル名（アップロード順）**:
  1. `hope_E1_ending.png` — Picture 1 / 開始フレーム
- **プロンプト**:

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Cinematic live-action photorealistic footage, soft 35mm film grain, matching <Picture 1>: a locked-off wide shot with an empty stone path in the foreground leading up over a hill crest into the sunrise, the upper half of the frame a vast pale gold sky left as negative space, a small controlled lens flare near the horizon. The camera does not move at all — no pan, no tilt, no zoom, no drift — so the composition holds like a photograph. The only movement is distant and small: a tiny figure walks away over the crest in the upper middle of the frame, growing no larger than a thumbnail, taking six or seven unhurried steps and passing out of sight beyond the ridge at around the seventh second. Thin clouds drift slowly across the upper sky from right to left, and the pale gold brightens slightly as the sun clears the ridge, so the negative space up top becomes a little more luminous without losing its emptiness. Grass at the edges of the path moves in a light wind and a few insects cross the low foreground. The lens flare shifts by a hair as the light changes but stays small and low. No text of any kind appears at any point, and the upper half of the frame stays clean and empty for a title to be added later. The final frame holds the empty path and the bright sky.

overall_soundscape: A soft open-air ambience: light wind through grass, distant birds, and the last faint footsteps fading over the crest. Very quiet, with air moving past the microphone.

non_diegetic_music: N/A
```

- **編集メモ**: 10秒。完全固定。タイトルは編集で上半分に載せる（生成側で文字を描かせない）。最後は2秒ほど空のまま余韻を残す。

## 3. 生成と検収の手順

- **手順1**: `hope_refs.csv` → 参照画像7枚（4000–4600）。`hope_ref_02_character-sheet` の顔が決まるまで他を進めない。
- **手順2**: `scenes.csv` → 静止画26枚（1000–3500）。Scene 06 と Scene 23 は構図を揃え、23 は 06 の静止画を img2img の初期画像にして位置と倍率を固定する。
- **手順3**: 各静止画を確認する。`no text` が守られているか、人物が一人か、CS1 の顔が一致しているか。
- **手順4**: このファイルの26ブロックを H3 に投入する（1ブロック＝静止画1枚＋プロンプト全文）。尺は各ブロックの「秒数」をそのまま使う。
- **手順5**: クリップ確認の観点 — 動きすぎ（走る・跳ねる・大げさに振り向く）なら `does not` 文を強調して再生成。Scene 06 でつぼみが開いたら `the bud must not open` を先頭へ。Scene 05・17 の光が強すぎるなら `halation` の記述を弱める。手のカット（04・16・20）は2回に1回は崩れる前提で多めに引く。
- **手順6**: 検収は `python <skills>/media/music-video-production/scripts/check_mv_assets.py . --prefix hope_ --song-seconds 176`。このスクリプトは参照CSVを `uk_refs.csv` の名前で探すため、検収時のみ一時ディレクトリに `hope_refs.csv` を `uk_refs.csv` としてコピーして実行する。
- **手順7**: 動画ツール用の一覧表 `movies.yaml`（`id / name / duration / ref-image1..3 / prompt / lyrics`）は `python <skills>/media/music-video-production/scripts/gen_movies_table.py .` でこのファイルから生成する。`prompt` は `|-` のブロックで本ファイルと一字一句同一、`id` は `"01"` の文字列で出る。
- **手順8**: 編集で176秒に合わせてトリムし、歌を載せる。字幕は Scene 22 以降のみ画面下12%に小さく入れる。

## 4. 出典・準拠

- プロンプト方言: `h3-prompt-writing` スキルの `base-en.txt`（I2VA の定型文・カメラ語彙・soundscape 規約）と `ref-en.txt`（Ref2VA 6節・`<Subject N>` / `<Picture N>` の使い分け）。
- 制作手順: `music-video-production` スキル（Stage 1–6）と `references/file-templates.md`。
- 画像生成: ComfyUI `qwen_image_2_1_t2i.json`（Qwen Image 2.1 / 25 steps / cfg 1 / euler-simple / 16:9 1MP）。
- 楽曲: 「希望の道」（自作詞）。歌詞は本プロジェクトの `plan.md` §3 に対応表として収録。
