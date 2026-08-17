#!/bin/bash

# Exit on error
set -e

APP_NAME="Notepad"
VERSION="1.0.0"
DMG_NAME="${APP_NAME}-v${VERSION}-macOS.dmg"
APP_SOURCE="dist/${APP_NAME}.app"

echo "Checking for ${APP_SOURCE}..."
if [ ! -d "${APP_SOURCE}" ]; then
    echo "Error: ${APP_SOURCE} not found. Run 'pyinstaller notepad_macos.spec' first."
    exit 1
fi

echo "Removing old DMG if it exists..."
rm -f "dist/${DMG_NAME}"

echo "Creating DMG..."
hdiutil create -volname "${APP_NAME} Installer" -srcfolder "${APP_SOURCE}" -ov -format UDZO "dist/${DMG_NAME}"

echo "Success! DMG created at dist/${DMG_NAME}"
