# ──────────────────────────────────────────────────────────────────────────────
#  RemoteResolution — Suporte Remoto
#  Desenvolvido por: Thomaz Arthur
# ──────────────────────────────────────────────────────────────────────────────

import sys
import tkinter as tk
from tkinter import messagebox

import driver_info
from win_display import (
    change_resolution,
    get_current_resolution,
    get_supported_resolutions,
    test_resolution,
)

# ── Edite com as resoluções DO SEU MONITOR ─────────────────────────────────────
MINHAS_RESOLUCOES = [
    (1024, 768),   # XGA
    (1152, 864),   # XGA+
    (1280, 720),   # HD
    (1280, 768),   # WXGA
    (1280, 800),   # WXGA 16:10
    (1280, 1024),  # SXGA
    (1366, 768),
    (1360, 768),
    (1400, 1050),  # SXGA+
    (1600, 900),
    (1600, 1200),  # UXGA
    (1680, 1050),  # WSXGA+
    (1920, 1080),  # Full HD
    (1920, 1200),  # WUXGA 16:10
    (2048, 1152),
    (2560, 1080),  # Ultrawide
    (2560, 1440),  # QHD
    (2560, 1600),  # WQXGA 16:10
    (3440, 1440),  # Ultrawide QHD
    (3840, 2160),  # 4K UHD
    (1440, 900),
]

PERFIS_RESOLUCAO = {
    "Padrão (recomendado)": MINHAS_RESOLUCOES,
    "Notebook/HD": [
        (1024, 768),
        (1152, 864),
        (1280, 720),
        (1280, 768),
        (1360, 768),
        (1366, 768),
        (1600, 900),
    ],
    "Full HD / 16:10": [
        (1280, 800),
        (1440, 900),
        (1680, 1050),
        (1920, 1080),
        (1920, 1200),
        (2048, 1152),
    ],
    "QHD / 4K / Ultrawide": [
        (2560, 1080),
        (2560, 1440),
        (2560, 1600),
        (3440, 1440),
        (3840, 2160),
    ],
}

SECOES_RESOLUCAO = [
    ("16:9", {(1280, 720), (1360, 768), (1366, 768), (1600, 900), (1920, 1080), (2048, 1152), (2560, 1440), (3840, 2160)}),
    ("16:10", {(1280, 800), (1440, 900), (1680, 1050), (1920, 1200), (2560, 1600)}),
    ("4:3 / 5:4", {(1024, 768), (1152, 864), (1280, 1024), (1400, 1050), (1600, 1200)}),
    ("Ultrawide", {(2560, 1080), (3440, 1440)}),
]

AUTOR = "Thomaz Arthur"
VERSAO = "1.1.1"

# ── GUI ────────────────────────────────────────────────────────────────────────
class App(tk.Tk):
    BG = "#0d1117"
    PANEL = "#161b22"
    BORDER = "#30363d"
    GREEN = "#238636"
    RED = "#da3633"
    BLUE = "#1f6feb"
    TEXT = "#e6edf3"
    SUBTEXT = "#8b949e"
    YELLOW = "#d29922"
    WIN_WIDTH = 760
    WIN_HEIGHT = 760

    def __init__(self):
        super().__init__()
        self.title("REMOTE SOLUTION")
        self.resizable(False, False)
        self.configure(bg=self.BG)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.original_res = get_current_resolution()
        self.current_res = self.original_res
        self.supported = get_supported_resolutions()
        self.supported_set = {(w, h) for w, h in self.supported}
        self.perfil_var = tk.StringVar(value="Padrão (recomendado)")

        self._build()
        self._center()
        self._check_driver_warning()

    def _check_driver_warning(self):
        if len(self.supported) == 0:
            messagebox.showwarning(
                "Driver de vídeo",
                "Nenhuma resolução foi detectada.\n\n"
                "Isso indica que o driver de vídeo está ausente ou corrompido.\n"
                "O script pode funcionar de forma limitada.",
            )
        elif len(self.supported) <= 2:
            self._status("⚠  Poucas resoluções — driver pode estar desatualizado.", warn=True)

    def _build(self):
        banner = tk.Frame(self, bg="#0a4ea3")
        banner.pack(fill="x")
        tk.Label(
            banner,
            text="REMOTE SOLUTION",
            bg="#0a4ea3",
            fg="white",
            font=("Segoe UI", 13, "bold"),
            padx=16,
            pady=9,
            anchor="w",
        ).pack(fill="x")
        tk.Frame(banner, bg="#083d80", height=2).pack(fill="x")

        info = tk.Frame(self, bg=self.PANEL)
        info.pack(fill="x", padx=14, pady=(12, 0))
        tk.Label(
            info,
            text="Resolução original:",
            bg=self.PANEL,
            fg=self.SUBTEXT,
            font=("Consolas", 9),
            padx=10,
            pady=4,
            anchor="w",
        ).grid(row=0, column=0, sticky="w")
        self.lbl_orig = tk.Label(
            info,
            text=f"{self.original_res[0]} × {self.original_res[1]}",
            bg=self.PANEL,
            fg=self.YELLOW,
            font=("Consolas", 10, "bold"),
            padx=6,
        )
        self.lbl_orig.grid(row=0, column=1, sticky="w")
        tk.Label(
            info,
            text="Resolução atual:",
            bg=self.PANEL,
            fg=self.SUBTEXT,
            font=("Consolas", 9),
            padx=10,
            pady=4,
            anchor="w",
        ).grid(row=1, column=0, sticky="w")
        self.lbl_cur = tk.Label(
            info,
            text=f"{self.current_res[0]} × {self.current_res[1]}",
            bg=self.PANEL,
            fg="#4fc3f7",
            font=("Consolas", 10, "bold"),
            padx=6,
        )
        self.lbl_cur.grid(row=1, column=1, sticky="w")
        tk.Label(
            info,
            text="Resoluções disponíveis:",
            bg=self.PANEL,
            fg=self.SUBTEXT,
            font=("Consolas", 9),
            padx=10,
            pady=4,
            anchor="w",
        ).grid(row=2, column=0, sticky="w")
        count_color = self.RED if len(self.supported) <= 2 else self.GREEN
        tk.Label(
            info,
            text=str(len(self.supported)),
            bg=self.PANEL,
            fg=count_color,
            font=("Consolas", 10, "bold"),
            padx=6,
        ).grid(row=2, column=1, sticky="w")

        tk.Label(
            self,
            text="⚡  Resoluções do analista (acesso rápido):",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI Semibold", 9),
            padx=14,
            anchor="w",
        ).pack(fill="x", pady=(12, 4))
        perfil_row = tk.Frame(self, bg=self.BG)
        perfil_row.pack(fill="x", padx=14, pady=(0, 6))
        tk.Label(
            perfil_row,
            text="Perfil de atalhos:",
            bg=self.BG,
            fg=self.SUBTEXT,
            font=("Segoe UI", 9),
        ).pack(side="left")
        perfil_menu = tk.OptionMenu(perfil_row, self.perfil_var, *PERFIS_RESOLUCAO.keys(), command=lambda _: self._render_quick_buttons())
        perfil_menu.config(
            bg=self.PANEL,
            fg=self.TEXT,
            activebackground=self.BORDER,
            activeforeground=self.TEXT,
            highlightthickness=0,
            bd=0,
            relief="flat",
            font=("Segoe UI", 9),
        )
        perfil_menu["menu"].config(bg=self.PANEL, fg=self.TEXT, activebackground=self.BLUE, activeforeground="white")
        perfil_menu.pack(side="left", padx=(8, 0))

        quick = tk.Frame(self, bg=self.BG)
        quick.pack(padx=14, fill="x")
        self.quick = quick
        self._render_quick_buttons()

        tk.Label(
            self,
            text="📋  Todas as resoluções suportadas por esta máquina:",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI Semibold", 9),
            padx=14,
            anchor="w",
        ).pack(fill="x", pady=(12, 4))
        list_frame = tk.Frame(self, bg=self.BG)
        list_frame.pack(padx=14, fill="both")
        sb = tk.Scrollbar(list_frame, orient="vertical")
        self.listbox = tk.Listbox(
            list_frame,
            yscrollcommand=sb.set,
            bg=self.PANEL,
            fg=self.TEXT,
            selectbackground=self.BLUE,
            selectforeground="white",
            font=("Consolas", 10),
            height=8,
            width=26,
            relief="flat",
            bd=0,
            activestyle="none",
        )
        sb.config(command=self.listbox.yview)
        sb.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)
        self._fill_list()
        if not self.supported:
            self.listbox.insert("end", "  Nenhuma resolução detectada")

        btn_frame = tk.Frame(self, bg=self.BG)
        btn_frame.pack(fill="x", padx=14, pady=12)
        tk.Button(
            btn_frame,
            text="✔  Aplicar Selecionada",
            command=self.apply_from_list,
            bg=self.BLUE,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8,
            bd=0,
            activebackground="#1a5fc8",
            activeforeground="white",
        ).pack(side="left", fill="x", expand=True, padx=(0, 6))
        tk.Button(
            btn_frame,
            text="↺  Restaurar Original",
            command=self.restore,
            bg=self.RED,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8,
            bd=0,
            activebackground="#b02a2a",
            activeforeground="white",
        ).pack(side="left", fill="x", expand=True)

        sec_frame = tk.Frame(self, bg=self.BG)
        sec_frame.pack(fill="x", padx=14, pady=(0, 6))
        tk.Button(
            sec_frame,
            text="🔍  Driver de vídeo",
            command=self.show_driver_info,
            bg=self.PANEL,
            fg=self.SUBTEXT,
            font=("Segoe UI", 8),
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=4,
            bd=0,
            activebackground=self.BORDER,
            activeforeground=self.TEXT,
        ).pack(side="left")

        footer = tk.Frame(self, bg="#21262d")
        footer.pack(fill="x", side="bottom")
        tk.Frame(footer, bg=self.BORDER, height=1).pack(fill="x")
        footer_row = tk.Frame(footer, bg="#21262d")
        footer_row.pack(fill="x", pady=5)
        tk.Label(
            footer_row,
            text=f"Desenvolvido por  {AUTOR}  •  v{VERSAO}",
            bg="#21262d",
            fg="#444d56",
            font=("Segoe UI", 8),
            anchor="w",
        ).pack(side="left")

        self.status_bar = tk.Label(
            self,
            text="✔  Pronto.",
            anchor="w",
            bg="#21262d",
            fg=self.SUBTEXT,
            font=("Segoe UI", 9),
            padx=12,
            pady=4,
        )
        self.status_bar.pack(fill="x", side="bottom")

    def apply_res(self, w, h):
        if (w, h) == self.current_res:
            self._status(f"ℹ  {w}×{h} já é a resolução atual.", warn=True)
            return
        if not test_resolution(w, h):
            self._status(f"✘  {w}×{h} não é aceita pelo driver desta máquina.", warn=True)
            return
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
            self._status("⚠  Selecione uma resolução na lista.", warn=True)
            return
        self.apply_res(*self.supported[sel[0]])

    def restore(self):
        w, h = self.original_res
        if (w, h) == self.current_res:
            self._status("ℹ  Resolução já está no valor original.", warn=True)
            return
        ok, erro = change_resolution(w, h)
        if ok:
            self.current_res = (w, h)
            self.lbl_cur.config(text=f"{w} × {h}")
            self._fill_list()
            self._status(f"✔  Resolução restaurada para {w} × {h}.")
        else:
            self._status(f"✘  Erro ao restaurar: {erro}", warn=True)

    def show_driver_info(self):
        messagebox.showinfo("Driver de Vídeo", f"Informações do adaptador de vídeo:\n\n{driver_info.get_driver_info()}")

    def on_close(self):
        if self.current_res != self.original_res:
            if messagebox.askyesno(
                "Restaurar resolução?",
                f"A resolução foi alterada para {self.current_res[0]}×{self.current_res[1]}.\n\n"
                "Deseja restaurar a resolução original antes de sair?",
            ):
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
        w, h = self.WIN_WIDTH, self.WIN_HEIGHT
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _render_quick_buttons(self):
        for widget in self.quick.winfo_children():
            widget.destroy()

        perfil = self.perfil_var.get()
        resolutions = PERFIS_RESOLUCAO.get(perfil, MINHAS_RESOLUCOES)
        if not resolutions:
            return

        grouped = {name: [] for name, _ in SECOES_RESOLUCAO}
        grouped["Outras"] = []

        for item in resolutions:
            assigned = False
            for sec_name, sec_set in SECOES_RESOLUCAO:
                if item in sec_set:
                    grouped[sec_name].append(item)
                    assigned = True
                    break
            if not assigned:
                grouped["Outras"].append(item)

        row = 0
        for sec_name, _ in SECOES_RESOLUCAO:
            section_res = grouped.get(sec_name, [])
            if not section_res:
                continue
            tk.Label(
                self.quick,
                text=sec_name,
                bg=self.BG,
                fg=self.SUBTEXT,
                font=("Segoe UI Semibold", 8),
                anchor="w",
            ).grid(row=row, column=0, sticky="w", pady=(4, 2))
            row += 1
            col = 0
            for w, h in section_res:
                available = (w, h) in self.supported_set and test_resolution(w, h)
                color = self.GREEN if available else self.BORDER
                fg = "white" if available else self.SUBTEXT
                state = "normal" if available else "disabled"
                tk.Button(
                    self.quick,
                    text=f"{w}×{h}",
                    bg=color,
                    fg=fg,
                    font=("Consolas", 9, "bold"),
                    relief="flat",
                    bd=0,
                    cursor="hand2" if available else "arrow",
                    state=state,
                    padx=10,
                    pady=6,
                    command=lambda ww=w, hh=h: self.apply_res(ww, hh),
                ).grid(row=row, column=col, padx=(0, 6), pady=(0, 6), sticky="w")
                col += 1
                if col >= 5:
                    row += 1
                    col = 0
            row += 1

        if grouped["Outras"]:
            tk.Label(
                self.quick,
                text="Outras",
                bg=self.BG,
                fg=self.SUBTEXT,
                font=("Segoe UI Semibold", 8),
                anchor="w",
            ).grid(row=row, column=0, sticky="w", pady=(4, 2))
            row += 1
            for col, (w, h) in enumerate(grouped["Outras"]):
                available = (w, h) in self.supported_set and test_resolution(w, h)
                color = self.GREEN if available else self.BORDER
                fg = "white" if available else self.SUBTEXT
                state = "normal" if available else "disabled"
                tk.Button(
                    self.quick,
                    text=f"{w}×{h}",
                    bg=color,
                    fg=fg,
                    font=("Consolas", 9, "bold"),
                    relief="flat",
                    bd=0,
                    cursor="hand2" if available else "arrow",
                    state=state,
                    padx=10,
                    pady=6,
                    command=lambda ww=w, hh=h: self.apply_res(ww, hh),
                ).grid(row=row, column=col, padx=(0, 6), pady=(0, 6), sticky="w")


def main():
    if sys.platform != "win32":
        print("Este programa funciona apenas no Windows.")
        sys.exit(1)
    import ctypes

    # Evita agrupar com outras janelas do python.exe e ajuda a barra de tarefas a usar o ícone da janela.
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "ThomazArthur.RemoteResolution.RemoteSolution.1"
        )
    except Exception:
        pass

    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    App().mainloop()


if __name__ == "__main__":
    main()
