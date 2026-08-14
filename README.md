# Notepad

A lightweight Python desktop notepad application with modular services and a simple GUI.

## Description

This project implements a small text editor designed for learning and extension. It separates concerns into UI components, services, and data models so features can be added or replaced easily.

## Features

- **Text Editing:** Core editor UI for creating and editing plain text documents.
- **File Management:** Open, save, and save-as functionality implemented via services/file_service.py.
- **Formatting Support:** Formatting toolbar and services/format_service.py to apply configurable formatting settings (see `format_settings.json`).
- **Keyboard Shortcuts:** Centralized shortcuts handling in services/shortcuts_service.py.
- **Document Statistics:** Tracks statistics (word/line counts) via models/document_statistics.py and services/statistics_service.py.
- **Save Dialog:** Save dialog view implemented in ui/dialogs/save_dialog_view.py with a base dialog in ui/dialogs/base_dialog.py.
- **Zoom Controls:** Zoom in/out support via services/zoom_service.py.
- **System Integration:** System-level helpers in services/system_service.py.
- **Status Bar & Menu:** UI elements for status and menu located in ui/status_bar.py and ui/menu.py.
- **Modular Architecture:** Clear separation between `ui/`, `services/`, and `models/` for maintainability.

## Installation

1. Install Python 3.10+.
2. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies if any (none are required by default).

## Running

Run the application using:

```bash
python main.py
```

or

```bash
python app.py
```

## Project Structure (high level)

- `main.py`, `app.py` — application entry points
- `ui/` — UI components: `editor.py`, `format_toolbar.py`, `menu.py`, `status_bar.py`, `dialogs/`
- `services/` — application services: `file_service.py`, `format_service.py`, `shortcuts_service.py`, `statistics_service.py`, `system_service.py`, `zoom_service.py`
- `models/` — data models: `document_state.py`, `document_statistics.py`
- `format_settings.json` — formatting defaults

## Contributing

Contributions welcome. Open an issue or create a pull request describing the change.

## License

Specify your preferred license here (e.g., MIT). 
