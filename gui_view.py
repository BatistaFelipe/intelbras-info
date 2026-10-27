import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from typing import Callable

WINDOW_TITLE = "Intelbras Info"
WINDOW_SIZE = "560x760"

COLOR_BG = "#F2F2F2"
COLOR_FRAME = "#FFFFFF"
COLOR_PRIMARY = "#5B9BD5"
COLOR_SECONDARY = "#A9CCE3"
COLOR_DANGER = "#E74C3C"
COLOR_DATA = "#C0392B"
COLOR_HEADER = "#111111"
COLOR_ERROR = "#B03A2E"

FONT_TITLE = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 10)
FONT_TEXT = ("Consolas", 9)
FONT_HEADER_TAG = ("Segoe UI", 10, "bold")
FONT_BUTTON = ("Segoe UI", 10, "bold")


def _asset_path(filename: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / "assets" / filename


class GuiView:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=COLOR_BG)
        self._apply_window_icon()

        self._configure_styles()
        self._build_header()
        self._build_credentials_form()
        self._build_output_area()
        self._build_action_buttons()

    def bind_handlers(
        self,
        on_fetch: Callable[[], None],
        on_sync: Callable[[], None],
        on_reboot: Callable[[], None],
    ) -> None:
        self.fetch_button.configure(command=on_fetch)
        self.sync_button.configure(command=on_sync)
        self.reboot_button.configure(command=on_reboot)

    def get_inputs(self) -> tuple[str, str, str, str]:
        return (
            self.host_entry.get().strip(),
            self.port_entry.get().strip(),
            self.user_entry.get().strip(),
            self.password_entry.get(),
        )

    def set_buttons_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self.sync_button.configure(state=state)
        self.fetch_button.configure(state=state)
        self.reboot_button.configure(state=state)

    def clear_output(self) -> None:
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

    def write_section(self, title: str, body: str) -> None:
        self._append(f"{title}\n", "header")
        self._append(f"{'-' * len(title)}\n")
        self._append(f"{body.strip()}\n\n", "data")

    def write_error(self, title: str, message: str) -> None:
        self._append(f"{title}\n", "header")
        self._append(f"{'-' * len(title)}\n")
        self._append(f"Erro: {message}\n\n", "error")

    def show_warning(self, message: str) -> None:
        messagebox.showwarning(WINDOW_TITLE, message)

    def ask_confirm(self, message: str) -> bool:
        return messagebox.askyesno(WINDOW_TITLE, message)

    def schedule(self, func: Callable[[], None]) -> None:
        self.root.after(0, func)

    def _append(self, text: str, tag: str | None = None) -> None:
        self.output.configure(state="normal")
        if tag:
            self.output.insert("end", text, tag)
        else:
            self.output.insert("end", text)
        self.output.see("end")
        self.output.configure(state="disabled")

    def _apply_window_icon(self) -> None:
        ico_path = _asset_path("icon.ico")
        if ico_path.exists():
            try:
                self.root.iconbitmap(default=str(ico_path))
                return
            except tk.TclError:
                pass
        png_path = _asset_path("icon.png")
        if png_path.exists():
            try:
                self._icon_image = tk.PhotoImage(file=str(png_path))
                self.root.iconphoto(True, self._icon_image)
            except tk.TclError:
                pass

    def _configure_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Primary.TButton",
            background=COLOR_PRIMARY,
            foreground="white",
            font=FONT_BUTTON,
            padding=(10, 8),
            borderwidth=0,
        )
        style.map("Primary.TButton", background=[("active", "#4A82B5")])

        style.configure(
            "Secondary.TButton",
            background=COLOR_SECONDARY,
            foreground="#1B2631",
            font=FONT_BUTTON,
            padding=(10, 8),
            borderwidth=0,
        )
        style.map("Secondary.TButton", background=[("active", "#8EB4D1")])

        style.configure(
            "Danger.TButton",
            background=COLOR_DANGER,
            foreground="white",
            font=FONT_BUTTON,
            padding=(10, 8),
            borderwidth=0,
        )
        style.map("Danger.TButton", background=[("active", "#B83225")])

        style.configure("Form.TLabel", background=COLOR_BG, font=FONT_LABEL)

    def _build_header(self) -> None:
        header = tk.Frame(
            self.root,
            bg=COLOR_FRAME,
            highlightbackground="#111111",
            highlightthickness=2,
        )
        header.pack(fill="x", padx=20, pady=(20, 10))
        tk.Label(
            header,
            text="INTELBRAS INFO",
            font=FONT_TITLE,
            bg=COLOR_FRAME,
        ).pack(pady=10)

    def _build_credentials_form(self) -> None:
        form = tk.Frame(self.root, bg=COLOR_BG)
        form.pack(fill="x", padx=20, pady=5)
        form.columnconfigure(1, weight=3)
        form.columnconfigure(3, weight=1)

        ttk.Label(form, text="IP/DDNS", style="Form.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 6), pady=4
        )
        self.host_entry = ttk.Entry(form)
        self.host_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=4)

        ttk.Label(form, text="Porta", style="Form.TLabel").grid(
            row=0, column=2, sticky="w", padx=(0, 6), pady=4
        )
        self.port_entry = ttk.Entry(form, width=10)
        self.port_entry.grid(row=0, column=3, sticky="ew", pady=4)

        ttk.Label(form, text="Usuário", style="Form.TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 6), pady=4
        )
        self.user_entry = ttk.Entry(form)
        self.user_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=4)

        ttk.Label(form, text="Senha", style="Form.TLabel").grid(
            row=1, column=2, sticky="w", padx=(0, 6), pady=4
        )
        self.password_entry = ttk.Entry(form, show="*")
        self.password_entry.grid(row=1, column=3, sticky="ew", pady=4)

    def _build_output_area(self) -> None:
        container = tk.Frame(
            self.root,
            bg=COLOR_FRAME,
            highlightbackground="#B2B2B2",
            highlightthickness=1,
        )
        container.pack(fill="both", expand=True, padx=20, pady=10)

        self.output = ScrolledText(
            container,
            wrap="word",
            font=FONT_TEXT,
            bg=COLOR_FRAME,
            relief="flat",
        )
        self.output.pack(fill="both", expand=True, padx=4, pady=4)
        self.output.tag_configure(
            "header", font=FONT_HEADER_TAG, foreground=COLOR_HEADER
        )
        self.output.tag_configure("data", foreground=COLOR_DATA)
        self.output.tag_configure("error", foreground=COLOR_ERROR, font=FONT_HEADER_TAG)
        self.output.configure(state="disabled")

    def _build_action_buttons(self) -> None:
        buttons = tk.Frame(self.root, bg=COLOR_BG)
        buttons.pack(fill="x", padx=20, pady=(0, 20))

        self.fetch_button = ttk.Button(
            buttons,
            text="BUSCAR",
            style="Primary.TButton",
        )
        self.fetch_button.pack(fill="x", pady=4)

        self.sync_button = ttk.Button(
            buttons,
            text="SINCRONIZAR DATA E HORA",
            style="Secondary.TButton",
        )
        self.sync_button.pack(fill="x", pady=4)

        self.reboot_button = ttk.Button(
            buttons,
            text="REBOOT",
            style="Danger.TButton",
        )
        self.reboot_button.pack(fill="x", pady=4)
