# Viewport Screenshot (VPS) for Maya

**Language:** [English](#english) | [日本語](#日本語)

[![Get Pro v1.2 on Gumroad](https://img.shields.io/badge/Get_Pro_v1.2-Gumroad_(Global)-ff90e8?style=for-the-badge&logo=gumroad&logoColor=black)](https://mashitaya.gumroad.com/l/ysgtzm/LAUNCH)
[![Get Pro v1.2 on BOOTH](https://img.shields.io/badge/Get_Pro_v1.2-BOOTH_(日本語)-fc4d50?style=for-the-badge)](https://yworks.booth.pm/items/9112055)
![Autodesk Maya](https://img.shields.io/badge/Autodesk_Maya-2022--2026-0696D7?style=for-the-badge&logo=autodesk&logoColor=white)

> [!IMPORTANT]
> **🚀 Viewport Screenshot Pro v1.2 is Out Now! (Launch Sale ends Nov 29)**
> Upgrade to **VPS Pro** to unlock the complete daily capture & sharing workflow inside Autodesk Maya:
> - **Real-Time 3D Viewport GIF Recording:** Record live viewport orbiting, modeling, or animation directly to a lightweight animated GIF—no OBS or external screen recorders required (includes custom FPS/scale, cursor indicator, auto-stop timer, and floating recording bar).
> - **Multi-Panel Composite & Full Window Capture:** Combine multiple panels (e.g., *3D Viewport + Outliner / Hypershade / Node Editor*) into a single image, or capture the entire Maya window cleanly.
> - **Transparent Background (Alpha PNG) & Presets:** Copy clean cutouts straight to your OS clipboard and save custom capture presets.
>
> 👉 **[Download VPS Pro on Gumroad (Global)](https://mashitaya.gumroad.com/l/ysgtzm/LAUNCH)** | **[BOOTHでPro版を購入する (国内向け / 11月29日までローンチセール中)](https://yworks.booth.pm/items/9112055)**

![Viewport Screenshot (VPS) v1.2 Demo](MAYA_all_demo.gif)

---

## English

### Overview

**Viewport Screenshot (VPS)** is a fast, lightweight utility for **Autodesk Maya** designed to capture clean viewport screenshots and copy them straight to your OS clipboard (`Ctrl+V` into Photoshop, Discord, Slack, or PureRef) in one click.

This repository hosts the standalone, open-source **Free Edition**.

#### Free Edition Features
* **One-Click Viewport Capture:** Capture the active 3D viewport instantly without opening Playblast or render dialogs.
* **Direct Clipboard Copy & File Save:** Automatically copies the image to your clipboard and/or saves it as PNG/JPG.
* **Auto-Hide UI Elements:** Temporarily hides HUD elements, floor grids, and selection highlights for clean WIP shots.
* **Zero External Dependencies:** Runs purely on Maya's built-in Python environment—no external libraries required.

### Free vs. Pro Comparison

| Feature | Free Edition (GitHub) | Pro Edition (v1.2) |
| :--- | :---: | :---: |
| Quick Viewport Screenshot & Clipboard Copy | ✅ | ✅ |
| Auto-Hide HUD / Grid / Overlays | ✅ | ✅ |
| PNG / JPG Export | ✅ | ✅ |
| **Real-Time 3D Viewport GIF Recording** | — | ✅ |
| **Multi-Panel Composite (Viewport + Editors)** | — | ✅ |
| **Full Maya Window Capture** | — | ✅ |
| **Transparent Background (Alpha PNG)** | — | ✅ |
| **Custom Presets & Advanced Capture Settings** | — | ✅ |

👉 **[Get VPS Pro v1.2 on Gumroad (Global)](https://mashitaya.gumroad.com/l/ysgtzm/LAUNCH)** | **[Get VPS Pro v1.2 on BOOTH (Japan)](https://yworks.booth.pm/items/9112055)**

### Installation

1. Download or clone this repository (`Code` > `Download ZIP`) and extract the files.
2. Copy the script folder/files into your Maya scripts directory:
   * **Windows:** `Documents\maya\<version>\scripts\`
   * **macOS:** `~/Library/Preferences/Autodesk/maya/<version>/scripts/`
   * **Linux:** `~/maya/<version>/scripts/`
3. Restart Maya (or run `rehash` in the Script Editor).
4. Run the launch command in the **Python** tab of Maya's Script Editor (and drag it to your Shelf for one-click access):
   ```python
   import viewport_screenshot
   viewport_screenshot.show()
   ```
   *(Note: Replace the module/function name above if your entry script filename differs.)*

### Compatibility & License

* **Autodesk Maya:** 2022, 2023, 2024, 2025, 2026 (Python 3 / PySide2 & PySide6)
* **OS:** Windows / macOS / Linux
* **License:** The **Free Edition** in this repository is open source. For commercial studio deployments or full workflow features, check out **[VPS Pro on Gumroad](https://mashitaya.gumroad.com/l/ysgtzm/LAUNCH)** or **[BOOTH](https://yworks.booth.pm/items/9112055)**.

---

## 日本語

### 概要

**Viewport Screenshot (VPS)** は、**Autodesk Maya** のビューポート画面をワンクリックで綺麗にキャプチャし、OSのクリップボードへ直接コピー（Photoshop、Discord、Slack、PureRefなどへ `Ctrl+V` で即貼り付け）できる軽量・高速な制作支援ツールです。

このリポジトリでは、単体で動作するオープンソースの **無料版（Free Edition）** を公開しています。

#### 無料版（Free Edition）の主な機能
* **ワンクリック・ビューポート撮影：** プレイブラストやレンダー設定を開く手間なく、アクティブな3Dビューポートを即座にキャプチャします。
* **クリップボード直接コピー＆画像保存：** 撮影と同時にクリップボードへ転送し、PNG / JPG形式での自動保存にも対応しています。
* **UI要素の自動一時非表示：** HUD、グリッド、選択ハイライトなどを撮影時だけ自動で隠し、クリーンなWIP（作業進捗）画像を出力します。
* **外部ライブラリ不要：** Maya標準のPython環境のみで動作するため、追加モジュールのインストールは不要です。

### 無料版（Free）と Pro版（v1.2）の機能比較

| 機能 | 無料版 (GitHub) | Pro版 (v1.2) |
| :--- | :---: | :---: |
| クイック・ビューポート撮影＆クリップボードコピー | ✅ | ✅ |
| HUD・グリッド・オーバーレイの自動非表示 | ✅ | ✅ |
| PNG / JPG 画像保存 | ✅ | ✅ |
| **リアルタイム 3Dビューポート GIF録画** | — | ✅ |
| **マルチパネル合成（ビューポート＋アウトライナ/ノード等）** | — | ✅ |
| **Mayaウィンドウ全体のクリーンキャプチャ** | — | ✅ |
| **背景透過（アルファ付きPNG）出力** | — | ✅ |
| **カスタムプリセット保存＆詳細キャプチャ設定** | — | ✅ |

> **🎉 v1.2 ローンチセール開催中（11月29日まで）：**
> リアルタイムGIF録画や複数パネル合成に対応した **VPS Pro v1.2** を特別価格で入手できます。
> 👉 **[BOOTHでVPS Pro v1.2を購入する (国内向け)](https://yworks.booth.pm/items/9112055)** | **[Gumroadで購入する (Global)](https://mashitaya.gumroad.com/l/ysgtzm/LAUNCH)**

### インストール方法

1. このリポジトリ上部の `Code` ＞ `Download ZIP` からファイルをダウンロードし、解凍します。
2. 解凍したスクリプトフォルダ／ファイルを、お使いの環境の Maya `scripts` フォルダにコピーします。
   * **Windows:** `Documents\maya\<バージョン>\scripts\`
   * **macOS:** `~/Library/Preferences/Autodesk/maya/<バージョン>/scripts/`
   * **Linux:** `~/maya/<バージョン>/scripts/`
3. Mayaを再起動します（またはスクリプトエディタで `rehash` を実行）。
4. スクリプトエディタの **Python** タブで以下のコマンドを実行します（シェルフにドラッグ＆ドロップするとボタン化できます）。
   ```python
   import viewport_screenshot
   viewport_screenshot.show()
   ```
   ※ エントリーポイントとなる `.py` ファイル名・関数名が異なる場合は、実際のファイル名に合わせて書き換えてください。

### 対応環境・ライセンス

* **対応Mayaバージョン：** Autodesk Maya 2022, 2023, 2024, 2025, 2026（Python 3 / PySide2 & PySide6 対応）
* **対応OS：** Windows / macOS / Linux
* **ライセンス：** 本リポジトリの **無料版（Free Edition）** はオープンソースです。GIF録画・複数パネル合成などの全機能を利用したい場合は、**[BOOTH](https://yworks.booth.pm/items/9112055)** または **[Gumroad](https://mashitaya.gumroad.com/l/ysgtzm/LAUNCH)** にて **Pro版** をお求めください。