# Python Tkinter Notepad

A lightweight, fully-featured Python desktop notepad application with modular services, built on `Tkinter`. 

## 🌟 Features
- **Text Editing:** Standard text entry with undo/redo capabilities.
- **File Management:** Open, Save, Save As, and Print files.
- **Advanced Formatting:** Customize font family, size, bold, italic, underline, strikethrough, text color, and highlight colors.
- **Search & Replace:** Find text and perform case-insensitive replacements.
- **Zooming:** Dynamic zoom in/out with UI scaling (50% to 400%).
- **Document Statistics:** Real-time tracking of character count, word count, line count, and cursor position (Line/Col).
- **Auto-Save:** Configurable background auto-save.
- **Configurable:** Centralized `AppConfig` and persistent formatting settings saving your preferences automatically.

## 💻 Supported Platforms
- **macOS** 10.15+ (Catalina and newer)
- **Windows** 10 and 11
- **Linux** (Source code execution only)

## ⌨️ Keyboard Shortcuts
| Action | Windows / Linux | macOS |
| --- | --- | --- |
| **New File** | `Ctrl + N` | `Cmd + N` |
| **Open File** | `Ctrl + O` | `Cmd + O` |
| **Save** | `Ctrl + S` | `Cmd + S` |
| **Save As** | `Ctrl + Shift + S` | `Cmd + Shift + S` |
| **Find** | `Ctrl + F` | `Cmd + F` |
| **Replace** | `Ctrl + H` | `Cmd + Option + F` |
| **Zoom In** | `Ctrl + +` | `Cmd + +` |
| **Zoom Out** | `Ctrl + -` | `Cmd + -` |
| **Reset Zoom**| `Ctrl + 0` | `Cmd + 0` |

## 🚀 Installation & Usage

### 🍎 macOS
1. Download `Notepad-v1.0.0-macOS.dmg` from the **Releases** page.
2. Open the `.dmg` file and drag **Notepad.app** to your Applications folder.
3. Launch from Applications. 
*(Note: If blocked by Gatekeeper, right-click and select "Open")*.

### 🪟 Windows
1. Download `Notepad-v1.0.0-Windows-Setup.exe` from the **Releases** page.
2. Run the installer and follow the prompt.
3. Launch via the Desktop or Start Menu shortcut.

### 🐍 From Source
1. Install Python 3.10+.
2. Clone the repository and run:
```bash
python main.py
```

## ⚠️ Known Limitations
- The application does not currently support multi-tab editing (one document per window).
- Large files (> 10MB) may experience slight syntax/line-counting lag due to Tkinter limitations.
- Rich Text formats (`.rtf`, `.docx`) are not supported; the app works purely with plain-text (`.txt`).

## 🏗 Build & Release
This project uses PyInstaller and GitHub Actions for packaging. 

**macOS:**
Run `pyinstaller notepad_macos.spec`, followed by `./build_macos_dmg.sh` to compile the app bundle and DMG.

**Windows:**
Run `pyinstaller notepad_windows.spec`, then compile `notepad_windows_installer.iss` using Inno Setup.

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
