if "%1"=="" goto noversion

set VERSION=%1
set APPNAME=particle_device_upgrader
set FQNAME=%APPNAME%-%VERSION%-windows

rd /s /y dist

python -m PyInstaller -y --onefile win_onefile.spec
call sign.bat
goto done

:noversion
echo Please specify a version

:done

