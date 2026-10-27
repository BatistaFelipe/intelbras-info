# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Dual-interface Python tool (Tkinter GUI + argparse CLI) that queries and manages Intelbras intercom devices over HTTP Digest auth. Targets Windows: both entry points ship as PyInstaller onefile executables.

## Common commands

Use the project `.venv` for all Python work (Windows: `.venv/Scripts/activate`).

```bash
# install deps
python -m pip install -r requirements.txt

# run GUI from source
python gui_app.py

# run CLI from source (requires INTELBRAS_USER/INTELBRAS_PASSWORD in .env or env)
python cli_app.py -H 192.168.1.100:8085 -i

# build executables (prefer the versioned .spec files)
pyinstaller gui_app.spec    # produces dist/intelbras_info_gui.exe (windowed, icon-embedded)
pyinstaller cli_app.spec    # produces dist/intelbras_info.exe (console)

# format (black is the configured VSCode formatter, formats on save)
black .
```

There is no test suite yet — do not claim coverage you cannot verify.

## Architecture

The code is a strict MVC split and the GUI/CLI share the same model layer. Preserve that split when editing — views and controllers must not import `requests` or format URLs; the model must not import Tk or argparse.

- `model.py` — `Credentials` dataclass (`frozen=True`) and pure HTTP functions (`get_system_info`, `get_config_sip`, `get_current_time`, `set_current_time`, `reboot`). All requests use `HTTPDigestAuth` with a 30s timeout. URLs hit the device's `/cgi-bin/*.cgi` endpoints (Dahua-style magicBox/configManager/global APIs).
- `gui_view.py` — Tkinter widgets, styles, and output formatting. Exposes `bind_handlers`, `get_inputs`, `set_buttons_enabled`, `write_section`, `write_error`, `schedule` (which wraps `root.after`). No business logic.
- `gui_controller.py` — Validates inputs, builds `Credentials`, runs model calls on a background `threading.Thread` (daemon), and marshals results back to the Tk main loop via `view.schedule(...)`. All UI updates from worker threads must go through `schedule`.
- `gui_app.py` / `cli_app.py` — Thin entry points (`tk.Tk()` + wiring, or `cli_controller.run()`).
- `cli_controller.py` — `argparse` definition and dispatch. Loads `.env` via `_load_env()`, which looks next to `sys.executable` when `sys.frozen` is set (PyInstaller onefile) and falls back to CWD; this is why `.env` must live beside the `.exe` in installed deployments.

### Credentials conventions

- GUI collects host + port separately and the controller combines them as `f"{host}:{port}"` before constructing `Credentials`.
- CLI expects host in `IP:PORT` form via `-H`.
- Credentials are never persisted by the GUI; the CLI reads only from env/`.env`.

### Asset loading (PyInstaller-aware)

`gui_view._asset_path` resolves against `sys._MEIPASS` when bundled, else the source directory. The GUI spec embeds `assets/icon.ico`; keep new assets under `assets/` and ensure the spec's `datas` includes them if they must be bundled.

## Build & install flow (Windows)

`scripts/install.ps1` (invoked by `scripts/Install.bat` to bypass ExecutionPolicy) requires admin, copies an `intelbras-info/` folder into `C:\Program Files\`, appends it to the Machine `PATH`, and creates Desktop + Start Menu shortcuts pointing at `intelbras_info_gui.exe`. The installer expects a layout where `intelbras-info/` sits next to `Install.bat` and `install.ps1` — i.e. produced by placing the two built `.exe` files inside a folder named `intelbras-info/`.

## Repository notes

- Current working branch: `feat/windows-gui`. `main` is the default PR target.
- `black` version is pinned in `requirements.txt`; VSCode uses `ms-python.black-formatter` with format-on-save (4-space indent).
- The old `intelbras_info.py` monolith has been removed in favor of the MVC split — don't resurrect it.
