; FileTreeViewer.iss
[Setup]
AppName=FileTreeViewer
AppVersion=1.0
DefaultDirName={autopf}\FileTreeViewer
DefaultGroupName=FileTreeViewer
OutputBaseFilename=FileTreeViewerInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\FileTreeViewer\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\FileTreeViewer"; Filename: "{app}\FileTreeViewer.exe"
Name: "{commondesktop}\FileTreeViewer"; Filename: "{app}\FileTreeViewer.exe"

[Run]
Filename: "{app}\FileTreeViewer.exe"; Description: "Launch FileTreeViewer"; Flags: nowait postinstall skipifsilent
