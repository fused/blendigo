;--------------------------------

; Use Modern UI
!include "MUI2.nsh"

;--------------------------------

; Setup Blendigo parameters
!define BLENDIGO_VERSION $%BLENDIGO_VERSION%
;!define BLENDER_VERSION $%BLENDER_VERSION%

; The name of the installer
Name "Blendigo ${BLENDIGO_VERSION} for Blender"

; The file to write
OutFile "blendigo-${BLENDIGO_VERSION}-installer.exe"

;--------------------------------
; New style GUI setup

; Colors and images
!define MUI_ICON "indigo.ico"
!define MUI_UNICON "indigo.ico"

!define MUI_PAGE_HEADER_TEXT "Blendigo Installation"
!define MUI_PAGE_HEADER_SUBTEXT "Version ${BLENDIGO_VERSION} for Blender"

LangString MUI_TEXT_DIRECTORY_TITLE ${LANG_ENGLISH} "Blendigo Installation"
LangString MUI_TEXT_DIRECTORY_SUBTITLE ${LANG_ENGLISH} "Version ${BLENDIGO_VERSION} for Blender"

LangString MUI_TEXT_INSTALLING_TITLE ${LANG_ENGLISH} "Blendigo Installation"
LangString MUI_TEXT_INSTALLING_SUBTITLE ${LANG_ENGLISH} "Version ${BLENDIGO_VERSION} for Blender"

!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "indigo_logo_150_57.bmp"
!define MUI_HEADERIMAGE_BITMAP_NOSTRETCH
!define MUI_HEADERIMAGE_UNBITMAP "indigo_logo_150_57.bmp"
!define MUI_HEADERIMAGE_UNBITMAP_NOSTRETCH

!define MUI_BGCOLOR "333333"
!define MUI_HEADER_TRANSPARENT_TEXT
!define MUI_LICENSEPAGE_BGCOLOR  "FFFFFF 333333"
!define MUI_INSTFILESPAGE_COLORS "FFFFFF 333333"

; These functions are called prior to the page macros below
Function "changeWelcomeTextColor"
	FindWindow $1 "#32770" "" $HWNDPARENT
	GetDlgItem $2 $1 1201
	SetCtlColors $2 0xFFFFFF 0x333333
	GetDlgItem $2 $1 1202
	SetCtlColors $2 0xFFFFFF 0x333333
FunctionEnd

Function "changeTitleColor"
	GetDlgItem $r3 $HWNDPARENT 1037
	SetCtlColors $r3 0xFFFFFF 0x333333
	GetDlgItem $r3 $HWNDPARENT 1038
	SetCtlColors $r3 0xFFFFFF 0x333333
FunctionEnd

; Installer behaviour
!define MUI_ABORTWARNING
!define MUI_UNABORTWARNING

; Welcome page
!define MUI_WELCOMEFINISHPAGE_BITMAP "indigo_logo_163_314.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP_NOSTRETCH
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "indigo_logo_163_314.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP_NOSTRETCH
!define MUI_WELCOMEPAGE_TITLE "Blendigo ${BLENDIGO_VERSION} for Blender"
!define MUI_WELCOMEPAGE_TEXT "This installer will first attempt to auto-locate your Blender installation folder. If the folder is not found, you will be asked to locate Blender yourself."

; License page
!define MUI_LICENSEPAGE_RADIOBUTTONS

; Directory page
!define MUI_DIRECTORYPAGE_TEXT_TOP "Choose the Blendigo installation directory.$\n$\nNote: Must be the directory of the version you intend to install for, e.g. .../Blender/2.72 ."

; Installation page
!define MUI_INSTFILESPAGE_FINISHHEADER_TEXT "Blendigo ${BLENDIGO_VERSION} for Blender Installation Complete"
!define MUI_INSTFILESPAGE_ABORTHEADER_TEXT "Blendigo ${BLENDIGO_VERSION} for Blender Installation Aborted"

;--------------------------------

; Request application privileges for Windows Vista
; We will request admin level privileges, so that we can write to the Program Files dir if needed.
RequestExecutionLevel admin

;--------------------------------

Function DetectInstallPath
	IfFileExists "$APPDATA\Blender Foundation\Blender\2.72" 0 AppData2_71
		CreateDirectory "$APPDATA\Blender Foundation\Blender\2.72\scripts\addons"
		StrCpy $INSTDIR "$APPDATA\Blender Foundation\Blender\2.72"
		Return
		
	AppData2_71:
	IfFileExists "$APPDATA\Blender Foundation\Blender\2.71" 0 AppData2_70
		CreateDirectory "$APPDATA\Blender Foundation\Blender\2.71\scripts\addons"
		StrCpy $INSTDIR "$APPDATA\Blender Foundation\Blender\2.71"
		Return
		
	AppData2_70:
	IfFileExists "$APPDATA\Blender Foundation\Blender\2.70" 0 AppData2_69
		CreateDirectory "$APPDATA\Blender Foundation\Blender\2.70\scripts\addons"
		StrCpy $INSTDIR "$APPDATA\Blender Foundation\Blender\2.70"
		Return
		
	AppData2_69:
	IfFileExists "$APPDATA\Blender Foundation\Blender\2.69" 0 AutoFindFailed
		CreateDirectory "$APPDATA\Blender Foundation\Blender\2.69\scripts\addons"
		StrCpy $INSTDIR "$APPDATA\Blender Foundation\Blender\2.69"
		Return

	AutoFindFailed:
	MessageBox MB_OK "Could not find an installation of a supported version of Blender. Choose your Blender install folder on the next page."
FunctionEnd

;--------------------------------

; Old-style Pages
;Page directory
;Page instfiles
;UninstPage uninstConfirm
;UninstPage instfiles

;--------------------------------

; Modern style pages
!define MUI_PAGE_CUSTOMFUNCTION_SHOW "changeWelcomeTextColor"
!insertmacro MUI_PAGE_WELCOME

; Language setting has to be after welcome page otherwise the welcome image doesn't show
!insertmacro MUI_LANGUAGE "English"
!define MUI_PAGE_CUSTOMFUNCTION_PRE "changeTitleColor"
!insertmacro MUI_PAGE_LICENSE "License.rtf"
Page custom DetectInstallPath
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

;--------------------------------

; The stuff to install
Section "" ;No components page, name is not important
	; Set output path to the installation directory.
	SetOutPath $INSTDIR\scripts\addons\indigo

	; Put files there recursively
	File /r ..\..\sources\indigo\*.py

	; Write the uninstall keys for Windows
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Blendigo" "DisplayName" "Blendigo"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Blendigo" "InstallDir" "$INSTDIR"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Blendigo" "UninstallString" '"$INSTDIR\scripts\addons\Blendigo_uninstall.exe"'
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Blendigo" "NoModify" 1
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Blendigo" "NoRepair" 1
	WriteUninstaller "$INSTDIR\scripts\addons\Blendigo_uninstall.exe"
  
SectionEnd ; end the section

Section "Uninstall"
	Var /GLOBAL INSTALL_DIR
	ReadRegStr $INSTALL_DIR HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Blendigo" "InstallDir"

	; Remove files and uninstaller
	Delete $INSTALL_DIR\scripts\addons\Blendigo_uninstall.exe
	rmdir /r $INSTALL_DIR\scripts\addons\indigo
	rmdir $INSTALL_DIR\scripts\addons\indigo

	; Remove registry keys
	DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\Blendigo"

SectionEnd
