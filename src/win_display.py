"""API Win32 para leitura e alteração da resolução do monitor principal."""

import ctypes
import sys
from ctypes import wintypes
from typing import List, Set, Tuple

if sys.platform != "win32":
    raise RuntimeError("win_display só é suportado no Windows.")


class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", ctypes.c_wchar * 32),
        ("dmSpecVersion", wintypes.WORD),
        ("dmDriverVersion", wintypes.WORD),
        ("dmSize", wintypes.WORD),
        ("dmDriverExtra", wintypes.WORD),
        ("dmFields", wintypes.DWORD),
        ("dmPositionX", wintypes.LONG),
        ("dmPositionY", wintypes.LONG),
        ("dmDisplayOrientation", wintypes.DWORD),
        ("dmDisplayFixedOutput", wintypes.DWORD),
        ("dmColor", wintypes.SHORT),
        ("dmDuplex", wintypes.SHORT),
        ("dmYResolution", wintypes.SHORT),
        ("dmTTOption", wintypes.SHORT),
        ("dmCollate", wintypes.SHORT),
        ("dmFormName", ctypes.c_wchar * 32),
        ("dmLogPixels", wintypes.WORD),
        ("dmBitsPerPel", wintypes.DWORD),
        ("dmPelsWidth", wintypes.DWORD),
        ("dmPelsHeight", wintypes.DWORD),
        ("dmDisplayFlags", wintypes.DWORD),
        ("dmDisplayFrequency", wintypes.DWORD),
        ("dmICMMethod", wintypes.DWORD),
        ("dmICMIntent", wintypes.DWORD),
        ("dmMediaType", wintypes.DWORD),
        ("dmDitherType", wintypes.DWORD),
        ("dmReserved1", wintypes.DWORD),
        ("dmReserved2", wintypes.DWORD),
        ("dmPanningWidth", wintypes.DWORD),
        ("dmPanningHeight", wintypes.DWORD),
    ]


DM_PELSWIDTH = 0x00080000
DM_PELSHEIGHT = 0x00100000
CDS_TEST = 0x00000002
CDS_UPDATEREGISTRY = 0x00000001
DISP_CHANGE_SUCCESSFUL = 0
DISP_CHANGE_BADMODE = -2
DISP_CHANGE_FAILED = -1
DISP_CHANGE_NOTUPDATED = 3

user32 = ctypes.windll.user32

ERROS_DRIVER = {
    DISP_CHANGE_BADMODE: "Resolução não suportada pelo driver de vídeo.",
    DISP_CHANGE_FAILED: "O driver de vídeo rejeitou a alteração.",
    DISP_CHANGE_NOTUPDATED: "Não foi possível salvar no registro do Windows.",
    -3: "Parâmetros inválidos na requisição.",
    -4: "Modo de vídeo não suportado neste hardware.",
    1: "Reinicialização necessária para aplicar a resolução.",
}

_MIN_WIDTH = 800


def get_current_resolution() -> Tuple[int, int]:
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def get_supported_resolutions() -> List[Tuple[int, int]]:
    resolutions: Set[Tuple[int, int]] = set()
    i = 0
    dm = DEVMODE()
    dm.dmSize = ctypes.sizeof(DEVMODE)
    try:
        while user32.EnumDisplaySettingsW(None, i, ctypes.byref(dm)):
            if dm.dmPelsWidth >= _MIN_WIDTH:
                resolutions.add((int(dm.dmPelsWidth), int(dm.dmPelsHeight)))
            i += 1
    except Exception:
        pass
    return sorted(resolutions, key=lambda r: r[0] * r[1])


def test_resolution(width: int, height: int) -> bool:
    dm = DEVMODE()
    dm.dmSize = ctypes.sizeof(DEVMODE)
    dm.dmPelsWidth = width
    dm.dmPelsHeight = height
    dm.dmFields = DM_PELSWIDTH | DM_PELSHEIGHT
    return user32.ChangeDisplaySettingsW(ctypes.byref(dm), CDS_TEST) == DISP_CHANGE_SUCCESSFUL


def change_resolution(width: int, height: int) -> Tuple[bool, str]:
    dm = DEVMODE()
    dm.dmSize = ctypes.sizeof(DEVMODE)
    dm.dmPelsWidth = width
    dm.dmPelsHeight = height
    dm.dmFields = DM_PELSWIDTH | DM_PELSHEIGHT
    result = user32.ChangeDisplaySettingsW(ctypes.byref(dm), CDS_UPDATEREGISTRY)
    if result == DISP_CHANGE_SUCCESSFUL:
        return True, ""
    return False, ERROS_DRIVER.get(result, f"Erro desconhecido (código {result}).")
