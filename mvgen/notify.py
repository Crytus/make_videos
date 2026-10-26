"""生成完了の通知（Windows トースト / Webhook）。"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request

# Windows PowerShell 5.1 の AppUserModelID（トーストの送信元として使う）
_PS_APP_ID = r"{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe"

_TOAST_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
$t = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
$texts = $t.GetElementsByTagName('text')
$texts.Item(0).AppendChild($t.CreateTextNode($env:MVGEN_TITLE)) > $null
$texts.Item(1).AppendChild($t.CreateTextNode($env:MVGEN_MESSAGE)) > $null
$n = [Windows.UI.Notifications.ToastNotification]::new($t)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($env:MVGEN_APPID).Show($n)
"""


def toast(title: str, message: str) -> None:
    """Windows のトースト通知を出す（WinRT が使える Windows PowerShell 5.1 経由）。"""
    if sys.platform != "win32":
        return
    env = {**os.environ, "MVGEN_TITLE": title, "MVGEN_MESSAGE": message, "MVGEN_APPID": _PS_APP_ID}
    subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", _TOAST_SCRIPT],
                   env=env, capture_output=True, timeout=30, check=True)


def webhook(url: str, message: str) -> None:
    """Discord（content）/ Slack（text）互換の JSON を POST する。"""
    body = json.dumps({"content": message, "text": message}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json",
                                                          "User-Agent": "mvgen"})
    with urllib.request.urlopen(req, timeout=15):
        pass


def notify(settings: dict, title: str, message: str) -> None:
    """設定に従って通知する。通知の失敗で処理全体は止めない。"""
    if settings.get("toast"):
        try:
            toast(title, message)
        except Exception as e:
            print(f"トースト通知に失敗しました: {e}", file=sys.stderr)
    if settings.get("webhook"):
        try:
            webhook(settings["webhook"], f"{title}\n{message}")
        except Exception as e:
            print(f"Webhook 通知に失敗しました: {e}", file=sys.stderr)
