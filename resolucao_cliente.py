# ──────────────────────────────────────────────────────────────────────────────
#  Ajuste de Resolução — Suporte Remoto
#  Desenvolvido por: Thomaz Arthur
# ──────────────────────────────────────────────────────────────────────────────

import tkinter as tk
from tkinter import messagebox
import ctypes
from ctypes import wintypes
import sys

if sys.platform == "win32":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# ── Win32 structs ──────────────────────────────────────────────────────────────
class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName",         ctypes.c_wchar * 32),
        ("dmSpecVersion",        wintypes.WORD),
        ("dmDriverVersion",      wintypes.WORD),
        ("dmSize",               wintypes.WORD),
        ("dmDriverExtra",        wintypes.WORD),
        ("dmFields",             wintypes.DWORD),
        ("dmPositionX",          wintypes.LONG),
        ("dmPositionY",          wintypes.LONG),
        ("dmDisplayOrientation", wintypes.DWORD),
        ("dmDisplayFixedOutput", wintypes.DWORD),
        ("dmColor",              wintypes.SHORT),
        ("dmDuplex",             wintypes.SHORT),
        ("dmYResolution",        wintypes.SHORT),
        ("dmTTOption",           wintypes.SHORT),
        ("dmCollate",            wintypes.SHORT),
        ("dmFormName",           ctypes.c_wchar * 32),
        ("dmLogPixels",          wintypes.WORD),
        ("dmBitsPerPel",         wintypes.DWORD),
        ("dmPelsWidth",          wintypes.DWORD),
        ("dmPelsHeight",         wintypes.DWORD),
        ("dmDisplayFlags",       wintypes.DWORD),
        ("dmDisplayFrequency",   wintypes.DWORD),
        ("dmICMMethod",          wintypes.DWORD),
        ("dmICMIntent",          wintypes.DWORD),
        ("dmMediaType",          wintypes.DWORD),
        ("dmDitherType",         wintypes.DWORD),
        ("dmReserved1",          wintypes.DWORD),
        ("dmReserved2",          wintypes.DWORD),
        ("dmPanningWidth",       wintypes.DWORD),
        ("dmPanningHeight",      wintypes.DWORD),
    ]

DM_PELSWIDTH           = 0x00080000
DM_PELSHEIGHT          = 0x00100000
CDS_TEST               = 0x00000002
CDS_UPDATEREGISTRY     = 0x00000001
DISP_CHANGE_SUCCESSFUL = 0
DISP_CHANGE_BADMODE    = -2
DISP_CHANGE_FAILED     = -1
DISP_CHANGE_NOTUPDATED = 3

user32 = ctypes.windll.user32

ERROS_DRIVER = {
    DISP_CHANGE_BADMODE:    "Resolução não suportada pelo driver de vídeo.",
    DISP_CHANGE_FAILED:     "O driver de vídeo rejeitou a alteração.",
    DISP_CHANGE_NOTUPDATED: "Não foi possível salvar no registro do Windows.",
    -3: "Parâmetros inválidos na requisição.",
    -4: "Modo de vídeo não suportado neste hardware.",
    1:  "Reinicialização necessária para aplicar a resolução.",
}

def get_current_resolution():
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def get_supported_resolutions():
    resolutions = set()
    i = 0
    dm = DEVMODE()
    dm.dmSize = ctypes.sizeof(DEVMODE)
    try:
        while user32.EnumDisplaySettingsW(None, i, ctypes.byref(dm)):
            if dm.dmPelsWidth >= 800:
                resolutions.add((dm.dmPelsWidth, dm.dmPelsHeight))
            i += 1
    except Exception:
        pass
    return sorted(resolutions, key=lambda r: r[0] * r[1])

def test_resolution(width, height):
    dm = DEVMODE()
    dm.dmSize       = ctypes.sizeof(DEVMODE)
    dm.dmPelsWidth  = width
    dm.dmPelsHeight = height
    dm.dmFields     = DM_PELSWIDTH | DM_PELSHEIGHT
    return user32.ChangeDisplaySettingsW(ctypes.byref(dm), CDS_TEST) == DISP_CHANGE_SUCCESSFUL

def change_resolution(width, height):
    dm = DEVMODE()
    dm.dmSize       = ctypes.sizeof(DEVMODE)
    dm.dmPelsWidth  = width
    dm.dmPelsHeight = height
    dm.dmFields     = DM_PELSWIDTH | DM_PELSHEIGHT
    result = user32.ChangeDisplaySettingsW(ctypes.byref(dm), CDS_UPDATEREGISTRY)
    if result == DISP_CHANGE_SUCCESSFUL:
        return True, ""
    return False, ERROS_DRIVER.get(result, f"Erro desconhecido (código {result}).")

def get_driver_info():
    try:
        import subprocess
        r = subprocess.run(
            ["wmic", "path", "win32_VideoController", "get", "Name,DriverVersion,Status"],
            capture_output=True, text=True, timeout=5
        )
        lines = [l.strip() for l in r.stdout.strip().splitlines() if l.strip()]
        if len(lines) >= 2:
            return "\n".join(lines[1:])
    except Exception:
        pass
    return "Informação não disponível"

# ── Edite com as resoluções DO SEU MONITOR ─────────────────────────────────────
MINHAS_RESOLUCOES = [
    (1366, 768),
    (1280, 720),
    (1920, 1080),
    (1600, 900),
    (1440, 900),
    (1280, 800),
]

AUTOR   = "Thomaz Arthur"
VERSAO  = "1.0"

# ── GUI ────────────────────────────────────────────────────────────────────────
class App(tk.Tk):
    BG      = "#0d1117"
    PANEL   = "#161b22"
    BORDER  = "#30363d"
    GREEN   = "#238636"
    RED     = "#da3633"
    BLUE    = "#1f6feb"
    TEXT    = "#e6edf3"
    SUBTEXT = "#8b949e"
    YELLOW  = "#d29922"

    def __init__(self):
        super().__init__()
        self.title("Suporte Remoto — Ajuste de Resolução")
        self.resizable(False, False)
        self.configure(bg=self.BG)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.original_res = get_current_resolution()
        self.current_res  = self.original_res
        self.supported    = get_supported_resolutions()

        self._build()
        self._center()
        self._check_driver_warning()

    def _check_driver_warning(self):
        if len(self.supported) == 0:
            messagebox.showwarning("Driver de vídeo",
                "Nenhuma resolução foi detectada.\n\n"
                "Isso indica que o driver de vídeo está ausente ou corrompido.\n"
                "O script pode funcionar de forma limitada.")
        elif len(self.supported) <= 2:
            self._status("⚠  Poucas resoluções — driver pode estar desatualizado.", warn=True)

    def _build(self):
        # ── Banner ──
        banner = tk.Frame(self, bg=self.BLUE)
        banner.pack(fill="x")
        tk.Label(banner, text="🖥  SUPORTE REMOTO  —  Ajuste de Resolução",
            bg=self.BLUE, fg="white", font=("Segoe UI Semibold", 12),
            padx=16, pady=11, anchor="w").pack(fill="x")
        tk.Label(banner, text="Adapta a resolução desta máquina à tela do analista de suporte.",
            bg=self.BLUE, fg="#b8d4ff", font=("Segoe UI", 9),
            padx=16, anchor="w").pack(fill="x")
        tk.Frame(banner, bg="#1158b7", height=3).pack(fill="x", pady=(6, 0))

        # ── Info atual ──
        info = tk.Frame(self, bg=self.PANEL)
        info.pack(fill="x", padx=14, pady=(12, 0))
        tk.Label(info, text="Resolução original:", bg=self.PANEL, fg=self.SUBTEXT,
            font=("Consolas", 9), padx=10, pady=4, anchor="w").grid(row=0, column=0, sticky="w")
        self.lbl_orig = tk.Label(info, text=f"{self.original_res[0]} × {self.original_res[1]}",
            bg=self.PANEL, fg=self.YELLOW, font=("Consolas", 10, "bold"), padx=6)
        self.lbl_orig.grid(row=0, column=1, sticky="w")
        tk.Label(info, text="Resolução atual:", bg=self.PANEL, fg=self.SUBTEXT,
            font=("Consolas", 9), padx=10, pady=4, anchor="w").grid(row=1, column=0, sticky="w")
        self.lbl_cur = tk.Label(info, text=f"{self.current_res[0]} × {self.current_res[1]}",
            bg=self.PANEL, fg="#4fc3f7", font=("Consolas", 10, "bold"), padx=6)
        self.lbl_cur.grid(row=1, column=1, sticky="w")
        tk.Label(info, text="Resoluções disponíveis:", bg=self.PANEL, fg=self.SUBTEXT,
            font=("Consolas", 9), padx=10, pady=4, anchor="w").grid(row=2, column=0, sticky="w")
        count_color = self.RED if len(self.supported) <= 2 else self.GREEN
        tk.Label(info, text=str(len(self.supported)), bg=self.PANEL, fg=count_color,
            font=("Consolas", 10, "bold"), padx=6).grid(row=2, column=1, sticky="w")

        # ── Atalhos rápidos ──
        tk.Label(self, text="⚡  Resoluções do analista (acesso rápido):",
            bg=self.BG, fg=self.TEXT, font=("Segoe UI Semibold", 9),
            padx=14, anchor="w").pack(fill="x", pady=(12, 4))
        quick = tk.Frame(self, bg=self.BG)
        quick.pack(padx=14, fill="x")
        supported_set = {(w, h) for w, h in self.supported}
        for col, (w, h) in enumerate(MINHAS_RESOLUCOES):
            available = (w, h) in supported_set and test_resolution(w, h)
            color = self.GREEN if available else self.BORDER
            fg    = "white"    if available else self.SUBTEXT
            state = "normal"   if available else "disabled"
            tk.Button(quick, text=f"{w}×{h}", bg=color, fg=fg,
                font=("Consolas", 9, "bold"), relief="flat", bd=0,
                cursor="hand2" if available else "arrow", state=state,
                padx=10, pady=6, command=lambda ww=w, hh=h: self.apply_res(ww, hh)
            ).grid(row=0, column=col, padx=(0, 6), pady=2)

        # ── Lista completa ──
        tk.Label(self, text="📋  Todas as resoluções suportadas por esta máquina:",
            bg=self.BG, fg=self.TEXT, font=("Segoe UI Semibold", 9),
            padx=14, anchor="w").pack(fill="x", pady=(12, 4))
        list_frame = tk.Frame(self, bg=self.BG)
        list_frame.pack(padx=14, fill="both")
        sb = tk.Scrollbar(list_frame, orient="vertical")
        self.listbox = tk.Listbox(list_frame, yscrollcommand=sb.set,
            bg=self.PANEL, fg=self.TEXT, selectbackground=self.BLUE,
            selectforeground="white", font=("Consolas", 10),
            height=8, width=26, relief="flat", bd=0, activestyle="none")
        sb.config(command=self.listbox.yview)
        sb.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)
        self._fill_list()
        if not self.supported:
            self.listbox.insert("end", "  Nenhuma resolução detectada")

        # ── Botões principais ──
        btn_frame = tk.Frame(self, bg=self.BG)
        btn_frame.pack(fill="x", padx=14, pady=12)
        tk.Button(btn_frame, text="✔  Aplicar Selecionada", command=self.apply_from_list,
            bg=self.BLUE, fg="white", font=("Segoe UI", 10, "bold"),
            relief="flat", cursor="hand2", padx=12, pady=8, bd=0,
            activebackground="#1a5fc8", activeforeground="white"
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))
        tk.Button(btn_frame, text="↺  Restaurar Original", command=self.restore,
            bg=self.RED, fg="white", font=("Segoe UI", 10, "bold"),
            relief="flat", cursor="hand2", padx=12, pady=8, bd=0,
            activebackground="#b02a2a", activeforeground="white"
        ).pack(side="left", fill="x", expand=True)

        # ── Botões secundários ──
        sec_frame = tk.Frame(self, bg=self.BG)
        sec_frame.pack(fill="x", padx=14, pady=(0, 6))
        tk.Button(sec_frame, text="🔍  Driver de vídeo",
            command=self.show_driver_info,
            bg=self.PANEL, fg=self.SUBTEXT, font=("Segoe UI", 8),
            relief="flat", cursor="hand2", padx=8, pady=4, bd=0,
            activebackground=self.BORDER, activeforeground=self.TEXT
        ).pack(side="left")


        # ── Rodapé com assinatura ──
        footer = tk.Frame(self, bg="#21262d")
        footer.pack(fill="x", side="bottom")
        tk.Frame(footer, bg=self.BORDER, height=1).pack(fill="x")
        tk.Label(footer,
            text=f"Desenvolvido por  {AUTOR}  •  v{VERSAO}",
            bg="#21262d", fg="#444d56",
            font=("Segoe UI", 8), pady=5
        ).pack()

        # ── Status bar ──
        self.status_bar = tk.Label(self, text="✔  Pronto.", anchor="w",
            bg="#21262d", fg=self.SUBTEXT, font=("Segoe UI", 9), padx=12, pady=4)
        self.status_bar.pack(fill="x", side="bottom")

    # ── Actions ───────────────────────────────────────────────────────────────
    def apply_res(self, w, h):
        if (w, h) == self.current_res:
            self._status(f"ℹ  {w}×{h} já é a resolução atual.", warn=True); return
        if not test_resolution(w, h):
            self._status(f"✘  {w}×{h} não é aceita pelo driver desta máquina.", warn=True); return
        ok, erro = change_resolution(w, h)
        if ok:
            self.current_res = (w, h)
            self.lbl_cur.config(text=f"{w} × {h}")
            self._fill_list()
            self._status(f"✔  Resolução alterada para {w} × {h}.")
        else:
            self._status(f"✘  {erro}", warn=True)

    def apply_from_list(self):
        sel = self.listbox.curselection()
        if not sel or not self.supported:
            self._status("⚠  Selecione uma resolução na lista.", warn=True); return
        self.apply_res(*self.supported[sel[0]])

    def restore(self):
        w, h = self.original_res
        if (w, h) == self.current_res:
            self._status("ℹ  Resolução já está no valor original.", warn=True); return
        ok, erro = change_resolution(w, h)
        if ok:
            self.current_res = (w, h)
            self.lbl_cur.config(text=f"{w} × {h}")
            self._fill_list()
            self._status(f"✔  Resolução restaurada para {w} × {h}.")
        else:
            self._status(f"✘  Erro ao restaurar: {erro}", warn=True)

    def show_driver_info(self):
        messagebox.showinfo("Driver de Vídeo",
            f"Informações do adaptador de vídeo:\n\n{get_driver_info()}")

    def on_close(self):
        if self.current_res != self.original_res:
            if messagebox.askyesno("Restaurar resolução?",
                f"A resolução foi alterada para {self.current_res[0]}×{self.current_res[1]}.\n\n"
                "Deseja restaurar a resolução original antes de sair?"):
                change_resolution(*self.original_res)
        self.destroy()

    def _fill_list(self):
        self.listbox.delete(0, "end")
        for idx, (w, h) in enumerate(self.supported):
            tag = "  ← atual" if (w, h) == self.current_res else ""
            self.listbox.insert("end", f"  {w} × {h}{tag}")
            if (w, h) == self.current_res:
                self.listbox.selection_set(idx)
                self.listbox.see(idx)

    def _status(self, msg, warn=False):
        self.status_bar.config(text=msg, fg=self.YELLOW if warn else "#3fb950")

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth()  // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    if sys.platform != "win32":
        print("Este programa funciona apenas no Windows.")
        sys.exit(1)
    App().mainloop()
