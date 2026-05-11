"""Gera img/app.ico a partir do PNG (CLI) para uso no build/execução local."""

import sys

from app_assets import ensure_icon_ico, icon_ico_path, icon_png_path


def main() -> int:
    png = icon_png_path()
    if not png.is_file():
        print(f"[make_ico] PNG não encontrado: {png}", file=sys.stderr)
        return 1
    if ensure_icon_ico(force=True):
        print(f"[make_ico] Gerado {icon_ico_path()}")
        return 0
    print(
        "[make_ico] Pillow não instalado ou falha ao gravar — use: py -3 -m pip install pillow",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
