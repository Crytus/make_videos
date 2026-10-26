# 希望の道 — シーン表（画像生成用）

全 26 カット（01–25 ＋ 固定 E-1）＋ 参照画像 7 枚。プロンプトの正は `plan.md`。このファイルは `_gen_assets.py` が plan.md から生成した出力であり、手で直さない。

## 0. 使い方

1. `hope_refs.csv` で参照画像7枚を先に生成する（道 → 人物 → 部屋・丘・扉・雨 → 物撮り）。
2. `hope_ref_02_character-sheet` をキャラクター参照として固定し、人物カットを生成する。
3. `scenes.csv` を batch に流す。プロンプトは1行1シーンで完結している。
4. 生成順は `scenes.csv` の並び（=編集順）でよい。人物の出ないカットは参照プレートだけで作れる。
5. 出来た PNG はこのディレクトリ直下に `file_name` の名前で置く（`movies.md` の開始フレーム指定と一致させる）。

**重要**: `scenes.csv` / この md を直接編集しない。`plan.md` → `python _build_plan.py` → `python _gen_assets.py` の順で再生成する。

## 1. 固定ブロック（plan.md と同一文・変更禁止）

### CH — 主人公（固定ブロック）

> a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest

### ST — スタイル固定ブロック

> cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture

### JP — 世界観固定ブロック（昼・夜明け）

> set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere

### JP-N — 世界観固定ブロック（夜・夕暮れ。例外表記）

> set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere

### 一貫性宣言文（CS1・人物が出るシーンのみ）

> the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord

### ネガティブプロンプト共有ベース

> text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon

※ 人物の出ないカット（01・02・06・15・18・23・E-1）は CH と CS1 を `no people present` に置き換える。`crowd` と `a second person` は常時必須（一人芝居の作品なので、もう一人現れた時点で失敗）。

---

## 2. 参照画像一覧

| ID | file_name | 用途 |
|---|---|---|
| REF-01 | `hope_ref_01_location-path-dawn.png` | 全屋外シーンの親プレート。道の形・曲がり・段数を固定する |
| REF-02 | `hope_ref_02_character-sheet.png` | 主人公の同一性基準。全シーンのキャラクターブロックを担保 |
| REF-03 | `hope_ref_03_location-room-morning.png` | 室内カット（Scene 03・05）の場所基準 |
| REF-04 | `hope_ref_04_location-hilltop-stars.png` | 夜の丘カット（Scene 18・19・20）の場所基準 |
| REF-05 | `hope_ref_05_location-old-door.png` | Bridge の場所基準（Scene 14・15・16・17） |
| REF-06 | `hope_ref_06_location-rain-street.png` | 雨パート（Scene 10・11・12・13）の場所基準 |
| REF-07 | `hope_ref_07_prop-key-bud.png` | マクロの反復装置（Scene 06・07・08・23）の物撮り基準 |

## 3. シーン一覧

| # | シーン名 | 曲構成 | 対応歌詞 | seed | file_name | 尺 |
|—|—|—|—|—|—|—|
| 01 | 夜明け前の一本道 | Intro | （イントロ／歌唱なし） | 1000 | `hope_01_path_before_dawn.png` | 8s |
| 02 | 新しい朝が | Verse 1 | 新しい朝が | 1100 | `hope_02_new_morning_sky.png` | 6s |
| 03 | 窓を照らすよ | Verse 1 | 窓を照らすよ | 1200 | `hope_03_window_light.png` | 6s |
| 04 | 胸に秘めた光 | Verse 1 | 胸に秘めた光 | 1300 | `hope_04_light_in_hands.png` | 6s |
| 05 | 解き放つ時 | Verse 1 | 解き放つ時 | 1400 | `hope_05_release_the_light.png` | 6s |
| 06 | 小さなつぼみ | Verse 2 | 小さなつぼみ | 1500 | `hope_06_small_bud.png` | 6s |
| 07 | 夢を抱きしめ | Verse 2 | 夢を抱きしめ | 1600 | `hope_07_holding_the_dream.png` | 6s |
| 08 | 風に揺れても | Verse 2 | 風に揺れても | 1700 | `hope_08_bending_in_wind.png` | 6s |
| 09 | 顔上げて進む | Verse 2 | 顔上げて進む | 1800 | `hope_09_chin_up_walk_on.png` | 6s |
| 10 | 時には涙 | Chorus | 時には涙 | 1900 | `hope_10_a_tear.png` | 7s |
| 11 | こぼれる日も | Chorus | こぼれる日も | 2000 | `hope_11_walking_in_rain.png` | 7s |
| 12 | それでも強く | Chorus | それでも強く | 2100 | `hope_12_still_strong.png` | 7s |
| 13 | 立ち上がるから | Chorus | 立ち上がるから | 2200 | `hope_13_standing_up.png` | 7s |
| 14 | 誰も知らない | Bridge | 誰も知らない | 2300 | `hope_14_nobody_knows.png` | 7s |
| 15 | 未来の扉 | Bridge | 未来の扉 | 2400 | `hope_15_door_of_the_future.png` | 7s |
| 16 | 自分の手で | Bridge | 自分の手で | 2500 | `hope_16_with_my_own_hands.png` | 7s |
| 17 | 開いていこう | Bridge | 開いていこう | 2600 | `hope_17_open_it_up.png` | 8s |
| 18 | 輝く星は | Verse 3 | 輝く星は | 2700 | `hope_18_the_stars.png` | 6s |
| 19 | いつも見守る | Verse 3 | いつも見守る | 2800 | `hope_19_always_watching.png` | 6s |
| 20 | 信じる心 | Verse 3 | 信じる心 | 2900 | `hope_20_believing_heart.png` | 6s |
| 21 | 道しるべだよ | Verse 3 | 道しるべだよ | 3000 | `hope_21_a_signpost.png` | 6s |
| 22 | 優しい笑顔 | Chorus 2 | 優しい笑顔 | 3100 | `hope_22_gentle_smile.png` | 7s |
| 23 | 希望を咲かせ | Chorus 2 | 希望を咲かせ | 3200 | `hope_23_hope_blooms.png` | 7s |
| 24 | 自分らしく | Chorus 2 | 自分らしく | 3300 | `hope_24_as_i_am.png` | 7s |
| 25 | 生きていこう | Chorus 2 | 生きていこう | 3400 | `hope_25_live_on.png` | 8s |
| E-1 | 希望の道 | 固定エンディング）（Ending | （アウトロ／歌唱なし） | 3500 | `hope_E1_ending.png` | 10s |

## 4. シーン詳細

### Scene 01 — 夜明け前の一本道

- **シーン名**: 夜明け前の一本道
- **曲構成**: Intro
- **対応歌詞**: （イントロ／歌唱なし）
- **シーン説明**: 夜明け前の谷。細い石畳の道が手前の木の柵から稜線の一本木へと続く。低く霧がたまり、地平線だけがうっすら白い。まだ誰もいない道——これから歩き出す一歩の予告。
- **カメラ・光**: ローアングルの引き、道の消失点を画面中央に固定。ほぼ静止のごくゆっくりしたプッシュイン。空のグラデーションが主役。
- **参照画像**: hope_ref_01_location
- **seed**: 1000
- **file_name**: `hope_01_path_before_dawn.png`
- **尺**: 8s
- **positive_prompt**:

```text
cinematic wide establishing shot, low angle, an empty narrow stone-paved path curving between terraced rice fields toward a lone cherry tree on a hill crest before dawn, morning mist lying low in the valley, no people present, one small pale window light glimmering far down the path, the mist moving almost imperceptibly, deep indigo sky fading to pale silver at the horizon, cool blue hour with a single warm glint, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_01_location-path-dawn, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, ruts and footprints in the mud, wet reflections
```

### Scene 02 — 新しい朝が

- **シーン名**: 新しい朝が
- **曲構成**: Verse 1
- **対応歌詞**: 新しい朝が
- **シーン説明**: 空だけのカット。雲の縁が金色に焼け、太陽が地平線の下から昇りはじめる。三羽の鳥が横切る。彼女はまだ映らない——「朝が来る」を先に描く。
- **カメラ・光**: 空を仰ぐ広角。層になった雲のディテール。雲の流れだけがわずかに動く。
- **参照画像**: hope_ref_01_location
- **seed**: 1100
- **file_name**: `hope_02_new_morning_sky.png`
- **尺**: 6s
- **positive_prompt**:

```text
cinematic wide shot of a dawn sky over a Japanese valley, thin layered clouds igniting gold along their edges as the sun breaks below the horizon, no people present, three small birds crossing the frame, the mist far below turning pink, first direct sunrise light, gold rimming every cloud against a still-blue upper sky, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_01_location-path-dawn, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, aircraft, contrails, power lines, buildings
```

### Scene 03 — 窓を照らすよ

- **シーン名**: 窓を照らすよ
- **曲構成**: Verse 1
- **対応歌詞**: 窓を照らすよ
- **シーン説明**: 小さな部屋。カーテンの隙間から長方形の朝光が伸び、木の床を横切る。彼女はベッドの端に腰かけ、裸足を光の中に置いて、その光を見ている。埃が光の帯の中を漂う。
- **カメラ・光**: ミディアム。窓の光の帯が画面を斜めに横切る構図。室内は沈めて光だけを明るく。
- **参照画像**: hope_ref_02_character, hope_ref_03_location
- **seed**: 1200
- **file_name**: `hope_03_window_light.png`
- **尺**: 6s
- **positive_prompt**:

```text
cinematic medium shot inside a small Japanese room with cream curtains, a rectangle of morning sunlight falling across wooden floorboards and the end of a low bed, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, sitting on the edge of the bed in a loose side view, bare feet set down inside the rectangle of light, one hand resting on the mattress, watching the dust motes drift, hard warm window light with cool shadow filling the rest of the room, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_03_location-room-morning, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, cluttered room, television, wall posters, direct eye contact with camera
```

### Scene 04 — 胸に秘めた光

- **シーン名**: 胸に秘めた光
- **曲構成**: Verse 1
- **対応歌詞**: 胸に秘めた光
- **シーン説明**: 両手のアップ。胸の前で手を包みこむと、指の隙間から小さな金色の光が漏れはじめる。真鍮の鍵が光に触れて鈍く光る。誰にも見せていない、内側の光。
- **カメラ・光**: マクロ、浅い被写界深度。指先にピント、背景は暗く落とす。
- **参照画像**: hope_ref_02_character
- **seed**: 1300
- **file_name**: `hope_04_light_in_hands.png`
- **尺**: 6s
- **positive_prompt**:

```text
cinematic macro close-up of two cupped hands held together at her chest, the small brass key on its dark cord resting inside the palms, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, her fingers slowly closing around a soft golden point of light that glows between the palms and leaks through the gaps, the glow brightening and dimming like a pulse, a single warm pooled light from within her hands, everything else falling into soft brown shadow, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, glowing eyes, energy beams, magic circles, lens flare across the face
```

### Scene 05 — 解き放つ時

- **シーン名**: 解き放つ時
- **曲構成**: Verse 1
- **対応歌詞**: 解き放つ時
- **シーン説明**: 彼女が両手を開くと、光の粒が掌から立ちのぼる。背後では古い木戸が開き、外の朝の光が土間に流れ込む。戸口に立つ彼女の輪郭が逆光で縁取られる。
- **カメラ・光**: ミディアム、戸口の外からの自然光で完全な逆光。手前を光の粒のボケが横切る。
- **参照画像**: hope_ref_02_character, hope_ref_01_location
- **seed**: 1400
- **file_name**: `hope_05_release_the_light.png`
- **尺**: 6s
- **positive_prompt**:

```text
cinematic medium shot in the doorway of an old Japanese house with a sliding wooden door standing open behind her, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, opening both hands and letting scattered points of golden light rise and float upward past her shoulders, then stepping forward once onto the stone threshold, strong backlight from the open doorway rimming her hair and shoulders, the interior dark and warm, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_01_location-path-dawn, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, fire, smoke, sparks, explosion
```

### Scene 06 — 小さなつぼみ

- **シーン名**: 小さなつぼみ
- **曲構成**: Verse 2
- **対応歌詞**: 小さなつぼみ
- **シーン説明**: 土手のマクロ。菜の花の群れの中に一輪だけ白い小さなつぼみ。朝露が玉になり、逆光でつぼみの縁が透ける。このつぼみは最後（Scene 23）でもう一度出てくる。
- **カメラ・光**: マクロ、ローアングル。前ボケに菜の花、奥は緑のボケ。開花前の形を固定。
- **参照画像**: hope_ref_07_prop, hope_ref_01_location
- **seed**: 1500
- **file_name**: `hope_06_small_bud.png`
- **尺**: 6s
- **positive_prompt**:

```text
cinematic macro shot, low angle, a single closed pale bud on a slender green stem among wild mustard flowers on a grassy riverbank, no people present, the bud swaying slightly in a light breeze, dew gathering into beads along its petals, low morning backlight making the bud glow translucent, deep green bokeh behind, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_07_prop-key-bud, hope_ref_01_location-path-dawn, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, insects on the bud, torn petals, hands in frame, open flower
```

### Scene 07 — 夢を抱きしめ

- **シーン名**: 夢を抱きしめ
- **曲構成**: Verse 2
- **対応歌詞**: 夢を抱きしめ
- **シーン説明**: 彼女がしゃがみこみ、つぼみを両手でそっと包む。目を閉じて、まだ名前のない願いを預けるように。前髪が頬に落ち、鍵が紐ごと揺れる。
- **カメラ・光**: ミディアムクローズ、目線の高さ。背景は草の緑ボケ。
- **参照画像**: hope_ref_02_character, hope_ref_07_prop
- **seed**: 1600
- **file_name**: `hope_07_holding_the_dream.png`
- **尺**: 6s
- **positive_prompt**:

```text
cinematic medium close-up at eye level on a grassy riverbank, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, crouching down and gently cupping a single pale bud in both hands, eyes closed, a faint smile, her bob falling forward over her cheek, the brass key swinging free beneath her collar, soft morning light across her cheek and the bud, a gentle flare in the top corner, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_07_prop-key-bud, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, picking the flower, torn petals, looking at camera
```

### Scene 08 — 風に揺れても

- **シーン名**: 風に揺れても
- **曲構成**: Verse 2
- **対応歌詞**: 風に揺れても
- **シーン説明**: 突風。草が一斉に倒れ、髪とジャケットの裾が煽られる。彼女は踏ん張って立つ。つぼみも大きくしなるが、茎は折れない。
- **カメラ・光**: ミディアム、低めのアングル。風向きを画面の左→右で全カット統一する。
- **参照画像**: hope_ref_02_character, hope_ref_07_prop
- **seed**: 1700
- **file_name**: `hope_08_bending_in_wind.png`
- **尺**: 6s
- **positive_prompt**:

```text
cinematic medium shot, low angle, a strong gust flattening the riverbank grass and whipping the hem of her denim jacket sideways, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, standing with her weight braced, one forearm raised against the wind, hair blown across her face, eyes narrowed but open, the pale bud bending hard on its stem without breaking, silver-grey overcast light with a thin gold break in the clouds behind her, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_07_prop-key-bud, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, storm damage, broken plants, heavy rain, falling over
```

### Scene 09 — 顔上げて進む

- **シーン名**: 顔上げて進む
- **曲構成**: Verse 2
- **対応歌詞**: 顔上げて進む
- **シーン説明**: 彼女は顔を上げ、空を見て、石畳の道を歩き出す。後ろ姿から半身へ。白いスニーカーが石を踏む一歩。
- **カメラ・光**: 後方やや斜めからのトラッキング、腰の高さ。歩き出しに合わせてカメラも前へ。
- **参照画像**: hope_ref_02_character, hope_ref_01_location
- **seed**: 1800
- **file_name**: `hope_09_chin_up_walk_on.png`
- **尺**: 6s
- **positive_prompt**:

```text
cinematic tracking medium shot from behind and slightly to the side, on the stone path between the rice terraces, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, lifting her chin to the sky, then walking forward, the white canvas sneakers meeting the stones one after another, her jacket swinging, sun breaking through behind her, long early shadows raking across the path, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_01_location-path-dawn, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, walking backwards, running, looking at camera
```

### Scene 10 — 時には涙

- **シーン名**: 時には涙
- **曲構成**: Chorus
- **対応歌詞**: 時には涙
- **シーン説明**: 雨。横顔のクローズアップ。睫に水滴、頬に髪が貼りつき、一筋の涙がそばかすを伝って落ちる。瞳は閉じない。
- **カメラ・光**: 真横のエクストリームクローズ。涙にピント、背景の雨はボケの線。
- **参照画像**: hope_ref_02_character, hope_ref_06_location
- **seed**: 1900
- **file_name**: `hope_10_a_tear.png`
- **尺**: 7s
- **positive_prompt**:

```text
cinematic extreme close-up in profile in falling rain on a suburban street, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, standing perfectly still with wet hair strands stuck to her cheek, one tear sliding down over her freckles, eyes glassy but held open, blinking once against the rain, flat grey overcast light, cold and even, thin specular highlights on wet skin, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_06_location-rain-street, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, sobbing, open mouth crying, running makeup, hands covering face
```

### Scene 11 — こぼれる日も

- **シーン名**: こぼれる日も
- **曲構成**: Chorus
- **対応歌詞**: こぼれる日も
- **シーン説明**: 雨の歩道。傘を持たずに、肩を少し落として歩いていく全身。濡れたアスファルトに赤いポストと街灯が溶けて映る。
- **カメラ・光**: ワイド、横位置のロング。雨脚は斜め、反射で画面下半分が光る。
- **参照画像**: hope_ref_02_character, hope_ref_06_location
- **seed**: 2000
- **file_name**: `hope_11_walking_in_rain.png`
- **尺**: 7s
- **positive_prompt**:

```text
cinematic wide shot of a rain-soaked suburban Japanese sidewalk with a red-painted mailbox and low street lamps, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, walking alone without an umbrella, shoulders slightly bowed, one hand closed around the cord of her brass key, passing the mirror-like puddles, dull rainy daylight with warm streetlamp reflections smeared across the wet asphalt, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_06_location-rain-street, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, umbrella in hand, crowd, dry pavement, smiling brightly
```

### Scene 12 — それでも強く

- **シーン名**: それでも強く
- **曲構成**: Chorus
- **対応歌詞**: それでも強く
- **シーン説明**: 雨の中で顔を上げる。雲の裂け目から細い光の柱が一本、彼女の顔に落ちる。雨粒が光の中で銀色に光る。顎を引き、目は開いたまま。
- **カメラ・光**: ミディアムクローズ、正面やや下から。光の柱を画面の対角に通す。
- **参照画像**: hope_ref_02_character, hope_ref_06_location
- **seed**: 2100
- **file_name**: `hope_12_still_strong.png`
- **尺**: 7s
- **positive_prompt**:

```text
cinematic medium close-up, slightly low angle, standing in steady rain, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, raising her face into the rain as one narrow column of sunlight breaks through the clouds and lands on her face, water beading on her skin, her jaw setting, eyes steady and open, a single hard shaft of warm sunlight cutting through cold grey rain, silver droplets sparkling inside it, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_06_location-rain-street, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, sunny cloudless sky, rainbow, arms raised
```

### Scene 13 — 立ち上がるから

- **シーン名**: 立ち上がるから
- **曲構成**: Chorus
- **対応歌詞**: 立ち上がるから
- **シーン説明**: 濡れた石畳にしゃがんでいた彼女が、膝に手をついて立ち上がる。足元の水たまりに空が映り、立ち上がるにつれて顔がフレームに入ってくる。雨は上がりかけ。
- **カメラ・光**: ローアングル、ほぼ固定。腰から顔へと構図が変わる。
- **参照画像**: hope_ref_02_character, hope_ref_06_location
- **seed**: 2200
- **file_name**: `hope_13_standing_up.png`
- **尺**: 7s
- **positive_prompt**:

```text
cinematic low-angle medium shot on wet stone paving just after the rain, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, pushing up from a crouch with one hand on her knee, water dripping from her jacket hem, rising until her face enters the frame, the pale sky reflected in the puddle beneath her sneakers, breaking after-rain light, wet surfaces throwing soft reflections upward, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_06_location-rain-street, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, falling down, sitting in mud, bruised body
```

### Scene 14 — 誰も知らない

- **シーン名**: 誰も知らない
- **曲構成**: Bridge
- **対応歌詞**: 誰も知らない
- **シーン説明**: 夕暮れ。苔むした石段が杉林の上へ登っていく。彼女の後ろ姿が中ほどに。片手を苔の石壁に添える。木々の隙間に最初の星。
- **カメラ・光**: 石段の下からの見上げるワイド。段数と高低差で「上ること」を見せる。
- **参照画像**: hope_ref_02_character, hope_ref_05_location
- **seed**: 2300
- **file_name**: `hope_14_nobody_knows.png`
- **尺**: 7s
- **positive_prompt**:

```text
cinematic wide shot from below, an old moss-covered stone staircase climbing into a cedar grove at dusk, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, seen from behind halfway up the steps, one hand flat on the mossy stone wall, climbing steadily without looking back, last warm sky light through the cedar trunks, the first stars faint above the trees, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_05_location-old-door, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, torii gate, temple building, tourists, electric light
```

### Scene 15 — 未来の扉

- **シーン名**: 未来の扉
- **曲構成**: Bridge
- **対応歌詞**: 未来の扉
- **シーン説明**: 石段の突き当たりの古い木の扉。蔦が枠を這い、蝶番は錆びている。扉の隙間から細い暖色の光が漏れている。誰も知らない扉。
- **カメラ・光**: 正面のクローズ、扉を画面いっぱいに。光の筋にピント。
- **参照画像**: hope_ref_05_location
- **seed**: 2400
- **file_name**: `hope_15_door_of_the_future.png`
- **尺**: 7s
- **positive_prompt**:

```text
cinematic close-up of an old weathered wooden door at the top of the mossy stone steps, ivy creeping across its frame and a rusted iron hinge, no people present, a thin seam of warm light escaping through the gap between door and frame, ivy leaves trembling in the evening wind, deep blue dusk behind, warm amber light leaking from the crack, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_05_location-old-door, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, modern door, doorknob, hardware, signplate, open door
```

### Scene 16 — 自分の手で

- **シーン名**: 自分の手で
- **曲構成**: Bridge
- **対応歌詞**: 自分の手で
- **シーン説明**: 手のアップ。胸元の鍵を紐から外し、錆びた鍵穴へ差し込む。指先に力が入り、鍵穴から漏れる光が指を照らす。
- **カメラ・光**: マクロ。鍵穴と指先にタイト、背景は扉の木目。
- **参照画像**: hope_ref_02_character, hope_ref_05_location
- **seed**: 2500
- **file_name**: `hope_16_with_my_own_hands.png`
- **尺**: 7s
- **positive_prompt**:

```text
cinematic macro close-up of a hand lifting the small brass key on its dark cord away from her chest and guiding it into the old iron keyhole, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, her fingertips finding the keyhole, pressing the key home, thumb and forefinger turning it a quarter turn with a small effort, warm amber light from inside the keyhole washing over her fingers, cold blue dusk on the back of the hand, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_05_location-old-door, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, gloves, modern key, padlock, keychain clutter
```

### Scene 17 — 開いていこう

- **シーン名**: 開いていこう
- **曲構成**: Bridge
- **対応歌詞**: 開いていこう
- **シーン説明**: 鍵が回り、扉が内側へ開く。まぶしい夜明けの光が溢れ出し、彼女は敷居に立ってシルエットになる。光が杉の幹の間へこぼれていく。
- **カメラ・光**: ミディアムワイド、開く扉ごしの逆光。光が画面を白く飛ばす一瞬を作る。
- **参照画像**: hope_ref_02_character, hope_ref_05_location
- **seed**: 2600
- **file_name**: `hope_17_open_it_up.png`
- **尺**: 8s
- **positive_prompt**:

```text
cinematic medium-wide shot looking through an old wooden door as it swings inward at the top of the stone steps, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, standing on the threshold in silhouette, the brass key still in her hand, the door opening to flood warm dawn light past her into the dark cedar corridor, blinding warm dawn light from beyond the door, everything in front of it falling to silhouette, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_05_location-old-door, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, door breaking, wood splinters, explosion, smoke
```

### Scene 18 — 輝く星は

- **シーン名**: 輝く星は
- **曲構成**: Verse 3
- **対応歌詞**: 輝く星は
- **シーン説明**: 夜の丘。一本木のシルエットの上に満天の星。天の川の淡い帯。谷の底に街の灯が震えている。草に露。
- **カメラ・光**: 大ワイド、ローアングル気味。木を画面左に寄せ、右上に天の川。
- **参照画像**: hope_ref_04_location
- **seed**: 2700
- **file_name**: `hope_18_the_stars.png`
- **尺**: 6s
- **positive_prompt**:

```text
cinematic wide shot of a hilltop at night, a lone cherry tree in silhouette at the left of frame, the faint band of the Milky Way across the upper right, no people present, dew on the grass catching starlight, the tree branches absolutely still, starlight and a thin crescent moon, deep blue-black sky, distant warm town lights far below, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_04_location-hilltop-stars, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, oversized moon, city skyline, light pollution wash, satellites
```

### Scene 19 — いつも見守る

- **シーン名**: いつも見守る
- **曲構成**: Verse 3
- **対応歌詞**: いつも見守る
- **シーン説明**: 草の上に寝転び、星を見上げる彼女の顔アップ。瞳に星が点として映る。息がうっすら白い。髪が草に散る。
- **カメラ・光**: 真上からのクローズ（俯瞰）。空と顔だけで画面を作る。
- **参照画像**: hope_ref_02_character, hope_ref_04_location
- **seed**: 2800
- **file_name**: `hope_19_always_watching.png`
- **尺**: 6s
- **positive_prompt**:

```text
cinematic close-up from above, lying back in the grass under the lone tree and looking up at the sky, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, her eyes open wide and motionless, stars reflected as small white points in them, breath faintly visible, hair fanned out in the grass, one hand resting on the brass key, cool moonlight on her face with a faint warm rim from a lamp far below, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_04_location-hilltop-stars, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, bed, pillow, indoor ceiling, blanket
```

### Scene 20 — 信じる心

- **シーン名**: 信じる心
- **曲構成**: Verse 3
- **対応歌詞**: 信じる心
- **シーン説明**: 彼女は上体を起こし、胸の鍵に手のひらを当てる。掌の下から小さな光が脈打つように広がり、指の隙間から漏れる。Scene 04 と同じ光の、少しだけ大きくなった版。
- **カメラ・光**: ミディアムクローズ、正面。胸元にピント、顔はわずかにボケ。
- **参照画像**: hope_ref_02_character, hope_ref_04_location
- **seed**: 2900
- **file_name**: `hope_20_believing_heart.png`
- **尺**: 6s
- **positive_prompt**:

```text
cinematic medium close-up at night, sitting upright in the grass beside the lone tree, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, pressing her palm flat over the brass key at her chest, a soft golden glow pulsing outward from under her hand and leaking through her fingers, hair lifting in a light night wind, the glow from her chest as the only warm source, cool starlight rimming her hair, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_04_location-hilltop-stars, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, magic runes, glowing lines on skin, sparks, floating particles everywhere
```

### Scene 21 — 道しるべだよ

- **シーン名**: 道しるべだよ
- **曲構成**: Verse 3
- **対応歌詞**: 道しるべだよ
- **シーン説明**: 俯瞰の超ワイド。石畳の道が谷へ向かって蛇行し、その線に沿って星のような小さな光が点々と灯っていく。彼女は道のいちばん上に小さく立っている。
- **カメラ・光**: 斜め上からの超ワイド、道のラインを画面の対角線に。
- **参照画像**: hope_ref_02_character, hope_ref_04_location, hope_ref_01_location
- **seed**: 3000
- **file_name**: `hope_21_a_signpost.png`
- **尺**: 6s
- **positive_prompt**:

```text
cinematic extreme wide shot from high above, the stone-paved path winding down the dark hillside toward the valley, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, standing small at the top of the path with her back to camera, looking down its length as a dotted line of small star-like points of light ignites along the stones one by one, deep blue night with a chain of tiny warm lights tracing the path, town glow far below, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_04_location-hilltop-stars, hope_ref_01_location-path-dawn, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, rows of street lights, power lines, cars on roads, drone
```

### Scene 22 — 優しい笑顔

- **シーン名**: 優しい笑顔
- **曲構成**: Chorus 2
- **対応歌詞**: 優しい笑顔
- **シーン説明**: 夜明けの道。彼女は足を止め、肩ごしに振り返って、柔らかく笑う。朝日が頬と真鍮の鍵を同時に照らす。涙のあとはもう乾いている。
- **カメラ・光**: 後方からのミディアム。振り返りの瞬間にゆっくり寄る。
- **参照画像**: hope_ref_02_character, hope_ref_01_location
- **seed**: 3100
- **file_name**: `hope_22_gentle_smile.png`
- **尺**: 7s
- **positive_prompt**:

```text
cinematic medium shot from behind on the stone path at sunrise, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, pausing mid-step and turning her head back over her shoulder with a soft open smile, the morning light catching the edge of her face and the brass key, low warm sunrise on her face, cool blue still in the shadowed valley behind, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_01_location-path-dawn, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, sad expression, looking down, wide open mouth
```

### Scene 23 — 希望を咲かせ

- **シーン名**: 希望を咲かせ
- **曲構成**: Chorus 2
- **対応歌詞**: 希望を咲かせ
- **シーン説明**: Scene 06 とまったく同じ構図・同じ位置のつぼみが、いま開いている。花びらがほどけ、中心から金色の光の粒が立ちのぼる。露が一枚ずつ滑り落ちる。
- **カメラ・光**: Scene 06 と同構図のマクロ。位置・角度を一致させ、違いは開花だけ。
- **参照画像**: hope_ref_07_prop, hope_ref_01_location
- **seed**: 3200
- **file_name**: `hope_23_hope_blooms.png`
- **尺**: 7s
- **positive_prompt**:

```text
cinematic macro shot in exactly the same framing and camera position as the earlier bud image on the grassy riverbank, no people present, the pale bud now blooming open as its petals unfold outward one by one, glittering golden motes rising from its centre into the backlit morning air, low morning backlight turning the open petals translucent, dew sliding off their edges, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_07_prop-key-bud, hope_ref_01_location-path-dawn, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, different flower species, wilted petals, insects, bouquet
```

### Scene 24 — 自分らしく

- **シーン名**: 自分らしく
- **曲構成**: Chorus 2
- **対応歌詞**: 自分らしく
- **シーン説明**: 道を歩く後ろ姿。朝日が正面から当たり、長い影が手前の石畳へ伸びる。ジャケットの縁が金色に光り、空には鳥。
- **カメラ・光**: 後方ワイド、影を画面の下半分に大きく使う。
- **参照画像**: hope_ref_02_character, hope_ref_01_location
- **seed**: 3300
- **file_name**: `hope_24_as_i_am.png`
- **尺**: 7s
- **positive_prompt**:

```text
cinematic wide shot from behind, walking away up the stone path straight into the low sunrise, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, walking with an easy stride and loose arms, her shadow stretching long toward the camera across the stones, the edges of her jacket glowing with rim light, sunrise directly ahead, strong warm rim light and one large soft lens flare low in frame, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_01_location-path-dawn, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, walking toward camera, face visible, running
```

### Scene 25 — 生きていこう

- **シーン名**: 生きていこう
- **曲構成**: Chorus 2
- **対応歌詞**: 生きていこう
- **シーン説明**: 丘の頂上、一本木の下。彼女は両手を大きく広げ、顔を上げて朝日を浴びる。足元の谷には朝霧。鍵が光を受けて揺れる。ここが着地点。
- **カメラ・光**: ワイド、やや見上げ。木の枝を画面上辺に、空を大きく取る。
- **参照画像**: hope_ref_02_character, hope_ref_01_location, hope_ref_04_location
- **seed**: 3400
- **file_name**: `hope_25_live_on.png`
- **尺**: 8s
- **positive_prompt**:

```text
cinematic wide shot from slightly below on the hill crest beneath the lone cherry tree, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, standing at the very crest with both arms spread wide and her face lifted into the sunrise, dress and jacket moving in the morning wind, the brass key swinging on its cord, full warm sunrise flooding the frame from the left, long shadows raking across the grass, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_01_location-path-dawn, hope_ref_04_location-hilltop-stars, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, jumping, dancing, arms crossed, hands on hips
```

### Scene E-1 — 希望の道

- **シーン名**: 希望の道
- **曲構成**: 固定エンディング）（Ending
- **対応歌詞**: （アウトロ／歌唱なし）
- **シーン説明**: カメラは完全固定。手前の石畳の道が稜線へ続き、稜線の向こうへ小さな後ろ姿が歩き去っていく。空は淡い金色で、画面上半分はタイトル用の余白として空ける。フレアは地平線の低い位置だけ。
- **カメラ・光**: 固定ロング。動くのは人物と雲だけ。上部にタイトル用のネガティブスペースを大きく残す。
- **参照画像**: hope_ref_01_location
- **seed**: 3500
- **file_name**: `hope_E1_ending.png`
- **尺**: 10s
- **positive_prompt**:

```text
cinematic locked-off wide shot, an empty stone path in the foreground leading up over a hill crest into the sunrise, the upper half of the frame a vast pale gold sky left as negative space for a title, no people present, a tiny distant figure walking away over the crest, small and featureless at that distance, thin clouds drifting slowly, low sunrise behind the crest, one small controlled lens flare near the horizon, warm haze, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_01_location-path-dawn, 16:9, no text
```

- **negative_prompt**:

```text
text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, readable text, rendered title, watermark, birds in the title area
```

## 5. 検収チェックリスト

- [ ] 全カットのプロンプトに CH（または `no people present`）・JP/JP-N・ST が入っている
- [ ] 人物カットだけに CS1 が入っている（人物の出ないカットに CS1 が残っていない）
- [ ] 全プロンプト末尾が `16:9, no text`
- [ ] `references: reference sheets ...` の行が全カットにある
- [ ] seed と file_name が全カット・全参照画像で一意
- [ ] 参照画像を先に生成し、`hope_ref_02_character-sheet` の顔が全カットで一致している
- [ ] Scene 23 の開花カットが Scene 06 と同じ構図・同じ位置になっている
- [ ] E-1 の画面上半分にタイトル用の余白が残っている
- [ ] 画面内に文字・看板・ロゴが描画されていない
