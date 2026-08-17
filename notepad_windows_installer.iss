[Setup]
AppName=Notepad
AppVersion=1.0.0
AppPublisher=Notepad Developer
DefaultDirName={autopf}\Notepad
DefaultGroupName=Notepad
OutputBaseFilename=Notepad-v1.0.0-Windows-Setup
OutputDir=dist
Compression=lzma
SolidCompression=yes
UninstallDisplayIcon={app}\Notepad.exe
DisableProgramGroupPage=yes

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\Notepad.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Notepad"; Filename: "{app}\Notepad.exe"
Name: "{autodesktop}\Notepad"; Filename: "{app}\Notepad.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Notepad.exe"; Description: "{cm:LaunchProgram,Notepad}"; Flags: nowait postinstall skipifsilent
