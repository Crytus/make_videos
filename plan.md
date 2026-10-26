# ミュージックビデオ絵コンテ計画「希望の道」

楽曲: 希望の道（自作詞）/ シーン数: 26（Scene 01–25 ＋ 固定 E-1）/ 尺: 約2分56秒（176秒）/ アスペクト比: 16:9 / 画像生成: Qwen Image 2.1 / 動画生成: MiniMax H3（I2VA）

正（source of truth）。`scenes.md` / `scenes.csv` / `hope_refs.csv` はこのファイルを機械的に解析して生成する。プロンプトを他のファイルで手直ししないこと。

---

## 1. 全体のビジュアル・コンセプト

- **舞台**: 日本の里山。細い石畳の道、棚田、杉林、木の柵、赤いポスト。夜明け前から朝日までの一日を、同じ道の上で4つの光（夜明け前の藍 → 朝の金 → 雨の灰 → 夕暮れの藍 → 星 → 夜明けの金）で通す。
- **色**: 藍（#1b2a4a）と淡い金（#e8b96a）の二色対比。差し色は真鍮の鍵と赤いポストだけ。雨パートだけ彩度を落とす。
- **物語の弧**: 夜明け前の誰もいない道 → 朝が来る → 胸の内に灯る光を解き放つ → つぼみ＝まだ名のない願い → 風にしなる → 涙と雨 → それでも顔を上げて立ち上がる → 誰も知らない扉を自分の鍵で開ける → 星が道しるべ → 振り返って笑う → つぼみが開く → 朝日の中を歩き出す。
- **描き分けの軸（3つの反復装置）**:
  1. **同じ形の石畳の道**を全カットで使い回す（形は変えず、光だけ変える）。
  2. **掌の中の小さな光**（Scene 04 → 05 → 13 → 20 → 25）。出すたびに少しずつ大きくなる。
  3. **自然のマクロカット**（露 → つぼみ → 雨粒 → 蔦 → 星 → 開花）。各セクションに1枚ずつ挟み、彼女の内面の鏡にする。
- **カメラ**: 人物は「歩く・登る・立ち上がる」の縦横の移動だけで感情を語る。手ぶれなし、ほぼ固定または一定速のトラッキング。ピントは常に浅く、光源（窓・空・鍵穴）に向かってハレーションを出す。
- **文字ゼロ方針**: 全プロンプトに `no text`／ネガティブに signage・logo・subtitle。歌詞字幕は編集で載せるため、画面内に文字を一切描かせない。E-1 の上半分はタイトル用の余白として空ける。

## 2. キャラクター設定（一貫性ブロック・英語固定文）

以下を **全シーンのプロンプトに一字一句変わらずコピー** する（`_build_plan.py` の CH / ST / JP / JPN / CS1 が実体）。

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

## 3. シーン ↔ 歌詞 対応表

| # | シーン名 | 曲構成 | 対応歌詞 | 尺目安 |
|---|---|---|---|---|
| 01 | 夜明け前の一本道 | Intro | （イントロ／歌唱なし） | 8s |
| 02 | 新しい朝が | Verse 1 | 新しい朝が | 6s |
| 03 | 窓を照らすよ | Verse 1 | 窓を照らすよ | 6s |
| 04 | 胸に秘めた光 | Verse 1 | 胸に秘めた光 | 6s |
| 05 | 解き放つ時 | Verse 1 | 解き放つ時 | 6s |
| 06 | 小さなつぼみ | Verse 2 | 小さなつぼみ | 6s |
| 07 | 夢を抱きしめ | Verse 2 | 夢を抱きしめ | 6s |
| 08 | 風に揺れても | Verse 2 | 風に揺れても | 6s |
| 09 | 顔上げて進む | Verse 2 | 顔上げて進む | 6s |
| 10 | 時には涙 | Chorus | 時には涙 | 7s |
| 11 | こぼれる日も | Chorus | こぼれる日も | 7s |
| 12 | それでも強く | Chorus | それでも強く | 7s |
| 13 | 立ち上がるから | Chorus | 立ち上がるから | 7s |
| 14 | 誰も知らない | Bridge | 誰も知らない | 7s |
| 15 | 未来の扉 | Bridge | 未来の扉 | 7s |
| 16 | 自分の手で | Bridge | 自分の手で | 7s |
| 17 | 開いていこう | Bridge | 開いていこう | 8s |
| 18 | 輝く星は | Verse 3 | 輝く星は | 6s |
| 19 | いつも見守る | Verse 3 | いつも見守る | 6s |
| 20 | 信じる心 | Verse 3 | 信じる心 | 6s |
| 21 | 道しるべだよ | Verse 3 | 道しるべだよ | 6s |
| 22 | 優しい笑顔 | Chorus 2 | 優しい笑顔 | 7s |
| 23 | 希望を咲かせ | Chorus 2 | 希望を咲かせ | 7s |
| 24 | 自分らしく | Chorus 2 | 自分らしく | 7s |
| 25 | 生きていこう | Chorus 2 | 生きていこう | 8s |
| E-1 | 希望の道（固定エンディング） | Ending | （アウトロ／歌唱なし） | 10s |

各 Verse / Chorus は歌詞1行につき1シーン。計25カット＋固定エンディング。尺は目安（実尺は楽曲に合わせて編集で詰める）。

---

## 4. シーン詳細

### Scene 01 — 夜明け前の一本道（Intro）

- **歌詞**: （イントロ／歌唱なし）
- **内容**: 夜明け前の谷。細い石畳の道が手前の木の柵から稜線の一本木へと続く。低く霧がたまり、地平線だけがうっすら白い。まだ誰もいない道——これから歩き出す一歩の予告。
- **カメラ/光**: ローアングルの引き、道の消失点を画面中央に固定。ほぼ静止のごくゆっくりしたプッシュイン。空のグラデーションが主役。
- **positive_prompt**:
  `cinematic wide establishing shot, low angle, an empty narrow stone-paved path curving between terraced rice fields toward a lone cherry tree on a hill crest before dawn, morning mist lying low in the valley, no people present, one small pale window light glimmering far down the path, the mist moving almost imperceptibly, deep indigo sky fading to pale silver at the horizon, cool blue hour with a single warm glint, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_01_location-path-dawn, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, ruts and footprints in the mud, wet reflections
- **seed**: 1000 / **file_name**: `hope_01_path_before_dawn.png` / **尺**: 8s

### Scene 02 — 新しい朝が（Verse 1）

- **歌詞**: 新しい朝が
- **内容**: 空だけのカット。雲の縁が金色に焼け、太陽が地平線の下から昇りはじめる。三羽の鳥が横切る。彼女はまだ映らない——「朝が来る」を先に描く。
- **カメラ/光**: 空を仰ぐ広角。層になった雲のディテール。雲の流れだけがわずかに動く。
- **positive_prompt**:
  `cinematic wide shot of a dawn sky over a Japanese valley, thin layered clouds igniting gold along their edges as the sun breaks below the horizon, no people present, three small birds crossing the frame, the mist far below turning pink, first direct sunrise light, gold rimming every cloud against a still-blue upper sky, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_01_location-path-dawn, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, aircraft, contrails, power lines, buildings
- **seed**: 1100 / **file_name**: `hope_02_new_morning_sky.png` / **尺**: 6s

### Scene 03 — 窓を照らすよ（Verse 1）

- **歌詞**: 窓を照らすよ
- **内容**: 小さな部屋。カーテンの隙間から長方形の朝光が伸び、木の床を横切る。彼女はベッドの端に腰かけ、裸足を光の中に置いて、その光を見ている。埃が光の帯の中を漂う。
- **カメラ/光**: ミディアム。窓の光の帯が画面を斜めに横切る構図。室内は沈めて光だけを明るく。
- **positive_prompt**:
  `cinematic medium shot inside a small Japanese room with cream curtains, a rectangle of morning sunlight falling across wooden floorboards and the end of a low bed, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, sitting on the edge of the bed in a loose side view, bare feet set down inside the rectangle of light, one hand resting on the mattress, watching the dust motes drift, hard warm window light with cool shadow filling the rest of the room, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_03_location-room-morning, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, cluttered room, television, wall posters, direct eye contact with camera
- **seed**: 1200 / **file_name**: `hope_03_window_light.png` / **尺**: 6s

### Scene 04 — 胸に秘めた光（Verse 1）

- **歌詞**: 胸に秘めた光
- **内容**: 両手のアップ。胸の前で手を包みこむと、指の隙間から小さな金色の光が漏れはじめる。真鍮の鍵が光に触れて鈍く光る。誰にも見せていない、内側の光。
- **カメラ/光**: マクロ、浅い被写界深度。指先にピント、背景は暗く落とす。
- **positive_prompt**:
  `cinematic macro close-up of two cupped hands held together at her chest, the small brass key on its dark cord resting inside the palms, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, her fingers slowly closing around a soft golden point of light that glows between the palms and leaks through the gaps, the glow brightening and dimming like a pulse, a single warm pooled light from within her hands, everything else falling into soft brown shadow, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, glowing eyes, energy beams, magic circles, lens flare across the face
- **seed**: 1300 / **file_name**: `hope_04_light_in_hands.png` / **尺**: 6s

### Scene 05 — 解き放つ時（Verse 1）

- **歌詞**: 解き放つ時
- **内容**: 彼女が両手を開くと、光の粒が掌から立ちのぼる。背後では古い木戸が開き、外の朝の光が土間に流れ込む。戸口に立つ彼女の輪郭が逆光で縁取られる。
- **カメラ/光**: ミディアム、戸口の外からの自然光で完全な逆光。手前を光の粒のボケが横切る。
- **positive_prompt**:
  `cinematic medium shot in the doorway of an old Japanese house with a sliding wooden door standing open behind her, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, opening both hands and letting scattered points of golden light rise and float upward past her shoulders, then stepping forward once onto the stone threshold, strong backlight from the open doorway rimming her hair and shoulders, the interior dark and warm, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_01_location-path-dawn, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, fire, smoke, sparks, explosion
- **seed**: 1400 / **file_name**: `hope_05_release_the_light.png` / **尺**: 6s

### Scene 06 — 小さなつぼみ（Verse 2）

- **歌詞**: 小さなつぼみ
- **内容**: 土手のマクロ。菜の花の群れの中に一輪だけ白い小さなつぼみ。朝露が玉になり、逆光でつぼみの縁が透ける。このつぼみは最後（Scene 23）でもう一度出てくる。
- **カメラ/光**: マクロ、ローアングル。前ボケに菜の花、奥は緑のボケ。開花前の形を固定。
- **positive_prompt**:
  `cinematic macro shot, low angle, a single closed pale bud on a slender green stem among wild mustard flowers on a grassy riverbank, no people present, the bud swaying slightly in a light breeze, dew gathering into beads along its petals, low morning backlight making the bud glow translucent, deep green bokeh behind, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_07_prop-key-bud, hope_ref_01_location-path-dawn, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, insects on the bud, torn petals, hands in frame, open flower
- **seed**: 1500 / **file_name**: `hope_06_small_bud.png` / **尺**: 6s

### Scene 07 — 夢を抱きしめ（Verse 2）

- **歌詞**: 夢を抱きしめ
- **内容**: 彼女がしゃがみこみ、つぼみを両手でそっと包む。目を閉じて、まだ名前のない願いを預けるように。前髪が頬に落ち、鍵が紐ごと揺れる。
- **カメラ/光**: ミディアムクローズ、目線の高さ。背景は草の緑ボケ。
- **positive_prompt**:
  `cinematic medium close-up at eye level on a grassy riverbank, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, crouching down and gently cupping a single pale bud in both hands, eyes closed, a faint smile, her bob falling forward over her cheek, the brass key swinging free beneath her collar, soft morning light across her cheek and the bud, a gentle flare in the top corner, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_07_prop-key-bud, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, picking the flower, torn petals, looking at camera
- **seed**: 1600 / **file_name**: `hope_07_holding_the_dream.png` / **尺**: 6s

### Scene 08 — 風に揺れても（Verse 2）

- **歌詞**: 風に揺れても
- **内容**: 突風。草が一斉に倒れ、髪とジャケットの裾が煽られる。彼女は踏ん張って立つ。つぼみも大きくしなるが、茎は折れない。
- **カメラ/光**: ミディアム、低めのアングル。風向きを画面の左→右で全カット統一する。
- **positive_prompt**:
  `cinematic medium shot, low angle, a strong gust flattening the riverbank grass and whipping the hem of her denim jacket sideways, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, standing with her weight braced, one forearm raised against the wind, hair blown across her face, eyes narrowed but open, the pale bud bending hard on its stem without breaking, silver-grey overcast light with a thin gold break in the clouds behind her, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_07_prop-key-bud, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, storm damage, broken plants, heavy rain, falling over
- **seed**: 1700 / **file_name**: `hope_08_bending_in_wind.png` / **尺**: 6s

### Scene 09 — 顔上げて進む（Verse 2）

- **歌詞**: 顔上げて進む
- **内容**: 彼女は顔を上げ、空を見て、石畳の道を歩き出す。後ろ姿から半身へ。白いスニーカーが石を踏む一歩。
- **カメラ/光**: 後方やや斜めからのトラッキング、腰の高さ。歩き出しに合わせてカメラも前へ。
- **positive_prompt**:
  `cinematic tracking medium shot from behind and slightly to the side, on the stone path between the rice terraces, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, lifting her chin to the sky, then walking forward, the white canvas sneakers meeting the stones one after another, her jacket swinging, sun breaking through behind her, long early shadows raking across the path, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_01_location-path-dawn, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, walking backwards, running, looking at camera
- **seed**: 1800 / **file_name**: `hope_09_chin_up_walk_on.png` / **尺**: 6s

### Scene 10 — 時には涙（Chorus）

- **歌詞**: 時には涙
- **内容**: 雨。横顔のクローズアップ。睫に水滴、頬に髪が貼りつき、一筋の涙がそばかすを伝って落ちる。瞳は閉じない。
- **カメラ/光**: 真横のエクストリームクローズ。涙にピント、背景の雨はボケの線。
- **positive_prompt**:
  `cinematic extreme close-up in profile in falling rain on a suburban street, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, standing perfectly still with wet hair strands stuck to her cheek, one tear sliding down over her freckles, eyes glassy but held open, blinking once against the rain, flat grey overcast light, cold and even, thin specular highlights on wet skin, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_06_location-rain-street, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, sobbing, open mouth crying, running makeup, hands covering face
- **seed**: 1900 / **file_name**: `hope_10_a_tear.png` / **尺**: 7s

### Scene 11 — こぼれる日も（Chorus）

- **歌詞**: こぼれる日も
- **内容**: 雨の歩道。傘を持たずに、肩を少し落として歩いていく全身。濡れたアスファルトに赤いポストと街灯が溶けて映る。
- **カメラ/光**: ワイド、横位置のロング。雨脚は斜め、反射で画面下半分が光る。
- **positive_prompt**:
  `cinematic wide shot of a rain-soaked suburban Japanese sidewalk with a red-painted mailbox and low street lamps, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, walking alone without an umbrella, shoulders slightly bowed, one hand closed around the cord of her brass key, passing the mirror-like puddles, dull rainy daylight with warm streetlamp reflections smeared across the wet asphalt, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_06_location-rain-street, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, umbrella in hand, crowd, dry pavement, smiling brightly
- **seed**: 2000 / **file_name**: `hope_11_walking_in_rain.png` / **尺**: 7s

### Scene 12 — それでも強く（Chorus）

- **歌詞**: それでも強く
- **内容**: 雨の中で顔を上げる。雲の裂け目から細い光の柱が一本、彼女の顔に落ちる。雨粒が光の中で銀色に光る。顎を引き、目は開いたまま。
- **カメラ/光**: ミディアムクローズ、正面やや下から。光の柱を画面の対角に通す。
- **positive_prompt**:
  `cinematic medium close-up, slightly low angle, standing in steady rain, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, raising her face into the rain as one narrow column of sunlight breaks through the clouds and lands on her face, water beading on her skin, her jaw setting, eyes steady and open, a single hard shaft of warm sunlight cutting through cold grey rain, silver droplets sparkling inside it, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_06_location-rain-street, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, sunny cloudless sky, rainbow, arms raised
- **seed**: 2100 / **file_name**: `hope_12_still_strong.png` / **尺**: 7s

### Scene 13 — 立ち上がるから（Chorus）

- **歌詞**: 立ち上がるから
- **内容**: 濡れた石畳にしゃがんでいた彼女が、膝に手をついて立ち上がる。足元の水たまりに空が映り、立ち上がるにつれて顔がフレームに入ってくる。雨は上がりかけ。
- **カメラ/光**: ローアングル、ほぼ固定。腰から顔へと構図が変わる。
- **positive_prompt**:
  `cinematic low-angle medium shot on wet stone paving just after the rain, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, pushing up from a crouch with one hand on her knee, water dripping from her jacket hem, rising until her face enters the frame, the pale sky reflected in the puddle beneath her sneakers, breaking after-rain light, wet surfaces throwing soft reflections upward, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_06_location-rain-street, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, falling down, sitting in mud, bruised body
- **seed**: 2200 / **file_name**: `hope_13_standing_up.png` / **尺**: 7s

### Scene 14 — 誰も知らない（Bridge）

- **歌詞**: 誰も知らない
- **内容**: 夕暮れ。苔むした石段が杉林の上へ登っていく。彼女の後ろ姿が中ほどに。片手を苔の石壁に添える。木々の隙間に最初の星。
- **カメラ/光**: 石段の下からの見上げるワイド。段数と高低差で「上ること」を見せる。
- **positive_prompt**:
  `cinematic wide shot from below, an old moss-covered stone staircase climbing into a cedar grove at dusk, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, seen from behind halfway up the steps, one hand flat on the mossy stone wall, climbing steadily without looking back, last warm sky light through the cedar trunks, the first stars faint above the trees, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_05_location-old-door, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, torii gate, temple building, tourists, electric light
- **seed**: 2300 / **file_name**: `hope_14_nobody_knows.png` / **尺**: 7s

### Scene 15 — 未来の扉（Bridge）

- **歌詞**: 未来の扉
- **内容**: 石段の突き当たりの古い木の扉。蔦が枠を這い、蝶番は錆びている。扉の隙間から細い暖色の光が漏れている。誰も知らない扉。
- **カメラ/光**: 正面のクローズ、扉を画面いっぱいに。光の筋にピント。
- **positive_prompt**:
  `cinematic close-up of an old weathered wooden door at the top of the mossy stone steps, ivy creeping across its frame and a rusted iron hinge, no people present, a thin seam of warm light escaping through the gap between door and frame, ivy leaves trembling in the evening wind, deep blue dusk behind, warm amber light leaking from the crack, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_05_location-old-door, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, modern door, doorknob, hardware, signplate, open door
- **seed**: 2400 / **file_name**: `hope_15_door_of_the_future.png` / **尺**: 7s

### Scene 16 — 自分の手で（Bridge）

- **歌詞**: 自分の手で
- **内容**: 手のアップ。胸元の鍵を紐から外し、錆びた鍵穴へ差し込む。指先に力が入り、鍵穴から漏れる光が指を照らす。
- **カメラ/光**: マクロ。鍵穴と指先にタイト、背景は扉の木目。
- **positive_prompt**:
  `cinematic macro close-up of a hand lifting the small brass key on its dark cord away from her chest and guiding it into the old iron keyhole, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, her fingertips finding the keyhole, pressing the key home, thumb and forefinger turning it a quarter turn with a small effort, warm amber light from inside the keyhole washing over her fingers, cold blue dusk on the back of the hand, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_05_location-old-door, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, gloves, modern key, padlock, keychain clutter
- **seed**: 2500 / **file_name**: `hope_16_with_my_own_hands.png` / **尺**: 7s

### Scene 17 — 開いていこう（Bridge）

- **歌詞**: 開いていこう
- **内容**: 鍵が回り、扉が内側へ開く。まぶしい夜明けの光が溢れ出し、彼女は敷居に立ってシルエットになる。光が杉の幹の間へこぼれていく。
- **カメラ/光**: ミディアムワイド、開く扉ごしの逆光。光が画面を白く飛ばす一瞬を作る。
- **positive_prompt**:
  `cinematic medium-wide shot looking through an old wooden door as it swings inward at the top of the stone steps, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, standing on the threshold in silhouette, the brass key still in her hand, the door opening to flood warm dawn light past her into the dark cedar corridor, blinding warm dawn light from beyond the door, everything in front of it falling to silhouette, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_05_location-old-door, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, door breaking, wood splinters, explosion, smoke
- **seed**: 2600 / **file_name**: `hope_17_open_it_up.png` / **尺**: 8s

### Scene 18 — 輝く星は（Verse 3）

- **歌詞**: 輝く星は
- **内容**: 夜の丘。一本木のシルエットの上に満天の星。天の川の淡い帯。谷の底に街の灯が震えている。草に露。
- **カメラ/光**: 大ワイド、ローアングル気味。木を画面左に寄せ、右上に天の川。
- **positive_prompt**:
  `cinematic wide shot of a hilltop at night, a lone cherry tree in silhouette at the left of frame, the faint band of the Milky Way across the upper right, no people present, dew on the grass catching starlight, the tree branches absolutely still, starlight and a thin crescent moon, deep blue-black sky, distant warm town lights far below, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_04_location-hilltop-stars, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, oversized moon, city skyline, light pollution wash, satellites
- **seed**: 2700 / **file_name**: `hope_18_the_stars.png` / **尺**: 6s

### Scene 19 — いつも見守る（Verse 3）

- **歌詞**: いつも見守る
- **内容**: 草の上に寝転び、星を見上げる彼女の顔アップ。瞳に星が点として映る。息がうっすら白い。髪が草に散る。
- **カメラ/光**: 真上からのクローズ（俯瞰）。空と顔だけで画面を作る。
- **positive_prompt**:
  `cinematic close-up from above, lying back in the grass under the lone tree and looking up at the sky, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, her eyes open wide and motionless, stars reflected as small white points in them, breath faintly visible, hair fanned out in the grass, one hand resting on the brass key, cool moonlight on her face with a faint warm rim from a lamp far below, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_04_location-hilltop-stars, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, bed, pillow, indoor ceiling, blanket
- **seed**: 2800 / **file_name**: `hope_19_always_watching.png` / **尺**: 6s

### Scene 20 — 信じる心（Verse 3）

- **歌詞**: 信じる心
- **内容**: 彼女は上体を起こし、胸の鍵に手のひらを当てる。掌の下から小さな光が脈打つように広がり、指の隙間から漏れる。Scene 04 と同じ光の、少しだけ大きくなった版。
- **カメラ/光**: ミディアムクローズ、正面。胸元にピント、顔はわずかにボケ。
- **positive_prompt**:
  `cinematic medium close-up at night, sitting upright in the grass beside the lone tree, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, pressing her palm flat over the brass key at her chest, a soft golden glow pulsing outward from under her hand and leaking through her fingers, hair lifting in a light night wind, the glow from her chest as the only warm source, cool starlight rimming her hair, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_04_location-hilltop-stars, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, magic runes, glowing lines on skin, sparks, floating particles everywhere
- **seed**: 2900 / **file_name**: `hope_20_believing_heart.png` / **尺**: 6s

### Scene 21 — 道しるべだよ（Verse 3）

- **歌詞**: 道しるべだよ
- **内容**: 俯瞰の超ワイド。石畳の道が谷へ向かって蛇行し、その線に沿って星のような小さな光が点々と灯っていく。彼女は道のいちばん上に小さく立っている。
- **カメラ/光**: 斜め上からの超ワイド、道のラインを画面の対角線に。
- **positive_prompt**:
  `cinematic extreme wide shot from high above, the stone-paved path winding down the dark hillside toward the valley, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, standing small at the top of the path with her back to camera, looking down its length as a dotted line of small star-like points of light ignites along the stones one by one, deep blue night with a chain of tiny warm lights tracing the path, town glow far below, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_04_location-hilltop-stars, hope_ref_01_location-path-dawn, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, rows of street lights, power lines, cars on roads, drone
- **seed**: 3000 / **file_name**: `hope_21_a_signpost.png` / **尺**: 6s

### Scene 22 — 優しい笑顔（Chorus 2）

- **歌詞**: 優しい笑顔
- **内容**: 夜明けの道。彼女は足を止め、肩ごしに振り返って、柔らかく笑う。朝日が頬と真鍮の鍵を同時に照らす。涙のあとはもう乾いている。
- **カメラ/光**: 後方からのミディアム。振り返りの瞬間にゆっくり寄る。
- **positive_prompt**:
  `cinematic medium shot from behind on the stone path at sunrise, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, pausing mid-step and turning her head back over her shoulder with a soft open smile, the morning light catching the edge of her face and the brass key, low warm sunrise on her face, cool blue still in the shadowed valley behind, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_01_location-path-dawn, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, sad expression, looking down, wide open mouth
- **seed**: 3100 / **file_name**: `hope_22_gentle_smile.png` / **尺**: 7s

### Scene 23 — 希望を咲かせ（Chorus 2）

- **歌詞**: 希望を咲かせ
- **内容**: Scene 06 とまったく同じ構図・同じ位置のつぼみが、いま開いている。花びらがほどけ、中心から金色の光の粒が立ちのぼる。露が一枚ずつ滑り落ちる。
- **カメラ/光**: Scene 06 と同構図のマクロ。位置・角度を一致させ、違いは開花だけ。
- **positive_prompt**:
  `cinematic macro shot in exactly the same framing and camera position as the earlier bud image on the grassy riverbank, no people present, the pale bud now blooming open as its petals unfold outward one by one, glittering golden motes rising from its centre into the backlit morning air, low morning backlight turning the open petals translucent, dew sliding off their edges, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_07_prop-key-bud, hope_ref_01_location-path-dawn, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, different flower species, wilted petals, insects, bouquet
- **seed**: 3200 / **file_name**: `hope_23_hope_blooms.png` / **尺**: 7s

### Scene 24 — 自分らしく（Chorus 2）

- **歌詞**: 自分らしく
- **内容**: 道を歩く後ろ姿。朝日が正面から当たり、長い影が手前の石畳へ伸びる。ジャケットの縁が金色に光り、空には鳥。
- **カメラ/光**: 後方ワイド、影を画面の下半分に大きく使う。
- **positive_prompt**:
  `cinematic wide shot from behind, walking away up the stone path straight into the low sunrise, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, walking with an easy stride and loose arms, her shadow stretching long toward the camera across the stones, the edges of her jacket glowing with rim light, sunrise directly ahead, strong warm rim light and one large soft lens flare low in frame, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_01_location-path-dawn, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, walking toward camera, face visible, running
- **seed**: 3300 / **file_name**: `hope_24_as_i_am.png` / **尺**: 7s

### Scene 25 — 生きていこう（Chorus 2）

- **歌詞**: 生きていこう
- **内容**: 丘の頂上、一本木の下。彼女は両手を大きく広げ、顔を上げて朝日を浴びる。足元の谷には朝霧。鍵が光を受けて揺れる。ここが着地点。
- **カメラ/光**: ワイド、やや見上げ。木の枝を画面上辺に、空を大きく取る。
- **positive_prompt**:
  `cinematic wide shot from slightly below on the hill crest beneath the lone cherry tree, a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, standing at the very crest with both arms spread wide and her face lifted into the sunrise, dress and jacket moving in the morning wind, the brass key swinging on its cord, full warm sunrise flooding the frame from the left, long shadows raking across the grass, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, references: reference sheets hope_ref_02_character-sheet, hope_ref_01_location-path-dawn, hope_ref_04_location-hilltop-stars, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, jumping, dancing, arms crossed, hands on hips
- **seed**: 3400 / **file_name**: `hope_25_live_on.png` / **尺**: 8s

### Scene E-1 — 希望の道（固定エンディング）（Ending）

- **歌詞**: （アウトロ／歌唱なし）
- **内容**: カメラは完全固定。手前の石畳の道が稜線へ続き、稜線の向こうへ小さな後ろ姿が歩き去っていく。空は淡い金色で、画面上半分はタイトル用の余白として空ける。フレアは地平線の低い位置だけ。
- **カメラ/光**: 固定ロング。動くのは人物と雲だけ。上部にタイトル用のネガティブスペースを大きく残す。
- **positive_prompt**:
  `cinematic locked-off wide shot, an empty stone path in the foreground leading up over a hill crest into the sunrise, the upper half of the frame a vast pale gold sky left as negative space for a title, no people present, a tiny distant figure walking away over the crest, small and featureless at that distance, thin clouds drifting slowly, low sunrise behind the crest, one small controlled lens flare near the horizon, warm haze, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, references: reference sheets hope_ref_01_location-path-dawn, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, readable text, rendered title, watermark, birds in the title area
- **seed**: 3500 / **file_name**: `hope_E1_ending.png` / **尺**: 10s

---

## 5. シーンの流れ（編集メモ）

| 区間 | シーン | 編集の意図 |
|---|---|---|
| 0:00–0:08 | 01 | 誰もいない道で始める。観客に「これから歩く」と予告する引き。 |
| 0:08–0:32 | 02–05 | 朝が来る→窓→掌の光→解き放つ。光の粒を掌から空へ受け渡す4カット。 |
| 0:32–0:56 | 06–09 | つぼみを挿入し、風でしならせ、最後に顔を上げて歩き出す。Verse 2 は「耐える」区間。 |
| 0:56–1:24 | 10–13 | 雨。彩度を落とし、雨音を上げる。13で立ち上がって彩度が戻る＝サビの解答。 |
| 1:24–1:53 | 14–17 | 石段→扉→鍵→開く。ここだけ画面を暗く保ち、17の光量で一気に白飛びさせる。 |
| 1:53–2:17 | 18–21 | 星空。カットを長めに取り、BGM を抜いて環境音だけにする。21で光の点線が道をなぞる。 |
| 2:17–2:46 | 22–25 | 夜明け。22の振り返りスマイルが感情の着地、23でつぼみが開き、24–25で歩き出す。 |
| 2:46–2:56 | E-1 | 固定。歩き去る小さな後ろ姿と、タイトル用の空。終止符は動かさずに打つ。 |

## 6. Qwen Image 2.1 実行メモ

- **ワークフロー**: `qwen_image_2_1_t2i.json`（UNET `qwen_image_2.1_int8_convrot` / CLIP `qwen3vl_8b_int8_convrot` / VAE `qwen_image_2.1_vae_bf16`）。KSampler は steps 25・cfg 1・euler / simple・denoise 1。
- **cfg 1 の注意**: cfg 1 ではネガティブプロンプトが実質無効。本ファイルの negative は 「cfg を上げる／img2img で回す」場合のための記録であり、t2i の初回生成では効かない。文字や余分な人物が出た場合はプロンプト側の `no text`・`no people present`・`crowd` で抑えるか、cfg 1.5–2.0 の別ワークフローで再生成する。
- **解像度**: ResolutionSelector 16:9 / 1MP（1152×648 相当）。動画の元解像度として十分。アップスケールする場合は 1920×1080 へ。
- **seed**: 1000 から +100 刻み（01=1000 … 25=3400、E-1=3500）。参照画像は 4000 から +100（4000–4600）。
- **生成順**: `hope_ref_*` → 人物が出るシーン → 人物の出ないシーン。参照画像を先に作らないと顔と道の形が定まらない。
- **単一ソース原則**: この plan.md を直し、`python _build_plan.py` → `python _gen_assets.py` の順で再生成する。`scenes.csv` を直接編集しない。
- **検収**: `python <skill>/scripts/check_mv_assets.py . --prefix hope_ --song-seconds 176`。

## 7. 参照画像（リファレンス）プロンプト

シーン生成より先に作る。合計7枚。人物の出ないプレートは `no people present` とネガティブで人を排除する。

### REF-01 — 道と谷の基本プレート（夜明け）

- **用途**: 全屋外シーンの親プレート。道の形・曲がり・段数を固定する
- **作画の要点**: すべての屋外カットの基準。石畳の道を手前左から画面奥の稜線へ抜けさせ、左手前に木の柵、右手前に赤いポスト、稜線に一本木を置く。位置関係を言葉で固定する。
- **positive_prompt**:
  `cinematic wide establishing shot, low angle, a narrow stone-paved path curving between terraced rice fields toward a lone cherry tree on the hill crest, a weathered wooden fence at the lower left, one red-painted roadside mailbox at the right edge of frame, morning mist lying in the valley, no people present, cool blue-hour light with a pale silver horizon, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, any person, animals, vehicles, power lines, legible signs
- **seed**: 4000 / **file_name**: `hope_ref_01_location-path-dawn.png`

### REF-02 — キャラクターシート（3面＋3表情）

- **用途**: 主人公の同一性基準。全シーンのキャラクターブロックを担保
- **作画の要点**: 正面・斜め・背面の全身3点と、無表情・微笑・目を閉じた微笑のバスト3点。ラベル・見出し・カラースウォッチ・補助線は禁止（文字化けの原因）。余白で区切る。
- **positive_prompt**:
  `character reference sheet, three full-body views of the same young woman side by side (front view, three-quarter view, back view), and beneath them three head-and-shoulder expressions (neutral, soft closed smile, eyes closed with a faint smile), a 19-year-old Japanese young woman with delicate East Asian facial features, a chin-length dark brown bob with a soft side part, large clear brown eyes, fair skin and a light scattering of freckles across her nose, wearing a faded indigo denim jacket over a cream cotton dress, scuffed white canvas sneakers and a small brass key hanging on a thin dark cord at her chest, even soft studio light, no strong shadow, a seamless warm cream studio backdrop with wide empty margins on all sides, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, the same young woman as in every scene, identical face, identical chin-length bob, identical denim jacket and cream dress, identical brass key on its cord, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, labels, text, annotation lines, colour swatches, grids, border frames, second woman
- **seed**: 4100 / **file_name**: `hope_ref_02_character-sheet.png`

### REF-03 — 彼女の部屋（朝）

- **用途**: 室内カット（Scene 03・05）の場所基準
- **作画の要点**: クリーム色のカーテン、木の床、低いベッド、古い柱。窓は画面左。人物なし。
- **positive_prompt**:
  `cinematic medium-wide shot inside a small old Japanese room, cream curtains on a window at the left, worn wooden floorboards, a low bed with a folded quilt, a dark wooden post, a rectangle of morning sunlight lying across the floor, no people present, hard warm morning window light, cool shadow filling the room, a small Japanese house interior, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, any person, modern furniture, television, posters, clutter
- **seed**: 4200 / **file_name**: `hope_ref_03_location-room-morning.png`

### REF-04 — 丘の上の一本木（夜）

- **用途**: 夜の丘カット（Scene 18・19・20）の場所基準
- **作画の要点**: 一本木を画面左、天の川を右上、谷の灯を下部に。人物なし。空の濃さと星の密度を固定。
- **positive_prompt**:
  `cinematic wide shot of a hilltop at night, a lone cherry tree in silhouette at the left of frame, the faint band of the Milky Way across the upper right, warm town lights far down the valley, no people present, starlight and a thin crescent moon, no artificial light on the hill, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, any person, oversized moon, city skyline, light pollution wash
- **seed**: 4300 / **file_name**: `hope_ref_04_location-hilltop-stars.png`

### REF-05 — 苔むした石段と古い扉（夕暮れ）

- **用途**: Bridge の場所基準（Scene 14・15・16・17）
- **作画の要点**: 石段の段数と幅、扉の板の枚数・蔦の位置・錆びた蝶番を固定。明るさは「隙間の光だけ」。人物なし。
- **positive_prompt**:
  `cinematic shot from below of an old moss-covered stone staircase climbing into a cedar grove at dusk, ending at a weathered wooden door overgrown with ivy, a rusted iron hinge, a thin seam of warm light escaping through the crack of the door, no people present, deep blue dusk, warm amber only from the door crack, set in the same rural Japanese satoyama landscape at night, cedar groves and terraced fields in deep indigo silhouette, distant town lights trembling along the valley floor, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, any person, torii gate, temple architecture, modern door, doorknob
- **seed**: 4400 / **file_name**: `hope_ref_05_location-old-door.png`

### REF-06 — 雨の歩道とバス停

- **用途**: 雨パート（Scene 10・11・12・13）の場所基準
- **作画の要点**: 濡れたアスファルト、赤いポスト、低い街灯、水たまりの反射角。人物なし。雨の斜度も固定。
- **positive_prompt**:
  `cinematic wide shot of a rain-soaked suburban Japanese sidewalk, a red-painted mailbox and low street lamps, mirror-like puddles reflecting the grey sky, rain streaking diagonally, no people present, flat grey overcast daylight with warm lamp reflections in the water, set in a quiet rural Japanese satoyama landscape of narrow stone-paved paths between terraced rice fields, cedar groves, weathered wooden fences and a single red-painted roadside mailbox, morning mist lying in the valley, no legible signage anywhere, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, any person, umbrellas, cars, dry pavement
- **seed**: 4500 / **file_name**: `hope_ref_06_location-rain-street.png`

### REF-07 — 真鍮の鍵と一輪のつぼみ

- **用途**: マクロの反復装置（Scene 06・07・08・23）の物撮り基準
- **作画の要点**: 物語の二人の小道具を1枚に。鍵は紐付きで左、つぼみはガラス小瓶に一輪だけ右。開花前の形を固定し、Scene 23 の開花カットはこの形状を保ったまま花びらだけ開かせる。
- **positive_prompt**:
  `studio macro photograph on a plain warm cream background, a small tarnished brass key on a thin dark cord at the left, and a single closed pale bud in a small glass jar of water at the right, soft directional light, no people present, soft window-like side light, gentle shadow under the jar, wide empty cream margins with no labels or props, cinematic live-action photorealistic photography, soft 35mm film grain, gentle halation around light sources, warm amber and pale gold highlights against deep indigo shadows, shallow depth of field, natural skin texture, 16:9, no text`
- **negative_prompt**: text, letters, numbers, signage, logo, watermark, subtitle overlay, extra people, crowd, a second person, deformed hands, extra fingers, missing fingers, different face, different hairstyle, different outfit, duplicate subject, cartoon, anime, illustration, oversaturated colour, lowres, blurry, warped horizon, any person, hands, multiple flowers, jewellery, text
- **seed**: 4600 / **file_name**: `hope_ref_07_prop-key-bud.png`

---

## 8. 参照画像の運用（シーン別マッピング）

| シーン | 参照する基準画像 | 一致させる要素 |
|---|---|---|
| 01 夜明け前の一本道 | hope_ref_01_location-path-dawn（REF-01） | 場所の形のみ |
| 02 新しい朝が | hope_ref_01_location-path-dawn（REF-01） | 場所の形のみ |
| 03 窓を照らすよ | hope_ref_02_character-sheet（REF-02）、hope_ref_03_location-room-morning（REF-03） | 人物の同一性／室内レイアウト |
| 04 胸に秘めた光 | hope_ref_02_character-sheet（REF-02） | 人物の同一性 |
| 05 解き放つ時 | hope_ref_02_character-sheet（REF-02）、hope_ref_01_location-path-dawn（REF-01） | 人物の同一性 |
| 06 小さなつぼみ | hope_ref_07_prop-key-bud（REF-07）、hope_ref_01_location-path-dawn（REF-01） | 場所の形のみ／つぼみと鍵の形状 |
| 07 夢を抱きしめ | hope_ref_02_character-sheet（REF-02）、hope_ref_07_prop-key-bud（REF-07） | 人物の同一性／つぼみと鍵の形状 |
| 08 風に揺れても | hope_ref_02_character-sheet（REF-02）、hope_ref_07_prop-key-bud（REF-07） | 人物の同一性／つぼみと鍵の形状 |
| 09 顔上げて進む | hope_ref_02_character-sheet（REF-02）、hope_ref_01_location-path-dawn（REF-01） | 人物の同一性 |
| 10 時には涙 | hope_ref_02_character-sheet（REF-02）、hope_ref_06_location-rain-street（REF-06） | 人物の同一性／雨と濡れた地面の反射 |
| 11 こぼれる日も | hope_ref_02_character-sheet（REF-02）、hope_ref_06_location-rain-street（REF-06） | 人物の同一性／雨と濡れた地面の反射 |
| 12 それでも強く | hope_ref_02_character-sheet（REF-02）、hope_ref_06_location-rain-street（REF-06） | 人物の同一性／雨と濡れた地面の反射 |
| 13 立ち上がるから | hope_ref_02_character-sheet（REF-02）、hope_ref_06_location-rain-street（REF-06） | 人物の同一性／雨と濡れた地面の反射 |
| 14 誰も知らない | hope_ref_02_character-sheet（REF-02）、hope_ref_05_location-old-door（REF-05） | 人物の同一性／石段と扉の形状 |
| 15 未来の扉 | hope_ref_05_location-old-door（REF-05） | 場所の形のみ／石段と扉の形状 |
| 16 自分の手で | hope_ref_02_character-sheet（REF-02）、hope_ref_05_location-old-door（REF-05） | 人物の同一性／石段と扉の形状 |
| 17 開いていこう | hope_ref_02_character-sheet（REF-02）、hope_ref_05_location-old-door（REF-05） | 人物の同一性／石段と扉の形状 |
| 18 輝く星は | hope_ref_04_location-hilltop-stars（REF-04） | 場所の形のみ／星空と一本木の位置 |
| 19 いつも見守る | hope_ref_02_character-sheet（REF-02）、hope_ref_04_location-hilltop-stars（REF-04） | 人物の同一性／星空と一本木の位置 |
| 20 信じる心 | hope_ref_02_character-sheet（REF-02）、hope_ref_04_location-hilltop-stars（REF-04） | 人物の同一性／星空と一本木の位置 |
| 21 道しるべだよ | hope_ref_02_character-sheet（REF-02）、hope_ref_04_location-hilltop-stars（REF-04）、hope_ref_01_location-path-dawn（REF-01） | 人物の同一性／星空と一本木の位置 |
| 22 優しい笑顔 | hope_ref_02_character-sheet（REF-02）、hope_ref_01_location-path-dawn（REF-01） | 人物の同一性 |
| 23 希望を咲かせ | hope_ref_07_prop-key-bud（REF-07）、hope_ref_01_location-path-dawn（REF-01） | 場所の形のみ／つぼみと鍵の形状 |
| 24 自分らしく | hope_ref_02_character-sheet（REF-02）、hope_ref_01_location-path-dawn（REF-01） | 人物の同一性 |
| 25 生きていこう | hope_ref_02_character-sheet（REF-02）、hope_ref_01_location-path-dawn（REF-01）、hope_ref_04_location-hilltop-stars（REF-04） | 人物の同一性／星空と一本木の位置 |
| E-1 希望の道（固定エンディング） | hope_ref_01_location-path-dawn（REF-01） | 場所の形のみ |

追記ルール（5点・厳守）:

1. **CH / JP（または JP-N）/ ST / CS1 は一字一句そのまま**。短縮・言い換え禁止。
2. **CS1 は人物が出るシーンだけ**。人物の出ないカットは `no people present` に置き換える。
3. **`references: reference sheets <file>`** の行を必ず末尾近くに置く（`_gen_assets.py` と検収スクリプトがこれを見る）。
4. **末尾は必ず `16:9, no text`**。
5. 参照画像はクリップ1本につき**シーン静止画＋補助2枚まで**。3枚を超えると H3 がパレットを混ぜる。
