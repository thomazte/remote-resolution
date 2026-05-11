"""Caminhos de recursos (modo script e executável PyInstaller)."""

import sys
from pathlib import Path

ICON_FILENAME = "remote-resolution-icon-Photoroom.png"
ICO_FILENAME = "app.ico"
ICON_DIR = "img"


def app_root() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent


def icon_png_path() -> Path:
    return app_root() / ICON_DIR / ICON_FILENAME


def icon_ico_path() -> Path:
    """Ícone Windows (.ico) — melhor para barra de tarefas que PNG/iconphoto."""
    return app_root() / ICON_DIR / ICO_FILENAME


def ensure_icon_ico(*, force: bool = False) -> bool:
    """
    Garante que exista `img/app.ico` a partir do PNG (para barra de tarefas no Windows).
    No modo script: cria/atualiza o arquivo se Pillow estiver instalado.
    No .exe (PyInstaller): não grava em _MEIPASS — usa o .ico já empacotado no build.
    Retorna True se `icon_ico_path()` existir ao final.
    """
    if getattr(sys, "frozen", False):
        return icon_ico_path().is_file()

    png = icon_png_path()
    ico = icon_ico_path()
    if not png.is_file():
        return ico.is_file()

    if ico.is_file() and not force:
        try:
            if ico.stat().st_mtime >= png.stat().st_mtime:
                return True
        except OSError:
            return True

    try:
        from PIL import Image
    except ImportError:
        return ico.is_file()

    try:
        ico.parent.mkdir(parents=True, exist_ok=True)
        im = Image.open(png).convert("RGBA")
        im.thumbnail((256, 256), Image.Resampling.LANCZOS)
        im.save(ico, format="ICO")
        return True
    except Exception:
        return ico.is_file()
