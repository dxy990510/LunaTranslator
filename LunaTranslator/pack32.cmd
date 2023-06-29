set targetdir=..\build\LunaTranslator_x86
set targetdir_in=..\build\LunaTranslator_x86\LunaTranslator
set pythonlib=%LOCALAPPDATA%\Programs\Python\Python37-32\Lib
set pythondll=%LOCALAPPDATA%\Programs\Python\Python37-32\DLLs
set pythonpackage=%pythonlib%\site-packages

rmdir /S /Q %targetdir%
xcopy ..\build\x86\LunaTranslator_main.dist %targetdir_in% /e /y /I
xcopy .\files %targetdir%\files /e /y /I
copy ..\LICENSE %targetdir%\
xcopy .\LunaTranslator\ocrengines %targetdir_in%\ocrengines /e /y /I
xcopy .\LunaTranslator\webresource %targetdir_in%\webresource /e /y /I
xcopy .\LunaTranslator\postprocess %targetdir_in%\postprocess /e /y /I
xcopy .\LunaTranslator\translator %targetdir_in%\translator /e /y /I
xcopy .\LunaTranslator\cishu %targetdir_in%\cishu /e /y /I
xcopy .\LunaTranslator\tts %targetdir_in%\tts /e /y /I
xcopy .\LunaTranslator\hiraparse %targetdir_in%\hiraparse /e /y /I

xcopy /E /I %pythonpackage%\bcrypt %targetdir_in%\bcrypt
xcopy /E /I %pythonpackage%\certifi %targetdir_in%\certifi
xcopy /E /I %pythonpackage%\charset_normalizer %targetdir_in%\charset_normalizer
xcopy /E /I %pythonpackage%\cryptography %targetdir_in%\cryptography
xcopy /E /I %pythonlib%\http %targetdir_in%\http
xcopy /E /I %pythonpackage%\idna %targetdir_in%\idna
xcopy /E /I %pythonpackage%\websocket %targetdir_in%\websocket
xcopy /E /I %pythondll%\_overlapped.pyd %targetdir_in%

xcopy /E /I %pythonpackage%\OpenSSL %targetdir_in%\OpenSSL
xcopy /I %pythonpackage%\pytz %targetdir_in%\pytz
del %targetdir_in%\pytz\zoneinfo
mkdir %targetdir_in%\pytz\zoneinfo
copy /Y %pythonpackage%\pytz\zoneinfo\UTC %targetdir_in%\pytz\zoneinfo
xcopy /E /I %pythonpackage%\requests %targetdir_in%\requests
xcopy /E /I %pythonpackage%\urllib3 %targetdir_in%\urllib3
xcopy  %pythonpackage%\six.py %targetdir_in%
xcopy  %pythonpackage%\_brotli.cp37-win32.pyd %targetdir_in%
xcopy  %pythonpackage%\_cffi_backend.cp37-win32.pyd %targetdir_in%

xcopy ..\plugins\exec\builds\_x86 %targetdir%\ /e /y /I
del %targetdir_in%\qt5qml.dll
del %targetdir_in%\qt5qmlmodels.dll
del %targetdir_in%\qt5quick.dll
del %targetdir_in%\qt5printsupport.dll
del %targetdir_in%\qt5websockets.dll
del %targetdir_in%\qt5dbus.dll
del %targetdir_in%\qt5multimedia.dll
del %targetdir_in%\qt5svg.dll
del %targetdir_in%\qt5network.dll

del %targetdir_in%\PyQt5\qt-plugins\platforms\qminimal.dll
del %targetdir_in%\PyQt5\qt-plugins\platforms\qwebgl.dll
rmdir /S /Q %targetdir_in%\PyQt5\qt-plugins\mediaservice
rmdir /S /Q %targetdir_in%\PyQt5\qt-plugins\printsupport
rmdir /S /Q %targetdir_in%\PyQt5\qt-plugins\platformthemes
rmdir /S /Q %targetdir_in%\PyQt5\qt-plugins\iconengines

del %targetdir_in%\libssl-1_1-x64.dll
del %targetdir_in%\libcrypto-1_1-x64.dll
 


del %targetdir%\files\plugins\ocr64.dll
del %targetdir%\files\plugins\winsharedutils64.dll
del %targetdir%\files\plugins\winrtutils64.dll
del %targetdir%\files\plugins\libmecab64.dll


xcopy ..\binary\api-ms-win_32 %targetdir_in% /e /y /I

@echo off
setlocal enabledelayedexpansion

set "directory=%targetdir%"

if "%directory%" == "" (
    set /p directory="Enter directory path: "
)

for /f "delims=" %%i in ('dir /b /s "%directory%\*.pyc"') do (
    del "%%i"
)

for /f "delims=" %%d in ('dir /s /b /a:d "%directory%" ^| sort /r') do (
    rd "%%d" 2>nul
)


xcopy %targetdir%\ C:\dataH\LunaTranslator_x86 /e /y /I