"""Informações do adaptador de vídeo via PowerShell (CIM/WMI), sem wmic."""

from __future__ import annotations

import json
import subprocess
import sys
from typing import Any, Optional


def _run_powershell(command: str) -> Optional[str]:
    try:
        kw: dict[str, Any] = {
            "args": [
                "powershell",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                command,
            ],
            "capture_output": True,
            "text": True,
            "timeout": 15,
        }
        if sys.platform == "win32":
            kw["creationflags"] = subprocess.CREATE_NO_WINDOW
        r = subprocess.run(**kw)
        if r.returncode != 0:
            return None
        out = (r.stdout or "").strip()
        return out or None
    except (OSError, subprocess.TimeoutExpired):
        return None


def _format_json_block(raw: str) -> Optional[str]:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return None
    if isinstance(data, dict):
        rows = [data]
    elif isinstance(data, list):
        rows = data
    else:
        return None
    lines: list[str] = []
    for item in rows:
        if not isinstance(item, dict):
            continue
        name = item.get("Name") or "—"
        ver = item.get("DriverVersion") or "—"
        st = item.get("Status") or "—"
        lines.append(f"{name}  |  Driver: {ver}  |  Status: {st}")
    return "\n".join(lines) if lines else None


def get_driver_info() -> str:
    if sys.platform != "win32":
        return "Apenas Windows."

    # CIM: Windows 8+ / servidor moderno (substitui wmic de forma suportada).
    cim_cmd = (
        "Get-CimInstance -ClassName Win32_VideoController | "
        "Select-Object Name,DriverVersion,Status | ConvertTo-Json -Compress"
    )
    raw = _run_powershell(cim_cmd)
    if raw:
        formatted = _format_json_block(raw)
        if formatted:
            return formatted

    # WMI: fallback para ambientes mais antigos onde CIM pode falhar.
    wmi_cmd = (
        "Get-WmiObject Win32_VideoController | "
        "Select-Object Name,DriverVersion,Status | ConvertTo-Json -Compress"
    )
    raw = _run_powershell(wmi_cmd)
    if raw:
        formatted = _format_json_block(raw)
        if formatted:
            return formatted

    return "Informação não disponível (PowerShell ou permissões)."
