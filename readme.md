# Viewport Screenshot for Maya (Free)

> ⚡ **Looking for the Pro Version?**  
> Check out the Pro features on [Gumroad](https://mashitaya.gumroad.com/l/ysgtzm) or [BOOTH](https://yworks.booth.pm/).

Autodesk Mayaの3Dビューポートを、メニューバーやHUD、グリッドを一時的に自動非表示にした状態で綺麗に1枚キャプチャ・保存できるスクリプトツール（無料・お試し版）です。

作業進捗の共有、SNS投稿、ポートフォリオ用の画像書き出しを手間なくワンクリックで行えます。

---

## 主な特徴

- **ワンクリック撮影**: シェルフボタンや右クリックメニューから即座に撮影可能
- **自動クリーンアップ**: キャプチャ時のみ「メニューバー」「ツールバー」「HUD」「グリッド」を自動で一時非表示（撮影後に自動復元）
- **スマート保存**: Windows標準の `Pictures/Screenshots` フォルダへ自動保存（OneDrive同期環境も自動判別）
- **自動整理機能**: フォルダが散らからないよう、同一シーンのキャプチャは「常に最新1枚のみ残す」自動上書き整理仕様
- **多言語対応**: 日本語・英語のUI表示切り替えに対応（ウィンドウ内のメニューから即時切り替え）

---

## 動作要件

- **Autodesk Maya**: 2022 以降
- **Python環境**: Python 3（PySide2 または PySide6）
- **対応OS**: Windows（Screenshotsフォルダ自動判別対応）

---

## インストール手順

1. 本リポジトリの Releases（またはリポジトリ内）から `viewport_screenshot_maya_free.py` をダウンロードします。
2. ダウンロードしたファイルを、お使いの環境の Maya スクリプトフォルダに配置します。
   - 例: `C:/Users/<ユーザー名>/Documents/maya/scripts/`
3. Mayaを起動し、**スクリプトエディタ（Pythonタブ）** を開いて以下のコードを1度だけ実行します。

```python
import viewport_screenshot_maya_free as vssf
vssf.install_shelf_button()
```

4. 現在アクティブなシェルフに **カメラアイコン（ラベル: Free）** が追加されます。

---

## 使い方

### 1. シェルフボタンの操作
- **左クリック**: 設定・撮影ウィンドウを表示
- **右クリック**:
  - `クイック撮影（3Dビュー）`: ウィンドウを開かずに即時キャプチャ
  - `保存先フォルダを開く`: スクリーンショット保存先をエクスプローラーで開く
  - `設定ウィンドウを開く`: キャプチャオプション画面を表示

### 2. 設定ウィンドウの機能
- **言語切り替え**: `Language / 言語` メニューから 日本語 / English を切り替え可能
- **隠す項目のカスタマイズ**:
  - パネルのメニュー / ツールバーを隠す
  - HUD（ヘッドアップディスプレイ）を隠す
  - グリッドを隠す
- **保存先確認**: 保存先パスの表示と「保存先フォルダを開く」ボタン

---

## 更新履歴

- **v1.0.0**
  - 初回リリース
  - Maya 2022+ (PySide2 / PySide6) 対応
  - 日本語 / 英語 UI切り替え対応
  - UI一時非表示・自動復元機能
  - Windows / OneDrive 保存先自動検出

---

## ライセンス

本ツールは [MIT License](LICENSE) のもとで公開されています。商用・非商用問わずご利用いただけます。

---
## 💎 製品版　Viewport Screenshot
不要なUIの自動非表示、クリップボード即時コピー（Ctrl+V）、全パネル撮影に対応バージョンをBOOTHにて公開中。

👉 **[BOOTHで見る（Viewport Screenshot Pro）](https://yworks.booth.pm/items/9112055)**
---
