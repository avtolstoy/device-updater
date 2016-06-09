if "%1"=="" goto noversion

set VERSION=%1
set APPNAME=particle_firmware_manager
set FQNAME=%APPNAME%-%VERSION%-windows

rd /s dist

python -m PyInstaller -y --onefile win_onefile.spec --clean

"%SIGNTOOL_PATH%signtool.exe" sign /v /f windows_key.p12 /p %key_secret% /tr http://tsa.starfieldtech.com dist\%FQNAME%.exe
goto done

:noversion
echo Please specify a version

:done

