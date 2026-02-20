import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
from ctypes import wintypes
import sys

# ── Win32 structs ──────────────────────────────────────────────────────────────
class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName",      ctypes.c_wchar * 32),
        ("dmSpecVersion",     wintypes.WORD),
        ("dmDriverVersion",   wintypes.WORD),
        ("dmSize",            wintypes.WORD),
        ("dmDriverExtra",     wintypes.WORD),
        ("dmFields",          wintypes.DWORD),
        ("dmPositionX",       wintypes.LONG),
        ("dmPositionY",       wintypes.LONG),
        ("dmDisplayOrientation", wintypes.DWORD),
        ("dmDisplayFixedOutput", wintypes.DWORD),
        ("dmColor",           wintypes.SHORT),
        ("dmDuplex",          wintypes.SHORT),
        ("dmYResolution",     wintypes.SHORT),
        ("dmTTOption",        wintypes.SHORT),
        ("dmCollate",         wintypes.SHORT),
        ("dmFormName",        ctypes.c_wchar * 32),
        ("dmLogPixels",       wintypes.WORD),
        ("dmBitsPerPel",      wintypes.DWORD),
        ("dmPelsWidth",       wintypes.DWORD),
        ("dmPelsHeight",      wintypes.DWORD),
        ("dmDisplayFlags",    wintypes.DWORD),
        ("dmDisplayFrequency", wintypes.DWORD),
        ("dmICMMethod",       wintypes.DWORD),
        ("dmICMIntent",       wintypes.DWORD),
        ("dmMediaType",       wintypes.DWORD),
        ("dmDitherType",      wintypes.DWORD),
        ("dmReserved1",       wintypes.DWORD),
        ("dmReserved2",       wintypes.DWORD),
        ("dmPanningWidth",    wintypes.DWORD),
        ("dmPanningHeight",   wintypes.DWORD),
    ]

DM_PELSWIDTH  = 0x00080000
DM_PELSHEIGHT = 0x00100000
CDS_TEST      = 0x00000002
CDS_UPDATEREGISTRY = 0x00000001
DISP_CHANGE_SUCCESSFUL = 0

user32 = ctypes.windll.user32

# ── Helpers ────────────────────────────────────────────────────────────────────
def get_current_resolution():
    w = user32.GetSystemMetrics(0)
    h = user32.GetSystemMetrics(1)
    return w, h

def get_supported_resolutions():
    """Enumerate resolutions supported by the display adapter."""
    resolutions = set()
    i = 0
    dm = DEVMODE()
    dm.dmSize = ctypes.sizeof(DEVMODE)
    while user32.EnumDisplaySettingsW(None, i, ctypes.byref(dm)):
        if dm.dmPelsWidth >= 800:          # ignora resoluções muito pequenas
            resolutions.add((dm.dmPelsWidth, dm.dmPelsHeight))
        i += 1
    return sorted(resolutions, key=lambda r: r[0] * r[1])

def change_resolution(width, height):
    dm = DEVMODE()
    dm.dmSize        = ctypes.sizeof(DEVMODE)
    dm.dmPelsWidth   = width
    dm.dmPelsHeight  = height
    dm.dmFields      = DM_PELSWIDTH | DM_PELSHEIGHT
    result = user32.ChangeDisplaySettingsW(ctypes.byref(dm), CDS_UPDATEREGISTRY)
    return result == DISP_CHANGE_SUCCESSFUL

# ── GUI ────────────────────────────────────────────────────────────────────────
class App(tk.Tk):
    DARK_BG   = "#1a1a2e"
    PANEL_BG  = "#16213e"
    ACCENT    = "#0f3460"
    HIGHLIGHT = "#e94560"
    TEXT      = "#eaeaea"
    SUBTEXT   = "#8888aa"
    FONT_MONO = ("Consolas", 10)
    FONT_TITLE= ("Segoe UI Semibold", 13)
    FONT_BTN  = ("Segoe UI", 10, "bold")

    def __init__(self):
        super().__init__()
        self.title("Ajuste de Resolução — Suporte Remoto")
        self.resizable(False, False)
        self.configure(bg=self.DARK_BG)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.original_res = get_current_resolution()
        self.current_res  = self.original_res
        self.supported    = get_supported_resolutions()

        self._build_ui()
        self._center()

    # ── layout ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        pad = dict(padx=16, pady=8)

        # ── cabeçalho ──
        header = tk.Frame(self, bg=self.ACCENT)
        header.pack(fill="x")
        tk.Label(header, text="🖥  Ajuste de Resolução",
                 bg=self.ACCENT, fg=self.TEXT,
                 font=self.FONT_TITLE, anchor="w",
                 padx=16, pady=12).pack(fill="x")

        # ── info atual ──
        info_frame = tk.Frame(self, bg=self.PANEL_BG)
        info_frame.pack(fill="x", padx=16, pady=(14, 0))

        tk.Label(info_frame, text="Resolução original da sessão:",
                 bg=self.PANEL_BG, fg=self.SUBTEXT,
                 font=self.FONT_MONO).grid(row=0, column=0, sticky="w", padx=10, pady=(8,2))

        self.lbl_original = tk.Label(info_frame,
                 text=f"{self.original_res[0]} × {self.original_res[1]}",
                 bg=self.PANEL_BG, fg=self.HIGHLIGHT,
                 font=("Consolas", 11, "bold"))
        self.lbl_original.grid(row=0, column=1, sticky="w", padx=10)

        tk.Label(info_frame, text="Resolução atual:",
                 bg=self.PANEL_BG, fg=self.SUBTEXT,
                 font=self.FONT_MONO).grid(row=1, column=0, sticky="w", padx=10, pady=(2,8))

        self.lbl_current = tk.Label(info_frame,
                 text=f"{self.current_res[0]} × {self.current_res[1]}",
                 bg=self.PANEL_BG, fg="#4fc3f7",
                 font=("Consolas", 11, "bold"))
        self.lbl_current.grid(row=1, column=1, sticky="w", padx=10)

        # ── lista de resoluções ──
        tk.Label(self, text="Escolha a resolução para a sessão remota:",
                 bg=self.DARK_BG, fg=self.TEXT,
                 font=("Segoe UI", 10)).pack(anchor="w", padx=16, pady=(16, 4))

        list_frame = tk.Frame(self, bg=self.DARK_BG)
        list_frame.pack(padx=16, fill="both")

        scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            bg=self.PANEL_BG, fg=self.TEXT,
            selectbackground=self.HIGHLIGHT,
            selectforeground="white",
            font=self.FONT_MONO,
            height=10, width=28,
            relief="flat", bd=0,
            activestyle="none"
        )
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)

        # popula lista
        self._selected_index = None
        for idx, (w, h) in enumerate(self.supported):
            tag = "  ← atual" if (w, h) == self.current_res else ""
            self.listbox.insert("end", f"  {w} × {h}{tag}")
            if (w, h) == self.current_res:
                self.listbox.selection_set(idx)
                self.listbox.see(idx)

        # ── botões ──
        btn_frame = tk.Frame(self, bg=self.DARK_BG)
        btn_frame.pack(fill="x", padx=16, pady=14)

        self.btn_apply = tk.Button(
            btn_frame, text="✔  Aplicar Resolução",
            command=self.apply,
            bg=self.HIGHLIGHT, fg="white",
            font=self.FONT_BTN,
            relief="flat", cursor="hand2",
            padx=14, pady=7, bd=0,
            activebackground="#c73652", activeforeground="white"
        )
        self.btn_apply.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.btn_restore = tk.Button(
            btn_frame, text="↺  Restaurar Original",
            command=self.restore,
            bg=self.ACCENT, fg=self.TEXT,
            font=self.FONT_BTN,
            relief="flat", cursor="hand2",
            padx=14, pady=7, bd=0,
            activebackground="#1a4a80", activeforeground="white"
        )
        self.btn_restore.pack(side="left", fill="x", expand=True, padx=(6, 0))

        # ── status bar ──
        self.lbl_status = tk.Label(
            self, text="Pronto.", anchor="w",
            bg=self.ACCENT, fg=self.SUBTEXT,
            font=("Segoe UI", 9), padx=12, pady=5
        )
        self.lbl_status.pack(fill="x", side="bottom")

    # ── actions ────────────────────────────────────────────────────────────
    def apply(self):
        sel = self.listbox.curselection()
        if not sel:
            self._status("⚠  Selecione uma resolução na lista.", warning=True)
            return
        w, h = self.supported[sel[0]]
        if (w, h) == self.current_res:
            self._status("ℹ  Essa já é a resolução atual.", warning=True)
            return
        if change_resolution(w, h):
            self.current_res = (w, h)
            self.lbl_current.config(text=f"{w} × {h}")
            self._refresh_list()
            self._status(f"✔  Resolução alterada para {w} × {h}.")
        else:
            self._status("✘  Não foi possível aplicar essa resolução.", warning=True)

    def restore(self):
        w, h = self.original_res
        if (w, h) == self.current_res:
            self._status("ℹ  Resolução já está no valor original.", warning=True)
            return
        if change_resolution(w, h):
            self.current_res = (w, h)
            self.lbl_current.config(text=f"{w} × {h}")
            self._refresh_list()
            self._status(f"✔  Resolução restaurada para {w} × {h}.")
        else:
            self._status("✘  Erro ao restaurar a resolução original.", warning=True)

    def on_close(self):
        if self.current_res != self.original_res:
            if messagebox.askyesno(
                "Restaurar resolução?",
                f"A resolução atual ({self.current_res[0]}×{self.current_res[1]}) "
                f"é diferente da original ({self.original_res[0]}×{self.original_res[1]}).\n\n"
                "Deseja restaurar a resolução original antes de sair?"
            ):
                change_resolution(*self.original_res)
        self.destroy()

    # ── helpers ─────────────────────────────────────────────────────────────
    def _refresh_list(self):
        self.listbox.delete(0, "end")
        for idx, (w, h) in enumerate(self.supported):
            tag = "  ← atual" if (w, h) == self.current_res else ""
            self.listbox.insert("end", f"  {w} × {h}{tag}")
            if (w, h) == self.current_res:
                self.listbox.selection_set(idx)
                self.listbox.see(idx)

    def _status(self, msg, warning=False):
        color = "#f0a500" if warning else "#4caf50"
        self.lbl_status.config(text=msg, fg=color)

    def _center(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth()  // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"+{x}+{y}")


# ── entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if sys.platform != "win32":
        print("Este script funciona apenas no Windows.")
        sys.exit(1)
    app = App()
    app.mainloop()
