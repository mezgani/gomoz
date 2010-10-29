; Gomoz web application security scanner
; Copyright (c) securfox <handrix@users.sourceforge.net>
;
; This program is free software; you can redistribute it and/or modify
; it under the terms of the GNU General Public License as published by
; the Free Software Foundation; either version 2 of the License, or
; (at your option) any later version.
;
; This program is distributed in the hope that it will be useful,
; but WITHOUT ANY WARRANTY; without even the implied warranty of
; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
; GNU General Public License for more details.
;
; You should have received a copy of the GNU General Public License
; along with this program; if not, write to the Free Software
; Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

[Setup]
AppName=gomoz
AppVerName=gomoz version 1.0
AppPublisher=SecurFox
DefaultGroupName=gomoz
AppPublisherURL = http://groups.google.com/gomoz
DefaultDirName={pf}\gomoz
LicenseFile = LICENCE.txt
WizardImageFile = wizard.bmp
UninstallDisplayIcon={app}\gmz.exe
SetupIconFile=unis.ico
Compression=lzma/ultra
SolidCompression=yes
OutputDir=.
OutputBaseFilename = gmz-setup


[Files]
Source: dist\main.exe; DestDir: {app}; Flags: ignoreversion
Source: gmz.ico; DestDir: {app}; Flags: ignoreversion
Source: unis.ico; DestDir: {app}; Flags: ignoreversion
;Source: library.zip; DestDir: {app}; Flags: ignoreversion
;Source: dist\MSVCR71.dll; DestDir: {app}; Flags: ignoreversion
;Source: dist\python25.dll; DestDir: {app}; Flags: ignoreversion
Source: dist\msvcp71.dll; DestDir: {app}; Flags: ignoreversion
;Source: D:\marnic\lib\cc\cc.py; DestDir: {app}; Flags: ignoreversion
;Source: w9xpopen.exe; DestDir: {app}; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files
Source: "README.txt"; DestDir: "{app}"; Flags: isreadme
;Source: "COPYING_LGPL.txt"; DestDir: "{app}"; Flags: ignoreversion
;Source: "COPYING_GPL.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "gmz.ico"; DestDir: "{app}"; Flags: ignoreversion

Source: log\gomoz.log; DestDir: {app}\log; Flags: ignoreversion
Source: config\gomoz.cfg; DestDir: {app}\config; Flags: ignoreversion


[Icons]
Name: "{group}\gomoz"; Filename: "{app}\main.exe";IconFilename: "{app}\gmz.ico"
Name: "{group}\Uninstall gomoz"; Filename: "{uninstallexe}"; IconFilename: "{app}\unis.ico"
;Name: "{group}\GPL License"; Filename: "{app}\COPYING_GPL.txt"
;Name: "{group}\LGPL License"; Filename: "{app}\COPYING_LGPL.txt"

[Messages]
StatusUninstalling=Uninstalling %1 thank you for runing gomoz.


