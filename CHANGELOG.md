# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-08-17

### Added
- Core application foundation using Python and Tkinter.
- File operations: New, Open, Save, Save As, Exit.
- Text editing operations: Search, Find & Replace.
- View operations: Zoom In, Zoom Out, Reset Zoom.
- Advanced text formatting: Font family, font size, bold, italic, underline, strikethrough, text color, highlight color.
- UI Layout: Menu bar, editor view, formatting toolbar, and a dynamic status bar.
- File Info dialog displaying system file statistics.
- Auto-save functionality.
- Persistent formatting settings (saved in user home directory).
- Initial PyInstaller configurations for macOS and Windows standalone packaging.
- Centralized `AppConfig` for application metadata and defaults.
- Centralized `ResourceManager` for handling PyInstaller paths and caching images.
- Distribution configurations for macOS DMG and Windows Inno Setup.
- Fixed an inheritance bug causing `StatusBar` configuration errors.
