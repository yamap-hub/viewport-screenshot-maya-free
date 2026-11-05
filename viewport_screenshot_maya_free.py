# -*- coding: utf-8 -*-
"""
Viewport Screenshot for Maya  (無料・お試し版)

3Dビューポートを、パネルのメニュー/HUD/グリッドを隠した状態で1枚だけ
Windows標準の Pictures/Screenshots へ PNG 保存します。

【無料版でできること】
    3Dビューポートの撮影 / PNG保存 / Windows標準Screenshotsへ保存
    パネルのメニュー・HUD・グリッドを隠して撮影 / 常に最新1枚のみ保存

【製品版のみ】
    3Dビュー以外のパネル・ドッキングウィンドウの撮影 / マウス下を撮影
    JPEG・BMP保存 / ファイル名・プリフィックス・サフィックス・連番
    保存先フォルダの指定 / クリップボードへコピー
    マニピュレータ・ViewCube・オーバーレイを隠す

対応: Maya 2022 以降 (Python 3 / PySide2 or PySide6)

使い方:
    1. このファイルを Maya の scripts フォルダ (または任意のフォルダ) に
       viewport_screenshot_maya_free.py という名前で保存
    2. スクリプトエディタ (Python) で次を一度だけ実行してシェルフ登録
           import viewport_screenshot_maya_free as vssf
           vssf.install_shelf_button()
    3. シェルフのボタンをクリック → 設定ウィンドウが開く
       右クリック → クイック撮影 / 保存先フォルダを開く
"""

import os
import re
import glob
import shutil
import tempfile
import time
import platform
import subprocess
from datetime import datetime

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as omui
import maya.utils

try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from shiboken6 import wrapInstance
except ImportError:
    from PySide2 import QtCore, QtGui, QtWidgets
    from shiboken2 import wrapInstance



# ---------------------------------------------------------------------------
# 多言語対応 (日本語 / English)
#   tr(日本語の文): 現在のUI言語に合わせた表示文字列を返す（辞書に無い文はそのまま）
#   bi(日本語の文): 登録時に固定される文字列（シェルフのメニュー等）用に「日本語 / English」を返す
# ---------------------------------------------------------------------------
_EN = {
    "メニューを含むパネルのウィジェットが見つからなかったため、メニューなしで保存します（詳細はスクリプトエディタの [Viewport Capture] を確認）": "Could not find the widget containing the panel menu, so the image is saved without the menu (see [Viewport Capture] in the Script Editor for details)",
    "3Dビューポートが見つかりませんでした。": "Could not find a 3D viewport.",
    "画像を保存できませんでした。": "Could not save the image.",
    "ファイルとして保存・importしてから実行してください（シェルフ登録にはファイルの場所が必要です）。": "Save this as a file and import it before running (shelf registration needs the file location).",
    "保存先フォルダを作成できませんでした: {error}": "Could not create the output folder: {error}",
    "撮影に失敗しました: {error}": "Capture failed: {error}",
    "3Dビューポートを保存しました: {name}": "Saved the 3D viewport: {name}",
    "シェルフ「{name}」にボタンを登録しました。": "Registered the button on shelf '{name}'.",
    "保存先フォルダを開く": "Open Output Folder",
    "3Dビューをキャプチャ (1枚保存)": "Capture 3D view (save 1 image)",
    "3秒後にマウス下のパネルを撮影": "Capture the panel under the mouse after 3 s",
    "撮影時に隠すメニュー・表示": "Hide while capturing",
    "パネルのメニュー / ツールバーを隠す": "Hide panel menu / toolbar",
    "HUD (ヘッドアップディスプレイ) を隠す": "Hide HUD (heads-up display)",
    "グリッドを隠す": "Hide grid",
    "保存先フォルダを開く（撮影しない）": "Open output folder (no capture)",
    "保存先 (Windows標準 Screenshots)": "Output folder (Windows default Screenshots)",
    "形式: PNG / 常に最新1枚のみ保存": "Format: PNG / always keeps only the latest image",
    "製品版で使える機能": "Features in the full version",
    "製品版を見る": "View the full version",
    "[製品版]  ": "[Full]  ",
    "3Dビュー以外のパネル / ドッキングウィンドウの撮影": "Capturing panels / docked windows other than the 3D view",
    "JPEG / BMP 形式での保存": "Saving as JPEG / BMP",
    "ファイル名・プリフィックス・サフィックス・連番": "File name, prefix, suffix and sequence numbers",
    "保存先フォルダの自由な指定": "Choosing any output folder",
    "クリップボードにコピー (Ctrl+V)": "Copy to clipboard (Ctrl+V)",
    "マニピュレータ / ViewCube / オーバーレイを隠す": "Hide manipulators / ViewCube / overlays",
    "クイック撮影（3Dビュー）": "Quick capture (3D view)",
    "設定ウィンドウを開く": "Open settings window",
}


def get_lang():
    try:
        return "EN" if get_opt("language") == "EN" else "JA"
    except Exception:
        return "JA"


def tr(text):
    if get_lang() == "EN":
        return _EN.get(text, text)
    return text


def bi(text):
    en = _EN.get(text)
    if en and en != text:
        return f"{text} / {en}"
    return text


# ---------------------------------------------------------------------------
# 定数
# ---------------------------------------------------------------------------
WIN = "vpScreenshotFreeWindow"
LABEL_DIR = "vpScreenshotFreeDirLabel"
LANG_MENU = "vpScreenshotFreeLangMenu"

SHELF_LABEL = "VPCaptureFree"
SHELF_ANNOTATION = "Viewport Capture Free - right-click: quick capture / 右クリック: クイック撮影"

# 製品版の案内ページのURL。設定するとウィンドウに「製品版を見る」ボタンが出ます（空なら非表示）
PRO_URL = ""

# 製品版で使える機能（ウィンドウにロック表示します）
PRO_FEATURES = (
    "3Dビュー以外のパネル / ドッキングウィンドウの撮影",
    "3秒後にマウス下のパネルを撮影",
    "JPEG / BMP 形式での保存",
    "ファイル名・プリフィックス・サフィックス・連番",
    "保存先フォルダの自由な指定",
    "クリップボードにコピー (Ctrl+V)",
    "マニピュレータ / ViewCube / オーバーレイを隠す",
)

# UIを隠してから撮影するまでの待ち時間(ms)。まだ黒い/メニューが写る場合は増やす
WAIT_MS = 400
# 連打防止(秒)
DEBOUNCE_SEC = 1.2

_DEFAULTS = {
    "language": "JA",
    "hide_menus": 1,
    "hide_hud": 1,
    "hide_grid": 0,
}

_BUSY = False
_LAST_EXEC = 0.0


# ---------------------------------------------------------------------------
# 設定の保存 (optionVar)
# ---------------------------------------------------------------------------
def get_opt(key):
    name = "vpssf_" + key
    if cmds.optionVar(exists=name):
        return cmds.optionVar(q=name)
    return _DEFAULTS[key]


def set_opt(key, value):
    if isinstance(_DEFAULTS[key], str):
        cmds.optionVar(stringValue=("vpssf_" + key, str(value)))
    else:
        cmds.optionVar(intValue=("vpssf_" + key, int(bool(value))))


# ---------------------------------------------------------------------------
# パス関連
# ---------------------------------------------------------------------------
def get_windows_screenshots_dir():
    """Windowsの標準Screenshotsフォルダを取得（OneDrive環境対応）"""
    home = os.path.expanduser("~")
    default_path = os.path.join(home, "Pictures", "Screenshots")

    onedrive = os.environ.get("OneDrive") or os.environ.get("OneDriveConsumer")
    if onedrive and os.path.exists(onedrive):
        for sub in ("Pictures", "画像"):
            candidate = os.path.join(onedrive, sub, "Screenshots")
            if os.path.exists(candidate):
                return candidate

    try:
        os.makedirs(default_path, exist_ok=True)
    except Exception:
        pass
    return default_path


def open_directory_in_explorer(folder_path):
    """フォルダをエクスプローラー等で開く（撮影はしない）"""
    try:
        os.makedirs(folder_path, exist_ok=True)
        system = platform.system()
        if system == "Windows":
            os.startfile(folder_path)
        elif system == "Darwin":
            subprocess.run(["open", folder_path], check=False)
        else:
            subprocess.run(["xdg-open", folder_path], check=False)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# ヘルパー
# ---------------------------------------------------------------------------
def _info(msg):
    print("[Viewport Capture Free] " + msg)
    try:
        cmds.inViewMessage(amg=msg, pos="topCenter", fade=True)
    except Exception:
        pass


def _warn(msg):
    cmds.warning("[Viewport Capture Free] " + msg)


def _find_widget(name):
    """Mayaの UI/パネル名から QWidget を取得"""
    if not name:
        return None
    ptr = omui.MQtUtil.findControl(name) or omui.MQtUtil.findLayout(name)
    if not ptr:
        return None
    return wrapInstance(int(ptr), QtWidgets.QWidget)


def resolve_model_panel():
    """撮影対象の3Dビューを決める（フォーカス中の3Dビュー → 最大の3Dビュー）"""
    focus = cmds.getPanel(withFocus=True)
    if focus and cmds.getPanel(typeOf=focus) == "modelPanel":
        return focus

    models = [p for p in (cmds.getPanel(visiblePanels=True) or [])
              if cmds.getPanel(typeOf=p) == "modelPanel"]
    best, best_area = None, -1
    for p in models:
        w = _find_widget(p)
        if w is not None and w.width() * w.height() > best_area:
            best, best_area = p, w.width() * w.height()
    return best


# ---------------------------------------------------------------------------
# UI の一時非表示 / 復元
# ---------------------------------------------------------------------------
def _hide(state, getter, setter, hidden=False):
    """getterで現在値を取り、違えば hidden に変更。元に戻す処理を state に積む"""
    try:
        orig = getter()
        if orig == hidden:
            return False
        setter(hidden)
        state["restore"].append((setter, orig))
        return True
    except Exception:
        return False


def _hide_editor_flag(state, editor, flag):
    def getter():
        return bool(cmds.modelEditor(editor, q=True, **{flag: True}))

    def setter(v):
        cmds.modelEditor(editor, e=True, **{flag: v})

    return _hide(state, getter, setter, False)


def _hide_menu_bar(state, panel):
    def getter():
        return bool(cmds.panel(panel, q=True, menuBarVisible=True))

    def setter(v):
        cmds.panel(panel, e=True, menuBarVisible=v)

    return _hide(state, getter, setter, False)


def _hide_bar_layout(state, panel):
    """3Dビューのパネルツールバー（アイコン列）"""
    try:
        bar = cmds.modelPanel(panel, q=True, barLayout=True)
    except Exception:
        return False
    if not bar:
        return False

    def getter():
        return bool(cmds.layout(bar, q=True, visible=True))

    def setter(v):
        cmds.layout(bar, e=True, visible=v)

    return _hide(state, getter, setter, False)


def restore_ui(state):
    for setter, orig in reversed(state["restore"]):
        try:
            setter(orig)
        except Exception:
            pass
    state["restore"] = []
    try:
        cmds.refresh(force=True)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# 撮影
# ---------------------------------------------------------------------------
def begin_capture(panel):
    """UIを隠して撮影情報(state)を返す。撮影はまだしない"""
    if not panel or cmds.getPanel(typeOf=panel) != "modelPanel":
        _warn(tr("3Dビューポートが見つかりませんでした。"))
        return None

    output_dir = get_windows_screenshots_dir()
    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        _warn(tr("保存先フォルダを作成できませんでした: {error}").format(error=e))
        return None

    scene_path = cmds.file(q=True, sceneName=True) or ""
    scene_name = os.path.splitext(os.path.basename(scene_path))[0] if scene_path else "Untitled"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{scene_name}_{timestamp}.png"

    editor = cmds.modelPanel(panel, q=True, modelEditor=True)

    state = {
        "panel": panel,
        "editor": editor,
        "restore": [],
        "changed": False,
        "output_dir": output_dir,
        "scene_name": scene_name,
        "filename": filename,
        "filepath": os.path.join(output_dir, filename),
        "hide_hud": bool(get_opt("hide_hud")),
        "hide_menus": bool(get_opt("hide_menus")),
    }

    changed = False
    if get_opt("hide_menus"):
        changed |= _hide_menu_bar(state, panel)
        changed |= _hide_bar_layout(state, panel)
    if get_opt("hide_hud"):
        changed |= _hide_editor_flag(state, editor, "headsUpDisplay")
    if get_opt("hide_grid"):
        changed |= _hide_editor_flag(state, editor, "grid")

    state["changed"] = changed
    return state


def _log(msg):
    print("[Viewport Capture] " + msg)


def _viewport_widget(panel):
    """3Dビュー(GL描画領域)そのもののウィジェットを、M3dView経由で正確に取得する"""
    try:
        view = omui.M3dView()
        omui.M3dView.getM3dViewFromModelPanel(panel, view)
        ptr = view.widget()
        if ptr:
            return wrapInstance(int(ptr), QtWidgets.QWidget)
    except Exception:
        pass
    return None


def _viewport_pixel_size(panel, state):
    """playblastに渡す3Dビューの大きさ(ピクセル)を返す"""
    try:
        view = omui.M3dView()
        omui.M3dView.getM3dViewFromModelPanel(panel, view)
        w, h = int(view.portWidth()), int(view.portHeight())
        if w >= 16 and h >= 16:
            return w, h
    except Exception:
        pass

    widget = _viewport_widget(panel) or _find_widget(state["editor"]) or _find_widget(panel)
    ratio = 1.0
    try:
        ratio = float(widget.devicePixelRatioF())
    except Exception:
        pass
    return max(int(widget.width() * ratio), 16), max(int(widget.height() * ratio), 16)


def _describe_chain(widget):
    """ウィジェットから親をたどった構造を文字列にする（診断用）"""
    parts = []
    w = widget
    depth = 0
    while w is not None and depth < 10:
        try:
            parts.append("{}({})[{}x{}]".format(w.metaObject().className(), w.objectName(), w.width(), w.height()))
        except Exception:
            parts.append("?")
        w = w.parentWidget()
        depth += 1
    return " <- ".join(parts)


def _find_chrome_widget(panel_widget, editor_widget):
    """
    メニューバー/ツールバーを含む「パネル全体」のウィジェットを探す。
    3D描画領域より縦に十分大きく、横幅がほぼ同じ最初の親ウィジェットを採用する。
    """
    if editor_widget is None:
        return None

    candidates = []
    if panel_widget is not None:
        candidates.append(panel_widget)
    w = editor_widget.parentWidget()
    depth = 0
    while w is not None and depth < 10:
        candidates.append(w)
        w = w.parentWidget()
        depth += 1

    for c in candidates:
        try:
            if not c.isAncestorOf(editor_widget):
                continue
        except Exception:
            continue
        extra_h = c.height() - editor_widget.height()
        extra_w = c.width() - editor_widget.width()
        if extra_h >= 10 and -2 <= extra_w <= 6:
            return c
    return None


def _compose_with_panel_chrome(state, viewport_image):
    """
    パネルのメニュー/ツールバーも写す場合(隠さない設定)の合成処理。
    playblastの画像にはパネルのメニューが含まれないため、パネル全体をQtで取得し、
    3Dビュー部分をplayblastの画像で置き換える（GL描画が黒くなるのを避けるため）。
    """
    panel_widget = _find_widget(state["panel"])
    editor_widget = _viewport_widget(state["panel"]) or _find_widget(state["editor"])

    chrome_widget = _find_chrome_widget(panel_widget, editor_widget)
    _log("composite: viewport chain = " + (_describe_chain(editor_widget) if editor_widget is not None else "None"))
    _log("composite: panel widget = " + (_describe_chain(panel_widget) if panel_widget is not None else "None"))
    _log("composite: chrome widget = " + (_describe_chain(chrome_widget) if chrome_widget is not None else "None"))

    if chrome_widget is None or editor_widget is None:
        _warn(tr("メニューを含むパネルのウィジェットが見つからなかったため、メニューなしで保存します（詳細はスクリプトエディタの [Viewport Capture] を確認）"))
        return viewport_image

    chrome = chrome_widget.grab().toImage()
    ratio = float(chrome.devicePixelRatio()) or 1.0
    chrome.setDevicePixelRatio(1.0)
    rgb32 = getattr(QtGui.QImage, "Format_RGB32", None)
    if rgb32 is None:
        rgb32 = QtGui.QImage.Format.Format_RGB32
    chrome = chrome.convertToFormat(rgb32)

    top_left = editor_widget.mapTo(chrome_widget, QtCore.QPoint(0, 0))
    target = QtCore.QRectF(
        top_left.x() * ratio,
        top_left.y() * ratio,
        editor_widget.width() * ratio,
        editor_widget.height() * ratio,
    )
    painter = QtGui.QPainter(chrome)
    try:
        painter.drawImage(target, viewport_image)
    finally:
        painter.end()
    return chrome


def _save_model_panel(state):
    """playblast(1フレーム)でパネルを画像化し、RGBのPNGで保存する"""
    panel = state["panel"]
    filepath = state["filepath"]

    width, height = _viewport_pixel_size(panel, state)

    # playblastのPNGはアルファ付き(背景透明)になるため、
    # アルファを持たないJPGで一旦出力し、RGBのPNGへ変換して保存する
    tmp_dir = tempfile.mkdtemp(prefix="vpssf_")
    try:
        tmp_file = os.path.join(tmp_dir, "cap.jpg")
        cmds.refresh(force=True)
        cmds.playblast(
            frame=[cmds.currentTime(q=True)],
            format="image",
            compression="jpg",
            quality=100,
            percent=100,
            widthHeight=[width, height],
            viewer=False,
            showOrnaments=not state["hide_hud"],
            forceOverwrite=True,
            clearCache=True,
            offScreen=False,
            editorPanelName=panel,
            completeFilename=tmp_file,
        )

        candidates = sorted(
            glob.glob(os.path.join(glob.escape(tmp_dir), "*.jpg")),
            key=os.path.getmtime,
        )
        if not candidates:
            return False

        image = QtGui.QImage(candidates[-1])
        if image.isNull():
            return False

        fmt = getattr(QtGui.QImage, "Format_RGB888", None)
        if fmt is None:
            fmt = QtGui.QImage.Format.Format_RGB888
        image = image.convertToFormat(fmt)
        if not state["hide_menus"]:
            try:
                image = _compose_with_panel_chrome(state, image)
            except Exception:
                import traceback
                traceback.print_exc()   # 合成に失敗したら、メニューなしの画像をそのまま保存する
                _log("composite: 合成に失敗したため、メニューなしで保存します")
        return bool(image.save(filepath, "PNG"))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _cleanup_old_files(state):
    """無料版は常に最新1枚のみ残す（同じシーンの古い画像を削除）"""
    try:
        pattern = re.compile(rf"^{re.escape(state['scene_name'])}_\d{{8}}_\d{{6}}\.png$", re.IGNORECASE)
        out = state["output_dir"]
        for fname in os.listdir(out):
            if fname != state["filename"] and pattern.match(fname):
                p = os.path.join(out, fname)
                if os.path.isfile(p):
                    os.remove(p)
    except Exception:
        pass


def finish_capture(state):
    """描画が反映された状態で撮影し、UIを復元する"""
    global _BUSY
    ok = False
    try:
        ok = _save_model_panel(state)
    except Exception as e:
        _warn(tr("撮影に失敗しました: {error}").format(error=e))
    finally:
        restore_ui(state)
        _BUSY = False

    if not ok:
        _warn(tr("画像を保存できませんでした。"))
        return

    _cleanup_old_files(state)
    _info(tr("3Dビューポートを保存しました: {name}").format(name=state['filename']))


def start_capture(panel):
    """UIを隠す → 少し待つ → 撮影 → 復元"""
    global _BUSY, _LAST_EXEC
    now = time.time()
    if _BUSY or now - _LAST_EXEC < DEBOUNCE_SEC:
        return
    state = begin_capture(panel)
    if state is None:
        return
    _LAST_EXEC = now
    _BUSY = True

    if not state["changed"]:
        finish_capture(state)   # 何も隠していないので待たずに撮影
        return

    try:
        cmds.refresh(force=True)
    except Exception:
        pass
    QtCore.QTimer.singleShot(WAIT_MS, lambda: finish_capture(state))


# ---------------------------------------------------------------------------
# 公開コマンド
# ---------------------------------------------------------------------------
def capture():
    """3Dビューポートを撮影"""
    start_capture(resolve_model_panel())


def quick_capture():
    """シェルフ右クリック用（captureと同じ）"""
    capture()


def open_output_folder():
    open_directory_in_explorer(get_windows_screenshots_dir())


# ---------------------------------------------------------------------------
# 設定ウィンドウ
# ---------------------------------------------------------------------------
def _check(label, key):
    cmds.checkBox(
        label=tr(label),
        value=bool(get_opt(key)),
        changeCommand=lambda v, k=key: set_opt(k, v),
    )


def _on_language_changed(*_):
    idx = cmds.optionMenu(LANG_MENU, q=True, select=True)
    set_opt("language", "EN" if idx == 2 else "JA")
    maya.utils.executeDeferred(show)   # ウィンドウを作り直して言語を反映


def show():
    """設定ウィンドウを開く（シェルフのボタンから呼ばれる）"""
    if cmds.window(WIN, exists=True):
        cmds.deleteUI(WIN)

    cmds.window(WIN, title="Viewport Capture (Free)", widthHeight=(400, 560), sizeable=True)
    cmds.scrollLayout(childResizable=True)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=6, columnOffset=("both", 8))

    cmds.separator(height=4, style="none")

    cmds.optionMenu(LANG_MENU, label="Language / 言語", changeCommand=_on_language_changed)
    cmds.menuItem(label="日本語", parent=LANG_MENU)
    cmds.menuItem(label="English", parent=LANG_MENU)
    cmds.optionMenu(LANG_MENU, e=True, select=(2 if get_lang() == "EN" else 1))

    cmds.button(label=tr("3Dビューをキャプチャ (1枚保存)"), height=40,
                command=lambda *_: capture())

    # 隠す項目
    cmds.frameLayout(label=tr("撮影時に隠すメニュー・表示"), collapsable=False, marginWidth=6, marginHeight=6)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=2)
    _check("パネルのメニュー / ツールバーを隠す", "hide_menus")
    _check("HUD (ヘッドアップディスプレイ) を隠す", "hide_hud")
    _check("グリッドを隠す", "hide_grid")
    cmds.setParent("..")
    cmds.setParent("..")

    # 保存先（無料版は固定）
    cmds.frameLayout(label=tr("保存先 (Windows標準 Screenshots)"), collapsable=False, marginWidth=6, marginHeight=6)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=4)
    cmds.text(LABEL_DIR, label=get_windows_screenshots_dir(), align="left")
    cmds.button(label=tr("保存先フォルダを開く（撮影しない）"), command=lambda *_: open_output_folder())
    cmds.text(label=tr("形式: PNG / 常に最新1枚のみ保存"), align="left")
    cmds.setParent("..")
    cmds.setParent("..")

    # 製品版の機能（ロック表示）
    cmds.frameLayout(label=tr("製品版で使える機能"), collapsable=False, marginWidth=6, marginHeight=6)
    cmds.columnLayout(adjustableColumn=True, rowSpacing=2)
    for text in PRO_FEATURES:
        cmds.text(label=tr("[製品版]  ") + tr(text), align="left")
    if PRO_URL:
        cmds.button(label=tr("製品版を見る"),
                    command=lambda *_: cmds.launch(webPage=PRO_URL))
    cmds.setParent("..")
    cmds.setParent("..")

    cmds.showWindow(WIN)


# ---------------------------------------------------------------------------
# シェルフ登録
# ---------------------------------------------------------------------------
def install_shelf_button():
    """現在アクティブなシェルフにボタンを登録（再実行すると置き換え）"""
    try:
        mod_file = os.path.abspath(__file__)
    except NameError:
        _warn(tr("ファイルとして保存・importしてから実行してください（シェルフ登録にはファイルの場所が必要です）。"))
        return

    mod_dir = os.path.dirname(mod_file)
    mod_name = os.path.splitext(os.path.basename(mod_file))[0]
    boot = (
        "import sys\n"
        f"_p = {mod_dir!r}\n"
        "if _p not in sys.path:\n"
        "    sys.path.append(_p)\n"
        f"import {mod_name} as vssf\n"
    )

    shelf_top = mel.eval("$tmp = $gShelfTopLevel")
    current = cmds.tabLayout(shelf_top, q=True, selectTab=True)

    # 既存の同名ボタンを削除
    for child in cmds.shelfLayout(current, q=True, childArray=True) or []:
        try:
            if (cmds.objectTypeUI(child) == "shelfButton"
                    and cmds.shelfButton(child, q=True, label=True) == SHELF_LABEL):
                cmds.deleteUI(child)
        except Exception:
            pass

    btn = cmds.shelfButton(
        parent=current,
        label=SHELF_LABEL,
        annotation=SHELF_ANNOTATION,
        image1="camera.png",
        imageOverlayLabel="Free",
        overlayLabelColor=(1, 1, 1),
        overlayLabelBackColor=(0, 0, 0, 0.6),
        style="iconOnly",
        sourceType="python",
        command=boot + "vssf.show()",
    )

    popup = cmds.popupMenu(parent=btn, button=3)
    cmds.menuItem(label=bi("クイック撮影（3Dビュー）"), parent=popup,
                  sourceType="python", command=boot + "vssf.quick_capture()")
    cmds.menuItem(label=bi("保存先フォルダを開く"), parent=popup,
                  sourceType="python", command=boot + "vssf.open_output_folder()")
    cmds.menuItem(divider=True, parent=popup)
    cmds.menuItem(label=bi("設定ウィンドウを開く"), parent=popup,
                  sourceType="python", command=boot + "vssf.show()")

    _info(tr("シェルフ「{name}」にボタンを登録しました。").format(name=current))


# スクリプトエディタから直接実行した場合は設定ウィンドウを開く
if __name__ == "__main__":
    show()
