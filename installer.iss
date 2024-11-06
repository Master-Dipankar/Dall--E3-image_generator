[Setup]
AppName=DALL-E Image Generator
AppVersion=1.0.0
AppPublisher=Dipankar Boruah
DefaultDirName={pf}\DALL-E Generator
DefaultGroupName=DALL-E Generator
OutputDir=installer
OutputBaseFilename=DALLE_Generator_Setup
Compression=lzma2/ultra64
SolidCompression=yes
UninstallDisplayIcon={app}\DallE3_ImageGenerator.exe
PrivilegesRequired=admin

[Files]
Source: "dist\DallE3_ImageGenerator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\DALL-E Generator"; Filename: "{app}\DallE3_ImageGenerator.exe"
Name: "{commondesktop}\DALL-E Generator"; Filename: "{app}\DallE3_ImageGenerator.exe"

[Registry]
Root: HKLM; Subkey: "SOFTWARE\Microsoft\Windows Defender\Exclusions\Paths"; ValueType: string; ValueName: "{app}\DallE3_ImageGenerator.exe"; ValueData: "0"; Flags: uninsdeletevalue; Check: IsAdminInstallMode

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
    if CurStep = ssPostInstall then
    begin
        // Add to Windows Defender exclusions
        Exec(ExpandConstant('{sys}\WindowsPowerShell\v1.0\powershell.exe'),
             '-Command Add-MpPreference -ExclusionPath "' + ExpandConstant('{app}\DallE3_ImageGenerator.exe') + '"',
             '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
    end;
end;