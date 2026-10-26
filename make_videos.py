"""movies.yaml を読み込み、ローカルの ComfyUI（MiniMax H3）で各クリップの動画を生成する。

使い方は README.md を参照。設定は config.yaml。

  python make_videos.py [generate] [オプション]   動画を生成（既定のコマンド）
  python make_videos.py status                     生成状況を一覧表示
  python make_videos.py review [--serve]           確認用の review.html を作る
  python make_videos.py roughcut                   全クリップをつないだラフ版を作る
"""

import sys

from mvgen.cli import main

if __name__ == "__main__":
    sys.exit(main())
